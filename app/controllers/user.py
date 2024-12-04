from flask import Blueprint,render_template,redirect,url_for,request,session
from ..models.user import User
from ..models.post import Post
from .. import db

user = Blueprint("user",__name__)

@user.get("/")
def profile():    
    posts = Post.query.filter_by(author=session["identity"]).all()
    return render_template("profile.html",posts=posts)

@user.post("/")
def save_profile():
    nickname = request.form.get("nickname")    
    user = User.query.filter_by(code=session["identity"]).first()

    if user:
        user.nickname = nickname 
    session["nickname"] = nickname
    db.session.commit()

    return redirect(url_for("user.profile"))

@user.get("/loadaccess")
def load_access():
    return render_template("load.html")

@user.post("/loadaccess")
def load_access_process():
    code = request.form.get("code")
    user_exist = User.query.filter_by(code=code).first()
    post_exist = Post.query.filter_by(author=code).first()

    if user_exist or post_exist:
        session["identity"] = code
        session["nickname"] = user_exist.nickname
        return redirect(url_for("post.index"))

    return render_template("load.html",error="Code not exist or not saved")
