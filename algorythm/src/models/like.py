from ..db import db


class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    # comments = db.relationship('Comment', backref='hashtag', lazy='dynamic')

    def __init__(self, user_id, media_id, timestamp):
        self.user_id = user_id
        self.media_id = media_id
        self.timestamp = timestamp

    def __repr__(self):
        return '<Like {} {}>'.format(self.user_id, self.media_id)
