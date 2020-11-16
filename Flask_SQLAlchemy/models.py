from sqlalchemy import sql, orm
from app import db
from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import string
import random


class User(db.Model):
    email_id = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, email_id, password, name, admin):
        self.email_id = email_id
        self.password = password
        self.name = name
        self.admin = admin


class Client(db.Model):
    email_id = db.Column(db.String(100), db.ForeignKey(
        'user.email_id'), primary_key=True)
    phone_number = db.Column(db.Integer, nullable=False)
    timezone = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    major_minor = db.Column(db.String(100), nullable=False)
    classes = db.Column(db.String(100), nullable=False)
    partner_request = db.Column(db.String(100), nullable=False)
    priorities = db.Column(db.String(500), nullable=False)
    matched = db.Column(db.Integer, nullable=False)
    goals = db.relationship('Goal', backref='client')

    def __init__(self, email, phone, time, year, major, classes, partner_req, prio, matched):
        self.email_id = email
        self.phone_number = phone
        self.timezone = time
        self.year = year
        self.major_minor = major
        self.classes = classes
        self.partner_request = partner_req
        self.priorities = prio
        self.matched = matched

class Goal(db.Model):
    goal_id = db.Column(db.String(100), primary_key=True)
    email_id = db.Column(db.String(100), db.ForeignKey(
        'client.email_id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    deadline = db.Column(db.Date)
    progress = db.Column(db.Integer)
    milestones = db.relationship('Milestone', backref='goal')

    def __init__(self, email, name, date_created, deadline):
        self.goal_id = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10))
        self.email_id = email
        self.name = name
        self.date_created = date_created
        # self.date_created = datetime.now().date()
        self.deadline = deadline
        # self.deadline = datetime.strptime(str(deadline), '%Y-%m-%d')
        self.progress = 0


class Milestone(db.Model):
    Milestone_ID = db.Column(db.Integer, primary_key=True)
    Goal_ID = db.Column(db.String(100), db.ForeignKey(
        'goal.goal_id'), primary_key=True)
    Email_ID = db.Column(db.String(100), db.ForeignKey(
        'client.email_id'), primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Deadline = db.Column(db.DateTime)
    Completed = db.Column(db.Integer, nullable=False)
    Date_Completed = db.Column(db.DateTime)

    def __init__(self, milestone_id, goal_id, email_id, name, deadline, date_completed):
        self.Milestone_ID = milestone_id
        self.Goal_ID = goal_id
        self.Email_ID = email_id
        self.Name = name
        self.Deadline = deadline
        self.Completed = 0
        self.Date_Completed = date_completed


class Pairing(db.Model):
    Date_formed = db.Column(db.DateTime, primary_key=True)
    Email_ID_User_1 = db.Column(db.String(100), db.ForeignKey(
        'client.email_id'), primary_key=True)
    Email_ID_User_2 = db.Column(db.String(100), db.ForeignKey(
        'client.email_id'), primary_key=True)
    Concluded = db.Column(db.Boolean)
    Confirmed = db.Column(db.Boolean)

    def __init__(Date_formed, Email_ID_User_1, Email_ID_User_2, Concluded, Confirmed):
            self.Date_formed = Date_formed
            self.Email_ID_User_1 = Email_ID_User_1
            self.Email_ID_User_2 = Email_ID_User_2
            self.Concluded = Concluded
            self.Confirmed = Confirmed