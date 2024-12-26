from flask import Blueprint,render_template,redirect,url_for,request,session,make_response,jsonify
from shortuuid import uuid
from faker import Faker
from random import randint
from ..models.user import User
from ..models.post import Post,Reaction
from .. import db,limiter

user = Blueprint("user",__name__)

@user.get("/profile/create")
@limiter.limit("1 per month")
def _profile():
    id = uuid()
    faker = Faker()
    response = make_response(jsonify(msg="create_identity",id=id,nickname=f"{faker.user_name()}-{randint(0,9999)}"))
    response.set_cookie("identity",id,domain='.localhost.local')
    response.set_cookie("nickname","Anonymous",domain='.localhost.local')
    
    return response

@user.post("/profile/load")
def load_profile():
    try:
        code = request.get_json()["code"]    
    except KeyError:
        return jsonify(msg="field code missing"),400
        
    user_exist = User.query.filter_by(code=code).first()
    post_exist = Post.query.filter_by(author=code).first()
    like = Reaction.query.filter_by(user_id=session["identity"]).all()
    if user_exist or post_exist or like:
        response = make_response(jsonify(id=code,nickname=user_exist.nickname if user_exist else "Anonymous"))
        response.set_cookie("identity",code)
        response.set_cookie("nickname","Anonymous")

        return response 
    return jsonify(msg="identity code not found!"),404

@user.post("/profile/edit")
def edit_profile(): 
    id = uuid()
    try:
        nickname = request.get_json()["nickname"]   
    except KeyError:
        return jsonify(msg="field identity missing"),400  
     
    user = User.query.filter_by(code=request.headers.get("user_id")).first()
    if user:
        user.nickname = nickname 
        db.session.commit()
    else:
        user = User(code=request.headers.get("user_id"),nickname=nickname)
        db.session.add(user)
        db.session.commit()
    
    response = make_response(jsonify(msg="sucessfully edit nickname",id=request.headers.get("user_id"),nickname=nickname))
    response.set_cookie("nickname",nickname)
    
    return response
        

