from werkzeug.exceptions import HTTPException

from app import create_app
from app.libs.error import APIException
from app.libs.error_code import ServerError
import platform

app=create_app()

@app.errorhandler(Exception)            #捕获异常，Flask1.0才可以捕获所有异常
def framework_error(e):
    if isinstance(e,APIException):      #如果是APIException，原样返回回去
        return e
    if isinstance(e,HTTPException):     #如果是HTTPException，转换成APIException
        code=e.code
        msg=e.description
        error_code=1007
        return APIException(msg,code,error_code)
    else:                               #其他python异常返回一个自定义的APIException
        if not app.config['DEBUG']:     #如果当前是调试模式，则返回详细报错信息
            return ServerError()
        else:
            raise e



if __name__ == '__main__':
    if (platform.system() == 'Linux'):
        app.run(host='172.19.91.71', port=8666, debug=app.config['DEBUG'])
    else:
        app.run(host='0.0.0.0', debug=app.config['DEBUG'])