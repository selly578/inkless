from flask import Blueprint,render_template,request,redirect,url_for,session,jsonify
from ..models.post import Post,Reaction
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


@post.post("/like/<int:id>")
def like(id):
    like = Reaction.query.filter_by(post_id=id,user_id=session["identity"]).first()

    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify(msg="unlike post")
    
    like = Reaction(post_id=id,user_id=session["identity"])
    db.session.add(like)
    db.session.commit()

    return jsonify(msg="like post")