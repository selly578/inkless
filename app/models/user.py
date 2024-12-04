from datetime import datetime
from .. import db 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    code = db.Column(db.String(255), nullable=False)  # Default title is "Untitled"
    nickname = db.Column(db.Text, default="Anonymous")  # Content of the confession
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Default to current time

    def __repr__(self):
        return self.nickname