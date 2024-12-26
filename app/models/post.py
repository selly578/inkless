from datetime import datetime
from .. import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(255), default="Untitled", nullable=False)  
    content = db.Column(db.String(200), nullable=False)  
    author = db.Column(db.String(100), default="anonymous", nullable=False)  
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) 
    parent_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=True)
    quoted_post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=True)
    image_url = db.Column(db.String(100))  
    replies = db.relationship("Post", backref=db.backref("parent", remote_side=[id]), 
                              cascade="all, delete-orphan", foreign_keys=[parent_id])
    quotes = db.relationship("Post", backref=db.backref("quoted", remote_side=[id]),
                             foreign_keys=[quoted_post_id])
    def reply_count(self):
        return Post.query.filter_by(parent_id=self.id).count()

    def like_count(self):       
        return Reaction.query.filter_by(post_id=self.id).count()

    def liked_user(self):
        likes = Reaction.query.filter_by(post_id=self.id).all()
        return [like.user_id for like in likes]
    
    def quote_count(self):
        return Post.query.filter_by(quoted_post_id=self.id).count()
        

class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.String(50), nullable=False)  
    type = db.Column(db.String(50), default="like")  
    
    post = db.relationship("Post", backref=db.backref("reactions", lazy="dynamic"))