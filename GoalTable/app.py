  
from datetime import datetime
import random
import string
from faker import Faker
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

fake = Faker()

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, primary_key=True) #db.ForeignKey('user.email_id') when user table is created
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_completed = db.Column(db.DateTime)
    progress = db.Column(db.Integer, nullable=False)

def add_goal(name, email_id):
  letters = string.ascii_lowercase
  goal = Goal(
    goal_id = ''.join(random.choice(letters) for i in range(8)),
    email_id = fake.email(),
    name = fake.first_name(),
    progress = 0
  )
  db.session.add(goal)
  db.session.commit()

def add_fake_goals():
  db.create_all()
  for _ in range(100):
    add_goal(fake.sentence(), fake.email())


