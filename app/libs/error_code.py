from app.libs.error import APIException


class Success(APIException):
    code=201            #操作成功的返回，不要被继承APIException迷惑，这里会返回201
    msg='ok'
    error_code = 0      #自定义成功信息

class DeleteSuccess(Success):
    code=202
    error_code = 1

class ServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = 999

class ClientTypeException(APIException):   #继承自己实现的APIException异常，返回json的异常信息
    code = 400          #请求参数错误
    msg='client is invalid'
    error_code = 1006   #自定义错误信息

class ParameterException(APIException):     #全局WTForm异常
    code=400
    msg='Check your parameters.'
    error_code = 1000   #自定义错误信息

class NotFound(APIException):
    code=404
    msg='The resource are not_found !'
    error_code = 1001   #自定义错误信息

class AuthFailed(APIException):
    code=401        #禁止访问
    msg='authorization failed'
    error_code = 1005   #自定义错误信息

class Forbidden(APIException):
    code=403        #权限不够
    msg='forbidden, not in scope'
    error_code = 1004


class DuplicateGift(APIException):
    code = 400
    error_code = 2001
    msg = 'the current book has already in gift'