from sqlalchemy import sql, orm
from app import db
from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class User(db.Model):
    email_id = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.now)


class Client(db.Model):
    email_id = db.Column(db.String(100), db.ForeignKey(
        'user.email_id'), primary_key=True)
    phone_number = db.Column(db.Integer)
    timezone = db.Column(db.Integer)
    year = db.Column(db.Integer)
    major_minor = db.Column(db.String(100))
    classes = db.Column(db.String(100))
    partner_request = db.Column(db.String(100))
    priorities = db.Column(db.String(500))
    aim = db.Column(db.String(500))

    goals = db.relationship('Goal', backref='client')


class Goal(db.Model):
    goal_id = db.Column(db.String(100), primary_key=True)
    email_id = db.Column(db.String(100), db.ForeignKey(
        'client.email_id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_completed = db.Column(db.DateTime)
    progress = db.Column(db.Integer, default=0)

    milestones = db.relationship('Milestone', backref='goal')


class Milestone(db.Model):
    Milestone_ID = db.Column(db.Integer, primary_key=True)
    Goal_ID = db.Column(db.String(100), db.ForeignKey(
        'goal.goal_id'), primary_key=True)
    Email_ID = db.Column(db.String(100), db.ForeignKey(
        'client.email_id'), primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Deadline = db.Column(db.DateTime)
    Date_Completed = db.Column(db.DateTime)
