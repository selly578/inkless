from flask import Blueprint,render_template,request,redirect,url_for,session,jsonify
from ..models.post import Post,Reaction
from .. import db  

post = Blueprint("post",__name__)

@post.get("/")
def index():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template("posts.html",title="Posts",posts=posts)

@post.get("/<int:id>")
def _post(id):
    post = Post.query.get_or_404(id) 
    children = Post.query.filter_by(parent_id=post.id).all()
    
    return render_template("post.html",post=post,children=children,reply=False,single_post=True)

@post.get("/create")
def PostForm():
    return render_template("create.html",reply=False)

@post.post("/create")
def procesPostnForm():
    content = request.form.get("content")
    author = session["identity"]

    post = Post(content=content,author=author)
    db.session.add(post)
    db.session.commit()

    return redirect(url_for("post.index"))

@post.get("/reply/<int:id>")
def reply(id):
    post = Post.query.get_or_404(id) 
    return render_template("create.html",post=post,reply=True)

@post.post("/reply/<int:id>")
def save_reply(id):
    content = request.form.get("content")
    author = session["identity"]

    post = Post.query.get_or_404(id) 
    reply = Post(content=content,author=author,parent=post)
    db.session.add(reply)
    db.session.commit()

    return redirect(url_for("post.index"))

# api
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

@post.get("/posts")
def _posts():
    posts = Post.query.all()
    __posts = []
    for post in posts:
        _ = {
            "id": post.id,
            "author": post.author,
            "date_created": post.date_created,
            "parent_id": post.parent.id if post.parent else None,
            "content": post.content
        }
        __posts.append(_)

    return jsonify(posts=__posts)

@post.post("/compose")
def create_post():
    content = request.get_json()["content"]
    author = request.cookies.get("identity")
    parent_id = request.args.get("parent")

    parent = Post.query.filter_by(parent=parent_id).first()
    print(parent)
    post = Post(content=content,author=author)
    db.session.add(post)
    db.session.commit()

    return jsonify(msg="post created")

