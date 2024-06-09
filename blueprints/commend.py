from flask import Blueprint, render_template, jsonify, redirect, url_for
from exts import db
from flask import request
import string
import random
from .forms import SendCommend
from .forms import SendReply
from models import Reply
from datetime import datetime

bp = Blueprint("commend", __name__, url_prefix="/commend")

@bp.route("/content", methods=['GET', 'POST'])
def content(user_id, teacher_id):
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = SendCommend(request.form)
        if form.validate():
            content1 = form.content.data
            user = Reply(user_id=user_id, text=content1, like=0, last_id=0, teacher_id=teacher_id, date=datetime.now)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("commend.content"))
        else:
            print(form.errors)
            return redirect(url_for("commend.content"))

@bp.route("/reply", methods=['POST'])
def reply(user_id, teacher_id, commend_id):
    reply1 = request.args.get("reply")
    user = Reply(user_id=user_id, text=reply1, like=0, last_id=commend_id, teacher_id=teacher_id,
                     date=datetime.now)
    db.session.add(user)
    db.session.commit()
    return jsonify({"code": 200, "message": " ", "data": None})
