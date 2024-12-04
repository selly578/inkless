from flask import Blueprint,render_template,request,redirect,url_for,session
from ..models.post import Post
from .. import db  

post = Blueprint("post",__name__)

@post.get("/")
def index():
    posts = Post.query.all()
    return render_template("posts.html",title="Posts",posts=posts)

@post.get("/create")
def PostForm():
    return render_template("create.html",title="Create post")

@post.post("/create")
def procesPostnForm():
    content = request.form.get("content")
    author = session["identity"]

    post = Post(content=content,author=author)
    db.session.add(post)
    db.session.commit()

    return redirect(url_for("post.index"))


