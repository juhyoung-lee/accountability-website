
from datetime import datetime
import forms

from flask import Flask, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

from forms import GoalEditForm

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/layout.html')
def layout():
    return render_template('layout.html')


@app.route('/login.html')
def login():
    return render_template('login.html')


@app.route('/registration.html')
def registration():
    return render_template('registration.html')


@app.route('/view-client.html')
def view_client():
    return render_template('view-client.html')


@app.route('/view-goal.html')
def view_goal():
    return render_template('view-goal.html')


@app.route('/edit-goal.html')
def edit_goal():
    form = GoalEditForm()
    # if form.validate_on_submit():
    #     return redirect(url_for('success')) ## change this to appropriate url
    return render_template('edit-goal.html', form=form)


@app.route('/edit-client/<email_id>', methods=['GET', 'POST'])
def edit_client(email_id):
    client = db.session.query(models.Client)\
        .filter(models.Client.email_id == email_id).one()
    phone_number = db.session.query(client.phone_number).one()
    timezone = db.session.query(client.timezone).one()
    year = db.session.query(client.year).one()
    major_minor = db.session.query(client.major_minor).one()
    classes = db.session.query(client.classes).one()
    partner_request = db.session.query(client.partner_request).one()
    priorities = db.session.query(client.priorities).one()
    aim = db.session.query(client.aim).one()

    form = forms.ClientEditForm(client, phone_number, timezone, year, major_minor, classes,
                                partner_request, priorities, aim)

    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.Drinker.edit(email_id, form.phone_number.data, form.timezone.data,
                                form.year.data, form.major_minor.data, form.classes.data,
                                form.partner_request.data, form.priorities.data, form.aim.data)
            return redirect(url_for('clientdisplay', email_id=form.email_id.data))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('edit-client.html', Client=client, form=form)
    else:
        return render_template('edit-client.html', Client=client, form=form)


if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/<name>/<location>/<age>')
# def index(name, location):
#     user = User(name=name, location=location, age=age)
#     db.session.add(user)
#     db.session.commit()

#     return '<h1>Added New User!</h1>'


# @app.route('/<name>')
# def get_user(name):
#     user = User.query.filter_by(name=name).first()

#     return f'<h1>The user is located in: { user.location }</h1>'
