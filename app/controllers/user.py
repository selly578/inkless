from flask import Blueprint,render_template,redirect,url_for,request,session,make_response,jsonify
from shortuuid import uuid
from ..models.user import User
from ..models.post import Post,Reaction
from .. import db,limiter

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

    return render_template("load.html",error="Identity not exist or not saved")

@user.get("/profile/create")
@limiter.limit("1 per month")
def _profile():
    id = uuid()
    response = make_response(jsonify(msg="create_identity",id=id,nickname="Anonymous"))
    response.set_cookie("identity",id,domain='.localhost.local')
    response.set_cookie("nickname","Anonymous",domain='.localhost.local')
    
    return response

@user.post("/profile/load")
def load_profile():
    try:
        code = request.get_json()["identity"]    
    except KeyError:
        return jsonify(msg="field identity missing"),400
        
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
        

