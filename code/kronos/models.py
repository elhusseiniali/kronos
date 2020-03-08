from kronos import db, login_manager
from flask_login import UserMixin
from sqlalchemy_utils import EmailType


class Performer(db.Model):
    __tablename__ = "performer"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(25), unique=True, nullable=False)

    phone_number = db.Column(db.Integer, nullable=True)

    member_id = db.Column(db.Integer, db.ForeignKey("member.id"))
    member = db.relationship('Member',
                             back_populates='performers')

    performances = db.relationship("Performance",
                                   back_populates='performer')

    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

    def __repr__(self):
        return (f"Performer('Name: {self.name}', 'Number: {self.phone_number}')")


class Stage(db.Model):
    __tablename__ = "stage"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), unique=True, nullable=False)

    performances = db.relationship('Performance',
                                   back_populates='stage')
    boxes = db.relationship('Box',
                            back_populates='stage')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return (f"Stage('{self.name}')")


class Performance(db.Model):
    __tablename__ = "performance"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    duration = db.Column(db.Integer, nullable=False)
    when = db.Column(db.DateTime, nullable=False)

    performer_id = db.Column(db.Integer,
                             db.ForeignKey("performer.id"),
                             nullable=False)
    performer = db.relationship("Performer",
                                back_populates='performances')

    stage_id = db.Column(db.Integer,
                         db.ForeignKey("stage.id"))
    stage = db.relationship('Stage',
                            back_populates='performances')

    checkin = db.relationship('CheckIn',
                              back_populates='performance')
    checkout = db.relationship('CheckOut',
                               back_populates='performance')

    def __init__(self, performer_id, when):
        self.performer_id = performer_id
        self.when = when

    def __repr__(self):
        return (f"Performance('Performer: {self.performer_id}'))")


class Member(db.Model):
    __tablename__ = "member"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(25), unique=True, nullable=False)
    last_name = db.Column(db.String(25), unique=True, nullable=False)

    email = db.Column(EmailType)
    password = db.Column(db.String(60), nullable=False)

    performers = db.relationship('Performer',
                                 back_populates='member')

    checkins = db.relationship('CheckIn',
                               back_populates='member')
    checkouts = db.relationship('CheckOut',
                                back_populates='member')

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return (f"Member('{self.last_name}')")


class CheckIn(db.Model):
    __tablename__ = "checkin"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    when = db.Column(db.DateTime, nullable=False)

    performance_id = db.Column(db.ForeignKey('performance.id'), nullable=False)
    performance = db.relationship('Performance',
                                  back_populates='checkin')

    member_id = db.Column(db.Integer,
                          db.ForeignKey('member.id'),
                          nullable=False)
    member = db.relationship('Member',
                             back_populates='checkins')

    storage = db.relationship('Storage',
                              back_populates='checkin')

    def __init__(self, member_id, performance_id):
        self.member_id = member_id
        self.performance_id = performance_id

    def __repr__(self):
        return (f"Performance('{self.performance_id}')")


class CheckOut(db.Model):
    __tablename__ = "checkout"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    when = db.Column(db.DateTime, nullable=False)

    performance_id = db.Column(db.ForeignKey('performance.id'))
    performance = db.relationship('Performance',
                                  back_populates='checkout')

    member_id = db.Column(db.Integer,
                          db.ForeignKey('member.id'))
    member = db.relationship('Member',
                             back_populates='checkouts')

    def __init__(self, member_id, performance_id):
        self.member_id = member_id
        self.performance_id = performance_id

    def __repr__(self):
        return (f"Member('{self.member_id}')",
                f"Performance('{self.performance_id}')")


class Box(db.Model):
    __tablename__ = "box"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    stage_id = db.Column(db.Integer,
                         db.ForeignKey('stage.id'))
    stage = db.relationship('Stage',
                            back_populates='boxes')

    storages = db.relationship('Storage',
                               back_populates='box')

    def __init__(self, id, stage_id):
        self.id = id
        self.stage_id = stage_id

    def __repr__(self):
        return(f"Box('{self.id}') on stage {self.stage_id}")


class Storage(db.Model):
    __tablename__ = "storage"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    box_id = db.Column(db.Integer,
                       db.ForeignKey('box.id'))
    box = db.relationship('Box',
                          back_populates='storages')

    checkin_id = db.Column(db.Integer,
                           db.ForeignKey('checkin.id'),
                           nullable=False)
    checkin = db.relationship('CheckIn',
                              back_populates='storage')

    time_in = db.Column(db.DateTime, nullable=False)
    time_out = db.Column(db.DateTime, nullable=True)

    def __init__(self, box_id):
        self.box_id = box_id

    def __repr__(self):
        return (f"Storage('{self.box_id}')")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(20), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return (f"User('{self.username}')")
