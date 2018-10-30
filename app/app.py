from datetime import date

from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

from app.libs.error_code import ServerError


class JSONEncoder(_JSONEncoder):    #重写default方法
    '''原理:flask的jsonfy方法在得到一个可序列化类型的时候不调用default,
    在得到一个不可序列化的类型时会调用default方法尝试将未知类型转换为json类型，还无法转换则抛出异常'''
    def default(self, o):
        if hasattr(o,'keys') and hasattr(o,'__getitem__'):
            return dict(o)
        if isinstance(o,date):      #default会递归调用，遇到对象下嵌套对象的类型会反复递归序列化
            return o.strftime('%Y-%m-%d')
        raise ServerError()

class Flask(_Flask):
    json_encoder = JSONEncoder      #使用我们自定义的JSONEncoder代替原来内置的JSONEncoder

