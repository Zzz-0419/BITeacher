import flask_wtf
import wtforms
from wtforms.validators import Email, Length, EqualTo
from models import UserModel, EmailCaptureModel
from exts import db



class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])
    # 验证邮箱是否被注册，验证码是否正确
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(account=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册")

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptureModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或验证码错误")
        else:
            db.session.delete(captcha_model)
            db.session.commit()

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])


class SendCommend(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=0, max=20, message="评论格式不正确")])


class SendReply(wtforms.Form):
    reply = wtforms.StringField(validators=[Length(min=0, max=20, message="回复格式不正确")])

