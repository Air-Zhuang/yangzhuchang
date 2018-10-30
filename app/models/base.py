from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import inspect, Column, Integer, SmallInteger, orm
from contextlib import contextmanager

from app.libs.error_code import NotFound


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident):    #重写get_or_404,返回自定义异常
        rv = self.get(ident)
        if not rv:
            raise NotFound()
        return rv

    def first_or_404(self):         #first_or_404,返回自定义异常
        rv = self.first()
        if not rv:
            raise NotFound()
        return rv


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    create_time = Column(Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def __getitem__(self, item):        #keys和__getitem__一起使用可以实现dict(类)的功能，实例在Test35 __getitem__中
        return getattr(self, item)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        self.status = 0

    def keys(self):             #为了能使用hide()方法，将每个model想展现字段的keys列表放在各自的__init__中。参考book,记得打orm装饰器
        return self.fields

    def hide(self,*keys):       #实现了隐藏不想展现的字段的功能
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self,*keys):     #和hide()方法相反，是追加属性
        for key in keys:
            self.fields.append(key)
        return self

#     def keys(self):
#         return self.fields
#
#     def hide(self, *keys):
#         for key in keys:
#             self.fields.remove(key)
#         return self
#
#     def append(self, *keys):
#         for key in keys:
#             self.fields.append(key)
#         return self
#
#
# class MixinJSONSerializer:
#     @orm.reconstructor
#     def init_on_load(self):
#         self._fields = []
#         # self._include = []
#         self._exclude = []
#
#         self._set_fields()
#         self.__prune_fields()
#
#     def _set_fields(self):
#         pass
#
#     def __prune_fields(self):
#         columns = inspect(self.__class__).columns
#         if not self._fields:
#             all_columns = set(columns.keys())
#             self._fields = list(all_columns - set(self._exclude))
#
#     def hide(self, *args):
#         for key in args:
#             self._fields.remove(key)
#         return self
#
#     def keys(self):
#         return self._fields
#
#     def __getitem__(self, key):
#         return getattr(self, key)
