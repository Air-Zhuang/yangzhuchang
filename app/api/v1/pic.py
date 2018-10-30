from flask import jsonify

from app.libs.redprint import Redprint
from app.validators.forms import GetPicForm
from app.libs.error_code import parameter_exception

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

api=Redprint('pic')

@api.route('/<kind>',methods=['GET'])
def get_pic(kind):
    resp = {"value": []}
    form=GetPicForm().validate_for_api()
    with parameter_exception():
        piclist = eval(kind+".query.filter_by(title='" + form.title.data + "').all()")
        resp["value"]=piclist
        return jsonify(resp)

