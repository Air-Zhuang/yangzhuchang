from flask import jsonify,current_app

from app.libs.redprint import Redprint

api=Redprint('domain')

@api.route('',methods=['GET'])
def get_domain():
    resp={"value":{}}
    resp["value"]["ori_url"]=current_app.config["ORI_URL_DOMAIN"]
    resp["value"]["local_url"]=current_app.config["LOCAL_URL_DOMAIN"]
    return jsonify(resp)
