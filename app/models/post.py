from datetime import datetime
from .. import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    title = db.Column(db.String(255), default="Untitled", nullable=False)  # Default title is "Untitled"
    content = db.Column(db.Text, nullable=False)  # Content of the confession
    author = db.Column(db.String(100), default="anonymous", nullable=False)  # Default author is "anonymous"
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Default to current time
