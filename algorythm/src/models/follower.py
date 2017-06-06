from ..db import db


class Follower(db.Model):
    __tablename__ = 'followers'
    id = db.Column(db.Integer, primary_key=True)
    pk = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    unfollowed = db.Column(db.Boolean, default=False, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)

    def __init__(self, pk: str, name: str, timestamp):
        self.pk = pk
        self.name = name
        self.timestamp = timestamp

    def __repr__(self):
        return '<Follower {}>'.format(self.pk)
