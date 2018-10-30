from werkzeug.exceptions import HTTPException
from flask import request,json


class APIException(HTTPException):   #继承HTTPException，重写方法，使其能返回json格式的异常信息
    code=500
    msg='sorry,we make a mistake !'
    error_code=999                  #默认一个未知异常

    def __init__(self,msg=None,code=None,error_code=None,headers=None):
        if code:
            self.code=code
        if error_code:
            self.error_code=error_code
        if msg:
            self.msg=msg
        super(APIException,self).__init__(msg,None)
    def get_body(self, environ=None):   #重写get_body方法
        body=dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method+" "+self.get_url_no_param()
        )
        text=json.dumps(body)
        return text

    def get_headers(self, environ=None):    #get_headers
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():     #给get_body使用，拼接request信息
        full_path=str(request.full_path)
        main_path=full_path.split('?')
        return main_path[0]