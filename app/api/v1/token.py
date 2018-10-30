from flask import current_app,jsonify

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import AuthFailed
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, TokenForm

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

api=Redprint('token')

@api.route('',methods=['POST'])
def get_token():
    """生成令牌"""
    '''
        http://localhost:5000/v1/token
        {"account":"999@qq.com","secret":"123456","type":100}
    '''
    form=ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify
    }
    identity=promise[ClientTypeEnum(form.type.data)](   #调用User.verify方法返回一个携带用户信息的字典
        form.account.data,
        form.secret.data
    )
    #生成token令牌
    expiration=current_app.config['TOKEN_EXPIRATION']
    token=generate_auth_token(identity['uid'],form.type.data,identity['scope'],expiration)
    t={
        'token':token.decode('ascii')       #将bytes类型字符串转化成普通字符串
    }
    return jsonify(t),201                   #返回一个json字符串和一个状态码



@api.route('/secret', methods=['POST'])
def get_token_info():
    """获取令牌信息"""
    '''
    http://localhost:5000/v1/token/secret
    {"token":"eyJhbGciOiJIUzIgjb7Y"}
    '''
    form = TokenForm().validate_for_api()
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(form.token.data, return_header=True)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)

    r = {
        'scope': data[0]['scope'],
        'create_at': data[1]['iat'],        #token创建时间
        'expire_in': data[1]['exp'],        #token有效期
        'uid': data[0]['uid']
    }
    return jsonify(r)

def generate_auth_token(uid,ac_type,scope=None,expiration=7200):    #scope:权限作用域，expiration:过期时间
    '''生成token令牌的方法'''
    s=Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
    return s.dumps({            #调用序列化器的dumps方法写入想写入的信息。 返回一个bytes类型字符串
        'uid':uid,              #令牌中写入用户id
        'type':ac_type.value,   #令牌中写入客户端类型
        'scope':scope
    })