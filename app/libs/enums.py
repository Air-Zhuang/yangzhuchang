from enum import Enum

class ClientTypeEnum(Enum):
    USER_EMAIL=100      #用邮箱的方式
    USER_MOBILE=101     #用手机号的方式
    USER_MINA=200       #微信小程序
    USER_WX=201         #微信公众号

if __name__ == '__main__':
    print(ClientTypeEnum.USER_EMAIL.value)
    print(ClientTypeEnum.USER_EMAIL.name)
    print(ClientTypeEnum.USER_EMAIL)
    print(ClientTypeEnum(100).value)
    print(ClientTypeEnum(100).name)
    print(ClientTypeEnum(100))