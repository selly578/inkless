from flask import session,request,jsonify
from shortuuid import uuid
from faker import Faker
from humanize import naturalday,naturaltime
from imgurpython import ImgurClient
from random import randint
from ..models.user import User
from .. import app

IMGUR_ID = "ce3c77177b4e01c"
IMGUR_SECRET = "eb6275603083462c784095668ff4f1e6e5c223ba"

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


@app.errorhandler(404)
def not_found_handler(e):
    return jsonify(msg="data not found"),404 

@app.errorhandler(429)
def too_many_request_handler(e):
    return jsonify(msg="please don't spam :)"),429

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
            "quoted_post": post.quoted.id if post.quoted else None,
            "content": post.content,
            "reply_count": post.reply_count(),
            "like_count": post.like_count(),
            "quote_count": post.quote_count(),
            "user_like_this": current_user in post.liked_user(),
	    "image_url": post.image_url
        }
        __posts.append(_)

    return __posts

def upload_to_imgur(image):
    import requests
    import base64
    url = "https://api.imgur.com/3/image"
    headers = {
        "Authorization": f"Client-ID ce3c77177b4e01c"
    }
    
    data = {
        "key": IMGUR_SECRET,
        "image": base64.b64encode(image.read()),
        "type": "base64",
        "name": "testing.jpg",
        "title": "testing.jpg"
    }
    # Send the file to Imgur as binary data
    response = requests.post(url, headers=headers,data=data)
    print(response)
    return response.json()['data']['link']

