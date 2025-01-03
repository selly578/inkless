from flask import Blueprint,render_template,request,redirect,url_for,session,jsonify
from ..models.post import Post,Reaction
from ..models.user import User
from ..utils import posts_to_json,upload_to_imgur
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
    sort_by = request.args.get("sort","latest")
    posts = Post.query.all()

    __posts = posts_to_json(posts,user_id)

    if sort_by.lower() == "latest":
       __posts = sorted(__posts, key=lambda d: d["date_created"],reverse=True)

    if sort_by.lower() == "oldest":
       __posts = sorted(__posts, key=lambda d: d["date_created"])
    
    if sort_by.lower() == "most_likes":
       __posts = sorted(__posts, key=lambda d: d["like_count"],reverse=True)

    if sort_by.lower() == "least_likes":
       __posts = sorted(__posts, key=lambda d: d["date_created"])


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
        "quoted_post": post.quoted.id if post.quoted else None,
        "content": post.content,
        "reply_count": post.reply_count(),
        "like_count": post.like_count(),
        "quote_count": post.quote_count(),
        "user_like_this": user_id in post.liked_user(),
	    "image_url": post.image_url
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
    content = request.form.get("content")
    author = request.headers.get("user_id")
    parent_id = request.form.get("parent")
    quoted_id = request.form.get("quoted")
    image = request.files.get("image")
    image_url = None
    print(request.form)		
    if image:
        print(image)
        image_url = upload_to_imgur(image)

    parent = Post.query.filter_by(id=parent_id).first()
    quoted = Post.query.filter_by(id=quoted_id).first()
    post = Post(content=content,author=author,parent=parent,quoted=quoted,image_url=image_url)
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
