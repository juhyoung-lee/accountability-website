from datetime import datetime, timedelta
from faker import Faker
import random
import string

fake = Faker()


from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
#db.init_app(app)

def add_milestones():
    letters = string.ascii_lowercase
    for _ in range(100):
        milestone = Milestone(
            Milestone_ID = ''.join(random.choice(letters) for i in range(8)),
            Goal_ID = ''.join(random.choice(letters) for i in range(10)),
            Email_ID = fake.email(),
            Name = fake.first_name(),
            Deadline = fake.date_time_this_year(),
            Date_Completed = fake.date_time_this_year()
        )
        db.session.add(milestone)
    db.session.commit()

def create_random_data():
    db.create_all()
    add_milestones()

