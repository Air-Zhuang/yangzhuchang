from collections import namedtuple

from flask import current_app,g,request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadSignature,SignatureExpired

from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scope import is_in_scope

auth=HTTPBasicAuth()    #利用HTTP本身的协议提交token。放在HTTP的头部。
User=namedtuple('User',['uid','ac_type','scope'])

@auth.verify_password
def verify_password(token,password):    #这里将token当做账号，密码不传的方式来传送token,password占位用。(如果实际调用，传入的key:value要经过base64加密)
    '''
    header传账号密码格式:
        key=Authorization
        value=basic base64(Air:123456)
    '''
    user_info=verify_auth_token(token)
    if not user_info:
        return False                    #拿不到用户信息，返回验证不通过
    else:
        g.user=user_info                #将用户信息放在 g 变量中
        return True

def verify_auth_token(token):       #获取token中的信息。验证token合法性
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data=s.loads(token)         #解密的方法
    except BadSignature:            #验证合法性。如果是BadSignature异常，则抛出自定义的AuthFailed
        raise AuthFailed(msg='token is invalid',error_code=1002)
    except SignatureExpired:        #验证是否过期
        raise AuthFailed(msg='token is expired',error_code=1003)
    uid=data['uid']
    ac_type=data['type']
    scope=data['scope']
    allow=is_in_scope(scope,request.endpoint)     #endpoint表示要访问的视图函数，类似于url_for
    if not allow:
        raise Forbidden()
    return User(uid,ac_type,scope)