#Client_table  
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

class Client(db.Model):
    email_id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.Integer)
    timezone = db.Column(db.Integer)
    year = db.Column(db.Integer)
    major_minor = db.Column(db.String(200))
    classes = db.Column(db.String(500))
    partner_request = db.Column(db.String(50))
    priorities = db.Column(db.String(500))
    aim = db.Column(db.String(500))

def add_client():
  letters = string.ascii_lowercase
  client = Client(
    email_id = fake.email(),
    phone_number = randome.randint(10000000000, 99999999999),
    timezone = random.randint(0, 23), #choose one of the one-hour time zone randomly
    year = random.randint(2021,2024), #or can be a bigger range
    major_minor = join(random.choice(letters) for _ in range(30)),
    classes = join(random.choice(letters) for _ in range(50)),
    partner_request = fake.name,
    priorities = join(random.choice(letters) for _ in range(100)),
    aim = join(random.choice(letters) for _ in range(100)),
  )
  db.session.add(client)
  db.session.commit()

def add_fake_clients():
  db.create_all()
  for _ in range(100):
    add_client()


