from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

home = Blueprint("home", __name__)


@home.route("/")
def homepage():
    if current_user.is_authenticated:
        return redirect(url_for("tasks.manage_tasks"))
    return render_template("home.html")
