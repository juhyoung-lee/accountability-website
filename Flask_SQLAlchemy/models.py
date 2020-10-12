from sqlalchemy import sql, orm
from app import db
from datetime import datetime, timedelta


class User(db.Model):
    email_id = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(50))
    phone_number = db.Column(db.Integer)
    time_zone = db.Column(db.String(50))
    year = db.Column(db.Integer)
    major = db.Column(db.String(50))
    classes = db.Column(db.String(100))
    partner_request = db.Column(db.String(50))
    priorities = db.Column(db.String(50))
    aim = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.now)


class Client(db.Model):
    email_id = db.Column(db.String(100), primary_key=True)
    phone_number = db.Column(db.Integer)
    timezone = db.Column(db.Integer)
    year = db.Column(db.Integer)
    major_minor = db.Column(db.String(200))
    classes = db.Column(db.String(500))
    partner_request = db.Column(db.String(50))
    priorities = db.Column(db.String(500))
    aim = db.Column(db.String(500))


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    # db.ForeignKey('user.email_id') when user table is created
    # email_id = db.Column(db.Integer, db.ForeignKey(
    #     'user.email_id'), primary_key=True)
    email_id = db.Column(db.Integer)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_completed = db.Column(db.DateTime)
    progress = db.Column(db.Integer, nullable=False)


class Milestone(db.Model):
    Milestone_ID = db.Column(db.String(100), primary_key=True)
    Goal_ID = db.Column(db.String(100), primary_key=True)
    # Email_ID = db.Column(db.String(100), db.ForeignKey(
    #     'user.email_id'), primary_key=True)
    Email_ID = db.Column(db.String(100), primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Deadline = db.Column(db.DateTime)
    Date_Completed = db.Column(db.DateTime)
