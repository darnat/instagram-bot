from ..db import db


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    # hashtag_id = db.Column(db.Integer, db.ForeignKey('hashtag.id'))
    # hashtag = db.relationship('Hashtag',
    #                           backref=db.backref('comments', lazy='dynamic'))

    def __init__(self, content: str):
        self.content = content
        # self.hashtag = hashtag

    def __repr__(self):
        return '<Comment {}>'.format(self.name)
