from sqlalchemy import sql, orm
from app import db
from faker import Faker

fake = Faker()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    location = db.Column(db.String(50))
    age = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.now)

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, primary_key=True) #db.ForeignKey('user.email_id') when user table is created
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_completed = db.Column(db.DateTime)
    progress = db.Column(db.Integer, nullable=False)
    @staticmethod
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

class Milestone(db.Model):
    Milestone_ID = db.Column(db.String(100), primary_key=True) 
    Goal_ID = db.Column(db.String(100), primary_key=True) 
    Email_ID = db.Column(db.String(100), primary_key=True) 
    Name = db.Column(db.String(50), nullable=False)
    Deadline = db.Column(db.DateTime)
    Date_Completed = db.Column(db.DateTime)