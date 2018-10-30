from sqlalchemy import Column, Integer, String, SmallInteger
from werkzeug.security import generate_password_hash,check_password_hash

from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db


class User(Base):
    id=Column(Integer,primary_key=True)
    email=Column(String(24),unique=True,nullable=False)
    nickname=Column(String(24),unique=True)
    auth=Column(SmallInteger,default=1)         #1为普通用户，2为管理员
    _password=Column('password',String(100))

    def keys(self):                             #keys和__getitem__一起使用可以实现dict(类)的功能，实例在Test35 __getitem__中
        return ['id','email','nickname','auth']
    # def __getitem__(self, item):              #放在Base基类中了
    #     return getattr(self,item)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw):
        self._password=generate_password_hash(raw)

    def check_password(self,raw):
        if not self._password:
            return False
        return check_password_hash(self._password,raw)


    @staticmethod
    def register_by_email(nickname,account,secret):
        with db.auto_commit():
            user=User()
            user.nickname=nickname
            user.email=account
            user.password=secret
            db.session.add(user)

    @staticmethod
    def verify(email,password):
        user=User.query.filter_by(email=email).first_or_404()
        # if not user:                              #检查是否有这个用户,因为重写了get_or_404这个方法，这两行可以省略
        #     raise NotFound(msg='user not found')
        if not user.check_password(password):       #检查密码是否正确
            raise AuthFailed()
        scope='AdminScope' if user.auth==2 else 'UserScope'
        return {'uid':user.id,'scope':scope}