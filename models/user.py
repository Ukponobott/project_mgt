from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from models.project import ProjectModel
from datetime import datetime


class TimeMixin(object):
    created_at = db.Column(db.DateTime(), default=datetime.today())


class UserModel(db.Model, TimeMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    password_hash = db.Column(db.String(80))

    def __init__(self, full_name, email, confirmed, password):
        self.full_name = full_name
        self.email = email
        self.confirmed = confirmed
        self.set_password(password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {"full_name": self.full_name, "email": self.email, "projects": ProjectModel.find_by_id(self.id)}

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    # def __repr__(self):
    #     return '<User %r' % self.username
