from flask import Blueprint, render_template, jsonify, redirect, url_for
from exts import mail, db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptureModel
from .forms import RegisterForm
from models import UserModel
from .forms import LoginForm
from werkzeug.security import generate_password_hash

# 之后的适度函数都会以auth为前缀
bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/")
def index():
    return "你好"

@bp.route("/login", methods=['GET', 'POST'])
def login(account="001", password="1234"):

    user = UserModel.query.filter_by(account=account, password=password).first()
    if not user:
        return jsonify({"code": 400, "message": "失败", "data": None})
    else:
        return jsonify({"success": True, "token":})





# 注册函数
@bp.route("/register", methods=['GET', 'POST'])
def register():
    # 如何验证验证码是否正确
    # 表单验证flask-wtf
    if request.method == 'GET':
        # user = UserModel(account="account", password="password")
        # db.session.add(user)
        # db.session.commit()
        # return "注册成功"
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            account = form.email.data
            password = form.email.data
            user = UserModel(account=account, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))


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