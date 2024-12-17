from flask import session,request
from shortuuid import uuid
from faker import Faker
from humanize import naturalday,naturaltime
from random import randint
from ..models.user import User
from .. import app

@app.template_filter("getnickname")
def get_nickname(identity: str):
    return User.query.filter_by(code=identity).first() or "Anonymous"

@app.template_filter("naturalday")
def _naturalday(date):
    return naturaltime(date)

@app.before_request
def generate_session():
    faker = Faker()
    if not session.get("identity"):
        session["identity"] = uuid()
        session["nickname"] = User.query.filter_by(code=session["identity"] ).first() or f"{faker.user_name()}-{randint(0,9999)}"        
        session.permanent = True

    session["ip"] = request.remote_addr
    print(session)

def posts_to_json(posts,current_user):
    __posts = [] 
    print(posts)
    for post in posts:
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
            "user_like_this": current_user in post.liked_user()
        }
        __posts.append(_)

    return __posts