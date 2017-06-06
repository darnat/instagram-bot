from ..db import db


class Hashtag(db.Model):
    __tablename__ = 'hashtags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    blacklisted = db.Column(db.Boolean, default=False, nullable=False)
    # comments = db.relationship('Comment', backref='hashtag', lazy='dynamic')

    def __init__(self, name: str, blacklisted: bool=False):
        self.name = name
        self.blacklisted = blacklisted

    def __repr__(self):
        return '<Hashtag {}>'.format(self.name)
