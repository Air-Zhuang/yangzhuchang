from wtforms import Form
from flask import request

from app.libs.error_code import ParameterException


class BaseForm(Form):
    def __init__(self):        #重写wtforms方法，核心思想就是将原来WTForm不抛出异常的特性改为抛出异常
        # data=request.json                             #这里直接传入表单信息，就不用在视图函数中传入了
        data = request.get_json(silent=True)            #用silent=True这种方式的到get中的请求参数，不会报错
        args=request.args.to_dict()                     #get请求参数
        super(BaseForm,self).__init__(data=data,**args)
    def validate_for_api(self):                         #我们不想覆盖原有的validate方法，所以我们重新写了一个方法
        valid=super(BaseForm,self).validate()           #先获取  validate()  内容
        if not valid:
            raise ParameterException(msg=self.errors)   #从errors属性中获取错误信息
        return self                                     #返回Form,这里很关键