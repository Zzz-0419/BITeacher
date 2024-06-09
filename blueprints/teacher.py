from flask import Blueprint
from models import Teacher
from flask import Blueprint, render_template, jsonify, redirect, url_for

bp = Blueprint("teacher", __name__, url_prefix="/teachers")


@bp.route("/show_details")
def show_details(teacher_id = 1):
    teacher = Teacher.query.filter_by(id=teacher_id).first()
    if teacher:
        path = teacher.info_path
        return path
    else:
        return "没有相应教师"