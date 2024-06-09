from exts import db


# userinfo.only_user可以访问账号密码
# user.information可以访问具体信息
class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("userinfo.id"), autoincrement=True)
    information = db.relationship("UserInfoModel", backref="only_user")
    # email = db.Column(db.String(100), nullable=False, unique=True)
    # join_time = db.Column(db.DateTime, default=datetime.now)


class bearertoken(db.Model):
    __tablename__ = "token_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(100), nullable=False)
    token = db.Column(db.String(1000), nullable=False)

class Captcha(db.Model):
    __tablename__ = "captcha_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)

class UserInfoModel(db.Model):
    __tablename__ = "userinfo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(100), nullable=True, unique=True)
    wechat = db.Column(db.String(100), nullable=True, unique=True)
    qq = db.Column(db.String(100), nullable=True, unique=True)
    email = db.Column(db.String(100), nullable=True, unique=True)


class UserCollection(db.Model):
    __tablename__ = "collection"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    use_id = db.Column(db.Integer, nullable=True, unique=True)
    collection = db.Column(db.Integer, nullable=True, unique=True)


# reply.information可以访问用户具体信息
# userinfo.replys可以看用户所有评论
class Reply(db.Model):
    __tablename__ = "reply"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("userinfo.id"))
    text = db.Column(db.Text)
    like = db.Column(db.Integer, default=0)
    last_id = db.Column(db.Integer)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"))
    date = db.Column(db.DateTime)
    information = db.relationship("UserInfoModel", backref="replys")
    teacherinfo = db.relationship("Teacher", backref="teacher_reply")

# reply.teacherinfo可以看教师信息
# teacher.teacher_reply可以看相应回答
class Teacher(db.Model):
    __tablename__ = "teacher"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    info_path = db.Column(db.String(100))
    eval_num = db.Column(db.Integer, default=0)
    score = db.Column(db.Float,default=0.0)

class CollegeTeacher(db.Model):
    __tablename__ = "collegeteacher"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    college = db.Column(db.String(100), nullable=False)
    teachername = db.Column(db.String(100), nullable=False)

class EmailCaptureModel(db.Model):
    __tablename__ = "email_capture"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)
    used = db.Column(db.Boolean, default=False)