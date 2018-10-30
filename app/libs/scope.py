
class Scope:
    allow_api=[]
    allow_module=[]
    forbidden=[]
    def __add__(self,other):
        self.allow_api=self.allow_api+other.allow_api
        self.allow_api=list(set(self.allow_api))        #去重

        self.allow_module = self.allow_module + other.allow_module
        self.allow_module = list(set(self.allow_module))  # 去重

        self.forbidden = self.forbidden + other.forbidden
        self.forbidden = list(set(self.forbidden))  # 去重
        return self

class AdminScope(Scope):
    # allow_api=['v1.user+super_get_user','v1.user+super_delete_user']        #2
    allow_module = ['v1.user']                                            #3#1
    # def __init__(self):                                                     #2
    #     self + UserScope()                                                  #2

class UserScope(Scope):
    # forbidden = ['v1.user+super_get_user','v1.user+super_delete_user']    #3
    # def __init__(self):                                                   #3
    #     self+AdminScope()                                                 #3
    allow_api = ['v1.user+get_user','v1.user+delete_user']                  #2


def is_in_scope(scope,endpoint):
    '''
    当前endpoint格式为v1.view_func
    我们将endpoint的格式变为v1.module_name+view_func 相当于 v1.redprint+view_func
    '''
    scope=globals()[scope]()                #通过字符串转化成对象
    splits=endpoint.split('+')
    red_name=splits[0]
    if endpoint in scope.forbidden:         #三个判断顺序不能变
        return False
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:      #可以访问整个红图下的所有视图函数
        return True
    else:
        return False