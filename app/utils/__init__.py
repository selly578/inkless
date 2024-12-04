from flask import session,request
from shortuuid import uuid
from faker import Faker
from random import randint
from ..models.user import User
from .. import app

@app.template_filter("getnickname")
def get_nickname(identity: str):
    return User.query.filter_by(code=identity).first() or session["nickname"] or "Anonymous"

@app.before_request
def generate_session():
    faker = Faker()
    if not session.get("identity"):
        session["identity"] = uuid(name="key")
        session["nickname"] = User.query.filter_by(code=session["identity"] ).first() or f"{faker.user_name()}-{randint(0,9999)}"        


    session["ip"] = request.remote_addr
    print(session)