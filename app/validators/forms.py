from wtforms import StringField,IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError

from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm as Form        #使用自定义的WTForm


class ClientForm(Form):
    account=StringField(validators=[DataRequired(message='不允许为空'),length(min=5,max=32)])       #账号
    secret=StringField()                                                        #密码
    type=IntegerField(validators=[DataRequired()])                              #客户端类型

    def validate_type(self,value):
        try:
            client=ClientTypeEnum(value.data)                                   #判断是否能将数字类型转换成枚举类型
        except ValueError as e:
            raise e                                                             #这里有异常，WTForm不会抛出，而会把异常记录在errors属性中
        self.type.data=client                                                   #将type赋值为枚举类型

class UserEmailForm(ClientForm):                                                #继承ClientForm，可以编写个性化的form
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    nickname = StringField(validators=[DataRequired(),
                                       length(min=2, max=22)])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()     #抛出WTForm异常

class TokenForm(Form):
    token=StringField(validators=[DataRequired()])

class CateListForm(Form):
    kind=StringField(validators=[DataRequired()])

class GetPicForm(Form):
    title=StringField(validators=[DataRequired()])