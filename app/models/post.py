from datetime import datetime
from .. import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(255), default="Untitled", nullable=False)  
    content = db.Column(db.Text, nullable=False)  
    author = db.Column(db.String(100), default="anonymous", nullable=False)  
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) 
    parent_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=True)
    
    replies = db.relationship("Post", backref=db.backref("parent", remote_side=[id]), cascade="all, delete-orphan")

    def like_count(self):
        print(Reaction.query.filter_by(post_id=self.id).count())
        return Reaction.query.filter_by(post_id=self.id).count()

    def liked_user(self):
        likes = Reaction.query.filter_by(post_id=self.id).all()
        return [like.user_id for like in likes]

class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.String(50), nullable=False)  
    type = db.Column(db.String(50), default="like")  
    
    post = db.relationship("Post", backref=db.backref("reactions", lazy="dynamic"))