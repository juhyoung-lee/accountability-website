from sqlalchemy import sql, orm
from app import db
from models import User, Goal, Milestone, Client

import random
import string
from datetime import datetime, timedelta, date
from faker import Faker

fake = Faker()


def add_users():
    emails = set()
    for i in range(5000):
        fake_email = fake.email()
        curr_len = len(emails)
        emails.add(fake_email)
        while curr_len == len(emails):
            fake_email = fake.email()
            emails.add(fake_email)

        user = User(
            email_id=fake_email,
            password='passwd',
            name=fake.name(),
            admin=0
        )
        db.session.add(user)
    db.session.commit()


def add_clients():
    users = User.query.all()
    letters = string.ascii_lowercase
    majors = ['AAAS', 'AMES', 'ARTHIST', 'BIOLOGY', 'BME', 'CEE', 'CHEM', 'CHINESE', 'CLST', 'COMPSCI', 'CULANTH', 'DANCE', 'ECE', 'ECON', 'ENGLISH', 'ENVIRON', 'EVANTH', 'FRENCH', 'GERMAN', 'GLHLTH', 'GREEK', 'GSF', 'HISTORY',
              'ITALIAN', 'ICS', 'LIT', 'LINGUIST', 'MATH', 'ME', 'MUSIC', 'MEDREN', 'NEUROSCI', 'PHIL', 'PHYSICS', 'POLSCI', 'PSY', 'PUBPOL', 'ROMST', 'RELIGION', 'RUSSIAN', 'SCIOL', 'SPANISH', 'STA', 'SES', 'THEATRST', 'VMS', 'WRITING']
    classes = [101, 102, 109, 111, 112, 134, 140, 146, 163, 171, 182, 190, 203, 204, 207, 209, 210, 211, 212, 213, 215,
               221, 222, 231, 246, 250, 261, 290, 301, 303, 305, 307, 308, 310, 316, 320, 329, 330, 334, 345, 356, 390, 490]
    priorities = ['grades', 'self care', 'personal projects', 'recruiting', 'hobbies',
                  'research', 'exercise', 'organizations', 'volunteering', 'being premed', 'making friends']
    for user in users:
        major = random.choice(majors)
        class_set = major + ' ' + str(random.choice(classes))
        for i in range(random.randint(1, 4)):
            rand_class = random.choice(classes)
            while str(rand_class) in class_set:
                rand_class = random.choice(classes)
            class_set = class_set + ', ' + major + ' ' + str(rand_class)
        client = Client(
            email=user.email_id,
            phone=random.randint(1000000000, 99999999999),
            # choose one of the UTC relative time zones
            time=random.randint(-12, 14),
            year=random.randint(2021, 2024),  # or can be a bigger range
            major=major,
            classes=class_set,
            partner_req='',
            partner='',
            prio=random.choice(priorities),
            matched=0
        )
        db.session.add(client)
    db.session.commit()


def match_clients():
    clients = Client.query.all()
    num_clients = len(clients)
    for i in range(num_clients//10*2):
        client = clients[-1]
        clients.pop()
        partner = random.choice(clients)
        clients.remove(partner)
        client.matched = 1
        partner.matched = 1
        client.partner_request = partner.email_id
        client.partner = partner.email_id
        partner.partner_request = client.email_id
        partner.partner = client.email_id
        db.session.merge(client)
        db.session.merge(partner)
    for i in range(num_clients//10*2):
        client = clients[-1]
        clients.pop()
        partner = random.choice(clients)
        clients.remove(partner)
        client.partner_request = partner.email_id
        partner.partner_request = client.email_id
        db.session.merge(client)
        db.session.merge(partner)
    db.session.commit()


def add_goals():
    clients = Client.query.all()
    goal_names = ['Problem set', 'Essay reflection', 'Midterm', 'Applications', 'Presentation', 'Call a friend', 'Go to the gym', 'Plan event', 'Watch movie', 'Watch lecture', 'Quiz', 'Read chapter', 'Find airpod', 'Drink water',
                  'Go on a run', 'Interview prep', 'MCAT', 'Lab', 'Lab report', 'Clean my room', 'Call parents', 'Call grandparents', 'Journal', 'Clean email inbox', 'Event planning', 'GRE', 'Bookbag', 'Take vitamins', 'Buy birthday gift']
    for client in clients:
        goal_count = random.randint(2, 6)
        goal_set = random.sample(goal_names, goal_count)
        for num in range(goal_count):
            date = (datetime.strptime('2020-9-1', '%Y-%m-%d') +
                    timedelta(days=random.randint(0, 75))).date()
            goal = Goal(
                email=client.email_id,
                name=goal_set.pop(),
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
            iter = random.randint(0, 3)
            start = goal.date_created
            end = goal.deadline
            delta = (end - start).days // iter
            for num in range(iter):
                deadline = start + \
                    timedelta(days=(iter*num+random.randint(0, iter)))
                milestone = Milestone(
                    milestone_id=num,
                    goal_id=goal.goal_id,
                    email_id=client.email_id,
                    name='Step '+str(num+1),
                    deadline=deadline,
                    date_completed=fake.date_between_dates(
                        date_start=start, date_end=deadline)
                )
                db.session.add(milestone)
    db.session.commit()


def add_admin():
    user = User(
        email_id='admin@gmail.com',
        password='passwd',
        name='admin',
        admin=1
    )
    db.session.add(user)

    admin = Client(
        email='admin@gmail.com',
        phone=1234567890,
        time=0,
        year=2022,
        major='COMPSCI',
        classes='COMPSCI 316, COMPSCI 201, COMPSCI 250, COMPSCI 330',
        partner_req='',
        partner='',
        prio='self care',
        matched=1
    )
    db.session.add(admin)

    goal = Goal(
        email='admin@gmail.com',
        name='Pass CS 316',
        date_created=datetime.now().date(),
        deadline=date.fromisoformat('2020-11-17')
    )
    db.session.add(goal)

    db.session.commit()


def add_fake_data():
    db.create_all()
    add_users()
    print('added users')
    add_clients()
    print('added clients')
    match_clients()
    print('matched clients')
    add_goals()
    print('added goals')
    add_milestones()
    print('added milestones')
    add_admin()
    print('added admin')
