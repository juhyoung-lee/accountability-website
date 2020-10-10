from sqlalchemy import sql, orm
from app import db
from models import User, Goal, Milestone

import random
import string
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

def add_goal(name, email):
    letters = string.ascii_lowercase
    goal = Goal(
      goal_id = ''.join(random.choice(letters) for i in range(8)),
      email_id = email,
      name = name,
      progress = 0
    )
    db.session.add(goal)
    db.session.commit()

def add_fake_goals():
    db.create_all()
    for _ in range(100):
      add_goal(fake.sentence(), fake.email())

def add_fake_milestones():
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

def add_fake_data():
    db.create_all()
    add_fake_goals()
    add_fake_milestones()
