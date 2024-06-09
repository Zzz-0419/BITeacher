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
from flask_jwt_extended import create_access_token
from flask_migrate import Migrate



app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'my_secret_key222'
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(teacher_bp)


@app.route('/')
def showindexpage():  # put application's code here
    directory = "./static/pictures"
    picture_urls = []
    for filename in os.listdir(directory):
        # 该 url 可以直接放到 html 文件中进行输出
        picture_urls.append("/pictures/" + filename)
        print(filename)
        print(picture_urls)

    return render_template("index.html", picture_url=picture_urls[0])


# 项目首页，其中应该有能够获取个人信息的页面
# 这里应该获得 user_id
@app.route("/Username")
def giveUserProfile(user_id=1):
    # id = request.json
    userinfo = UserInfoModel.query.get(user_id)
    if userinfo:
        return f"nickname: {userinfo.nickname}, wechat: {userinfo.wechat}, qq: {userinfo.qq}, email: {userinfo.email}"
    else:
        return f"You have not logged in or registered"


# 应该接收到一个 user_id 参数
@app.route("/password")
def getPass(user_id=1):
    # id = request.json
    userpas = UserModel.query.get(user_id)
    if userpas:
        return f"id:{userpas.id}\n, password: {userpas.password}\n"
    else:
        return f"You have not logged in"


# 定义带参数 url 还可以定义参数类型： string, int, float, path, uuid, any
@app.route("/profile/<prof_id>")
def profile_with_parameter(prof_id):
    return render_template("Book_detail.html", prof_id=prof_id)


# 可传可不传的参数，通过查询字符串的方式传参
# /book/list
# /book/list?page=2

@app.route('/like')
def likeComment(comment_id=1, like_status=False):
    # like_status 怎么确定（如何确定一个用户是否已经对某条（评论点赞）
    comment = Reply.query.get(comment_id)
    if comment and like_status is True:
        comment.like = comment.like - 1
        db.session.commit()
    elif comment and like_status is False:
        comment.like = comment.like + 1
        db.session.commit()
    else:
        return f"You have no comment"
    # 这里还应该有一个更改点赞图标的步骤
    return "Liked"

# 已经能够查找出所有评论
@app.route('/showcomment')
def showComment(teacherid = 1):
    # reply = Reply(user_id=1, text="1122", like=2, last_id=1, teacher_id=1, date=datetime.datetime.now())
    # db.session.add(reply)
    # db.session.commit()
    teacher = Teacher.query.filter_by(id=teacherid).first()
    # 所有的一级评论
    for comments in teacher.teacher_reply:
        if comments.last_id == 0:
            print('First Class Review')
            # 寻找该评论下所有的子评论
            print("User:" + giveUserProfile(comments.user_id))
            print("Text:" + comments.text)
            print('LikeNumber: ', comments.like)
            print('SubComments: ', comments)
            for comment in Reply.query.filter_by(last_id=comments.id).all():
                print(comment.text)

        else:
            print('Second Class Review')
            continue

    return "Teacher comments"


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)