from sqlalchemy import sql, orm
from app import db
from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import string
import random


class User(db.Model):
    email_id = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, email_id, password, name):
        self.email_id = email_id
        self.password = password
        self.name = name


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
    matched = db.Column(db.Integer)
    goals = db.relationship('Goal', backref='client')

    def __init__(self, email, phone, time, year, major, classes, partner, prio, aim, matched):
        self.email_id = email
        self.phone_number = phone
        self.timezone = time
        self.year = year
        self.major_minor = major
        self.classes = classes
        self.partner_request = partner
        self.priorities = prio
        self.aim = aim
        self.matched = matched


class Goal(db.Model):
    goal_id = db.Column(db.String(100), primary_key=True)
    email_id = db.Column(db.String(100), db.ForeignKey(
        'client.email_id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.Date, default=datetime.now().date())
    deadline = db.Column(db.Date)
    date_completed = db.Column(db.Date)
    progress = db.Column(db.Integer, default=0)
    milestones = db.relationship('Milestone', backref='goal')

    def __hash__(self):
        return hash(self)

    def __init__(self, email, name, date_created, deadline):
        self.goal_id = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10))
        self.email_id = email
        self.name = name
        self.date_created = date_created
        self.deadline = datetime.strptime(str(deadline), '%Y-%m-%d')


class Milestone(db.Model):
    Milestone_ID = db.Column(db.Integer, primary_key=True)
    Goal_ID = db.Column(db.String(100), db.ForeignKey(
        'goal.goal_id'), primary_key=True)
    Email_ID = db.Column(db.String(100), db.ForeignKey(
        'client.email_id'), primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Deadline = db.Column(db.DateTime)
    Completed = db.Column(db.Integer)
    Date_Completed = db.Column(db.DateTime)

    def __init__(self, milestone_id, goal_id, email_id, name, deadline, completed, date_completed):
        self.Milestone_ID = milestone_id
        self.Goal_ID = goal_id
        self.Email_ID = email_id
        self.Name = name
        self.Deadline = deadline
        self.Completed = completed
        self.Date_Completed = date_completed
