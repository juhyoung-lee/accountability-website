from sqlalchemy import sql, orm
from app import db
from models import User, Goal, Milestone, Client

import random
import string
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()


def add_users():
    for _ in range(10):
        user = User(
            email_id=fake.email(),
            password='passwd',
            name=fake.name()
        )
        db.session.add(user)
    db.session.commit()


def add_clients():
    users = User.query.all()
    letters = string.ascii_lowercase
    for user in users:
        client = Client(
            email=user.email_id,
            phone=random.randint(10000000000, 99999999999),
            # choose one of the one-hour time zone randomly
            time=random.randint(0, 23),
            year=random.randint(2021, 2024),  # or can be a bigger range
            major=''.join(random.choice(letters) for _ in range(30)),
            classes=''.join(random.choice(letters) for _ in range(50)),
            partner=fake.name(),
            prio=fake.sentence(),
            aim=fake.sentence(),
            matched=random.randint(0, 1)
        )
        db.session.add(client)
    db.session.commit()


def add_goals():
    letters = string.ascii_lowercase
    clients = Client.query.all()
    for client in clients:
        for num in range(random.randint(0, 6)):
            date=fake.date_this_year()
            goal = Goal(
                email=client.email_id,
                name=fake.color_name(),
                date_created=date,
                deadline=fake.date_between(start_date=date)
            )
            db.session.add(goal)
    db.session.commit()


def add_milestones():
    letters = string.ascii_lowercase
    clients = Client.query.all()
    for client in clients:
        for goal in client.goals:
            for num in range(random.randint(0, 3)):
                milestone = Milestone(
                    milestone_id=num,
                    goal_id=goal.goal_id,
                    email_id=client.email_id,
                    name=''.join(random.choice(letters) for i in range(8)),
                    deadline=fake.date_time_this_year(),
                    completed=random.randint(0,1),
                    date_completed=fake.date_time_this_year()
                )   
                db.session.add(milestone)
    db.session.commit()


def add_fake_data():
    db.create_all()
    add_users()
    add_clients()
    add_goals()
    add_milestones()
