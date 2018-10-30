from app.libs.enums import ClientTypeEnum
from app.libs.error_code import Success
from app.libs.redprint import Redprint


from app.models.user import User
from app.validators.forms import ClientForm, UserEmailForm

api=Redprint('client')

@api.route('/register',methods=['POST'])
def create_client():
    form=ClientForm().validate_for_api()                #已经在BaseForm重写了__init__方法，这里不需要传入表单信息了。如果传过来的是json,要用data=data。使用自己重写的validate方法
    promise={                                           #用字典的形式处理不同客户端的处理方式
        ClientTypeEnum.USER_EMAIL:__register_user_by_email
    }
    promise[form.type.data]()
    return Success()                                    #使用return HTTPException

def __register_user_by_email():
    form=UserEmailForm().validate_for_api()             #已经在BaseForm重写了__init__方法，这里不需要传入表单信息了。如果传过来的是json,要用data=data
    User.register_by_email(form.nickname.data,form.account.data,form.secret.data)