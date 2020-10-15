from datetime import datetime, timedelta
import forms
import models
from flask import Flask, redirect, render_template, url_for, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'sudeepa'
app.permanent_session_lifetime = timedelta(days=3)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/layout')
def layout():
    return render_template('layout.html')


@app.route('/loggedin')
def loggedin():
    if 'email' in session:
        email = session['email']
        return f'<h1>{email} logged in</h1>'
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email', None)
    return redirect(url_for('index'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['uname']
        psw = request.form['psw']
        # db.session.query(user)
        if models.User.query.filter_by(email_id=email, password=psw).first():
            session['email'] = email
            if request.form.get('remember') != None:
                session.permanent = True
            return redirect(url_for('loggedin'))
        else:
            return redirect(url_for('login'))

    else:
        if 'email' in session:
            return redirect(url_for('index'))
        return render_template('login.html')


@ app.route('/registration', methods=['POST', 'GET'])
def registration():
    return render_template('registration.html')


@ app.route('/view-client')
def view_client():
    usr = session['email']
    results = db.session.query(models.Client) \
                        .filter(models.Client.email_id == usr).one()
    return render_template('view-client.html', usr=usr, data=results)

@app.route('/view-goal')
def view_goal():
    usr = session['email']
    goal_results = db.session.query(models.Goal) \
                        .filter(models.Goal.email_id == usr).all()
    milestone_results = db.session.query(models.Milestone) \
                        .filter(models.Milestone.Email_ID == usr).all()
    return render_template('view-goal.html', usr=usr, goal_data=goal_results, milestone_data=milestone_results)

@ app.route('/edit-goal')
def edit_goal():
    return render_template('edit-goal.html')


@ app.route('/edit-client')
def edit_client1():
    return render_template('edit-client.html')


@ app.route('/edit-client/<email_id>', methods=['GET', 'POST'])
def edit_client(email_id):
    client = db.session.query(models.Client).filter(
        models.Client.email_id == email_id).one()
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
