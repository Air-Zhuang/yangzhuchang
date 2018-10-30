'''蓝图route方法
def route(self, rule, **options):
    """Like :meth:`Flask.route` but for a blueprint.  The endpoint for the
    :func:`url_for` function is prefixed with the name of the blueprint.
    """
    def decorator(f):
        endpoint = options.pop("endpoint", f.__name__)
        self.add_url_rule(rule, endpoint, f, **options)
        return f
'''

''' 实质上还是插入到蓝图的add_url_rule，只不过红图相当于暂时保存了插入蓝图时的变量'''
class Redprint:
    def __init__(self,name):
        self.name=name
        self.mound=[]

    def route(self,rule,**options): #参考蓝图的route方法实现红图的route方法
        def decorator(f):
            self.mound.append((f,rule,options))
            return f
        return decorator

    def register(self,bp,url_prefix=None):
        if url_prefix is None:
            url_prefix='/'+self.name
        for f,rule,options in self.mound:
            # endpoint = options.pop("endpoint", f.__name__)
            endpoint = self.name+'+'+options.pop("endpoint", f.__name__)       #自定义endpoint格式，变为v1.redprint+view_func
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)