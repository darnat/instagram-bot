from ..db import db


class Blacklist(db.Model):
    __tablename__ = 'blacklists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    pattern_only = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, name: str, pattern_only: bool):
        self.name = name
        self.pattern_only = pattern_only
        # self.hashtag = hashtag

    def __repr__(self):
        return '<Blacklist {}>'.format(self.name)
