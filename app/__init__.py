from .app import Flask

def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(),url_prefix='/v1')

def register_plugin(app):       #注册SQLAlchemy插件
    from app.models.base import db
    from flask_cors import CORS         #设置跨域请求头
    CORS(app, supports_credentials=True)
    db.init_app(app)
    with app.app_context():     #因为不在create_app函数中，需要调用app_context上下文管理器，将其推入到栈中
        db.create_all()

def create_app():
    app=Flask(__name__)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')

    register_blueprints(app)
    register_plugin(app)
    return app