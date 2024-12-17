from flask import Blueprint,render_template,request,redirect,url_for,session,jsonify
from ..models.post import Post,Reaction
from ..models.user import User
from ..utils import posts_to_json
from .. import db  

post = Blueprint("post",__name__)

# api
@post.post("/like/<int:id>")
def like(id):
    user_id = request.headers.get("user_id")
    like = Reaction.query.filter_by(post_id=id,user_id=user_id).first()

    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify(msg="unlike post")
    
    like = Reaction(post_id=id,user_id=user_id)
    db.session.add(like)
    db.session.commit()

    return jsonify(msg="like post")

@post.get("/")
def _posts():
    user_id = request.headers.get("user_id")
    posts = Post.query.order_by(Post.date_created.desc()).all()

    __posts = posts_to_json(posts,user_id)

    return jsonify(__posts)

@post.get("/<int:id>")
def _post(id):
    user_id = request.headers.get("user_id")
    post = Post.query.get_or_404(id)
    author = User.query.filter_by(code=post.author).first()

    _ = {
        "id": post.id,
        "author": {
            "id": author.code if author else post.author,
            "nickname": author.nickname if author else "Anonymous"
        },
        "date_created": post.date_created,
        "parent_id": post.parent.id if post.parent else None,
        "content": post.content,
        "reply_count": post.reply_count(),
        "like_count": post.like_count(),
        "user_like_this": user_id in post.liked_user()
    }

    return jsonify(_)

@post.get("/<int:id>/reply")
def _reply(id):
    user_id = request.headers.get("user_id")
    parent = Post.query.filter_by(id=id).first()
    replies = Post.query.filter_by(parent=parent).order_by(Post.date_created.desc()).all()

    __replies = posts_to_json(replies,user_id)

    return jsonify(__replies)


@post.post("/compose")
def create_post():
    content = request.get_json()["content"]
    author = request.headers.get("user_id")
    parent_id = request.get_json().get("parent")

    parent = Post.query.filter_by(id=parent_id).first()
    print(parent)
    post = Post(content=content,author=author,parent=parent)
    db.session.add(post)
    db.session.commit()

    return jsonify(msg="post created")

@post.get("/search")
def search():
    query = request.args.get("q")
    user_id = request.headers.get("user_id")
    print(query)
    posts = Post.query.filter(Post.content.like(f"%{query}%")).all()
    __posts = posts_to_json(posts,user_id)

    return jsonify(__posts)

@post.get("/user")
def user_posts():
    user_id = request.headers.get("user_id")
    posts = Post.query.filter_by(author=user_id).all()
    __posts = posts_to_json(posts,user_id)

    return jsonify(__posts)
