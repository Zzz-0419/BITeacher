from flask import Flask, render_template, request
import config
from exts import db, mail
from models import UserModel
from models import UserInfoModel
from models import Reply
from models import Teacher
from blueprints.user import bp as user_bp
from blueprints.auth import bp as auth_bp
from blueprints.teacher import bp as teacher_bp
from sqlalchemy import text
import os
from flask_jwt_extended import create_access_token,JWTManager
from flask_migrate import Migrate



app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'my_secret_key222'
jwt = JWTManager(app)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(teacher_bp)


@app.route('/')
def showindexpage():  # put application's code here

    return "ok"


# 项目首页，其中应该有能够获取个人信息的页面
# 这里应该获得 user_id



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)