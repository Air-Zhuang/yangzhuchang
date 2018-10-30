from flask import jsonify

from app.libs.error_code import ParameterException
from app.libs.redprint import Redprint
from app.models.cate import Cate
from app.validators.forms import CateListForm

from app.models.base import db
from app.models.aiyouwu import Aiyouwu
from app.models.bololi import Bololi
from app.models.girlt import Girlt
from app.models.legbaby import Legbaby
from app.models.missleg import Missleg
from app.models.slady import Slady
from app.models.tgod import Tgod
from app.models.toutiao import Toutiao
from app.models.tuigirl import Tuigirl
from app.models.ugirls import Ugirls

api=Redprint('cate')

@api.route('',methods=['GET'])
def get_cate():
    resp={"value":[]}
    cate=Cate.query.filter_by().all()                           #所有公司名
    resp["value"] = [i.hide('id').cate_name for i in cate]      #隐藏id列
    return jsonify(resp)

@api.route('/list',methods=['GET'])
def get_cate_list():
    resp = {"value": []}
    form=CateListForm().validate_for_api()                      #form.kind.data为查询参数
    try:
        catelist = eval("db.session.query("+form.kind.data+".title).filter("+form.kind.data+".status == 1).distinct().all()")
        resp["value"]=[i[0] for i in catelist]                      #多个list合并成一个list
        return jsonify(resp)
    except Exception as e:
        raise ParameterException
