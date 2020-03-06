from kronos import db, login_manager
from flask_login import UserMixin
from sqlalchemy.ext.associationproxy import association_proxy


class Performer(db.Model):
    __tablename__ = "performer"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(25), unique=True, nullable=False)

    phone_number = db.Column(db.Integer, nullable=True, default=0)

    member_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, name, number, defense_points):
        self.name = name
        self.number = number

    def __repr__(self):
        return (f"Performer('Name: {self.name}', Number: {self.number}, ")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), unique=True, nullable=False)
    last_name = db.Column(db.String(25), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    performers = db.relationship("Performer")

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return (f"Member('{self.first_name, self.last_name}")
