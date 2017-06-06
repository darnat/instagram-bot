from ..db import db


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    pk = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, pk, name):
        self.pk = pk
        self.name = name

    def __repr__(self):
        return '<Location {}>'.format(self.pk)
