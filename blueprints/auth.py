from flask import Blueprint, render_template, jsonify, redirect, url_for
from exts import mail, db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptureModel
from .forms import RegisterForm
from models import UserModel
from models import Captcha
from models import UserInfoModel
from models import bearertoken
from flask_jwt_extended import create_access_token
import json
from .forms import LoginForm
from werkzeug.security import generate_password_hash

# 之后的适度函数都会以auth为前缀
bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/")
def index():
    return "你好"

@bp.route("/login", methods=['GET', 'POST'])
def login(account="111", password="1234"):
    # username = json.dumps(account)
    user = UserModel.query.filter_by(account=account, password=password).first()
    if not user:
        return jsonify({"success": False, "token": "有问题"}), 400
    else:
        access_token = create_access_token(identity=account)
        token = bearertoken(account=account, token=access_token)
        db.session.add(token)
        db.session.commit()
        #return access_token
        return jsonify({"success": True, "token": access_token}), 200





# 注册函数
@bp.route("/register", methods=['GET', 'POST'])
def register(phone="7891", captcha="345", password="nihao", confirmPassword="nihao"):
   user1 = Captcha.query.filter_by(account=phone).first()
   chap = user1.captcha
   if chap == captcha and password==confirmPassword:
       user = UserModel(account=phone, password=password)
       db.session.add(user)
       userinfo = UserInfoModel()
       db.session.add(userinfo)
       db.session.commit()
       return jsonify({"success": True, "message": "注册成功"})
   else:
       return jsonify({"success": False, "message": "注册失败"})


@bp.route("/capture/email")
def get_email_capcha():
    # 运用问号的方式传参
    email = request.args.get("email")
    # 随机的组合
    source = string.digits*4
    capture = random.sample(source, 4)
    # 需要将列表改成字符串
    capture = "".join(capture)
    # print(capture)
    message = Message(subject="验证注册", recipients=[email], body=f"你的验证码是{capture}")
    mail.send(message)
    # 服务器中需要存储一份
    # 用数据库来存储
    email_captcha = EmailCaptureModel(email=email, captcha=capture)
    db.session.add(email_captcha)
    db.session.commit()
    # 返回正确错误的特定代码,以及错误信息
    return jsonify({"code": 200, "message": " ", "data": None})


@bp.route("/mail/test")
def mail_test():
    message = Message(subject="test", recipients=["1120212093@bit.edu.cn"], body="this is a test mail")
    mail.send(message)
    return "邮件发送成功"