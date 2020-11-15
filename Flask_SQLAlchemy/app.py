import sys
# from models import *
# import models
from datetime import datetime, timedelta
import forms
from flask import Flask, redirect, render_template, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy

# from forms import GoalEditForm
sys.path.append(".")


app = Flask(__name__)
app.secret_key = 'sudeepa'

app.permanent_session_lifetime = timedelta(days=3)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['WTF_CSRF_ENABLED'] = False

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
        person = db.session.query(models.User).filter(
            models.User.email_id == email).first()
        if person != None and person.password == psw:
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
    form = forms.AddClientForm()
    if form.validate_on_submit():
        email_id = request.form['email_id']
        password = request.form['password']
        password_rpt = request.form['password_rpt']
        name = request.form['name']
        phone_number = request.form['phone_number']
        timezone = request.form['timezone']
        year = request.form['year']
        major_minor = request.form['major_minor']
        classes = request.form['classes']
        partner_request = request.form['partner_request']
        priorities = request.form['priorities']
        aim = request.form['aim']
        user = models.User(email_id, password, name)
        db.session.add(user)
        client = models.Client(email_id, phone_number, timezone, year,
                               major_minor, classes, partner_request, priorities, aim)
        db.session.add(client)
        db.session.commit()
        session['email'] = email_id
        return redirect(url_for('view_goal'))
    else:
        error = form.errors.items()
        flash(f'{error}')
        print(error)
        return render_template('registration.html')


@app.route('/admin')
def admin():
    unmatched = db.session.query(models.Client) \
        .filter(models.Client.matched==0).\
    limit(5).from_self()
    matched = db.session.query(models.Client) \
        .filter(models.Client.matched==1).\
    limit(5).from_self()
    return render_template('admin.html', unmatched=unmatched, matched=matched)
    # return render_template('admin.html')

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


@app.route('/delete-goal/<id>', methods=['POST', 'GET'])
def delete_goal(id):
    while db.session.query(Milestone).filter_by(Goal_ID=id).first() != None:
        ms = db.session.query(Milestone).filter_by(Goal_ID=id).first()
        db.session.delete(ms)
    goal = db.session.query(Goal).filter_by(goal_id=id).first()
    db.session.delete(goal)
    db.session.commit()
    return redirect(url_for('view_goal'))


@app.route('/add-goal', methods=['POST', 'GET'])
def add_goal():
    form = forms.AddGoalForm()
    if form.validate_on_submit():
        email = session['email']
        name = request.form['name']
        deadline = request.form['deadline']
        if deadline == '':
            deadline = None
        goal = models.Goal(email, name, deadline)
        db.session.add(goal)
        db.session.commit()
        return redirect(url_for('view_goal'))
    else:
        error = form.errors.items()
        print(error)
        return render_template('add-goal.html')


@app.route('/view-partner-goal')
def view_partner_goal():
    usr = 'dorseyandrew@smith-clarke.biz'  # hardcoded partner for now
    goal_results = db.session.query(models.Goal) \
        .filter(models.Goal.email_id == usr).all()
    milestone_results = db.session.query(models.Milestone) \
        .filter(models.Milestone.Email_ID == usr).all()

    return render_template('view-partner-goal.html', usr=usr, goal_data=goal_results, milestone_data=milestone_results)


@app.route('/edit-goal/<id>', methods=['GET', 'POST'])
def edit_goal(id):
    # if form.validate_on_submit():
    #     return redirect(url_for('success')) ## change this to appropriate url
    goal = Goal.query.filter_by(goal_id=id).first_or_404()
    return render_template('edit-goal.html', goal=goal)
    # except con.Error as err: # if error
    # then display the error in 'database_error.html' page
    # return render_template('database_error.html', error=err)


@app.route('/submit-goal/<id>', methods=['POST'])
def submit_goal(id):
    goal = Goal.query.filter_by(goal_id=id).first_or_404()
    goal.name = request.form['name']
    goal.progress = request.form['progress']
    goal.deadline = request.form['deadline']
    db.session.merge(goal)
    db.session.commit()
    return redirect('/view-goal')


@ app.route('/edit-client')
def edit_client1():
    usr = session['email']
    user = db.session.query(models.Client) \
        .filter(models.Client.email_id == usr).one()
    return render_template('edit-client.html', Client=user)


@ app.route('/edit-client/<e_id>', methods=['GET', 'POST'])
def edit_client(e_id):
    '''
    client = db.session.query(models.Client).filter(
        models.Client.email_id == e_id).first()
    phone_number = db.session.query(client.phone_number).first()
    timezone = db.session.query(client.timezone).first()
    year = db.session.query(client.year).first()
    major_minor = db.session.query(client.major_minor).first()
    classes = db.session.query(client.classes).first()
    partner_request = db.session.query(client.partner_request).first()
    priorities = db.session.query(client.priorities).first()
    aim = db.session.query(client.aim).first()

    #form = forms.ClientEditForm(client, phone_number, timezone, year, major_minor, classes,
                                #partner_request, priorities, aim)

    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.Client.edit(email_id, form.phone_number.data, form.timezone.data,
                                form.year.data, form.major_minor.data, form.classes.data,
                                form.partner_request.data, form.priorities.data, form.aim.data)
            return redirect(url_for('clientdisplay', email_id=form.email_id.data))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('edit-client.html', Client=client, form=form)
    else:
        return render_template('edit-client.html', Client=client, form=form)
    '''
    client = Client.query.filter_by(email_id=e_id).first_or_404()
    # form = forms.ClientEditForm(client, phone_number, timezone, year, major_minor, classes,
    # partner_request, priorities, aim)
    client.phone_number = request.form['phone_number']
    client.timezone = request.form['timezone']
    client.year = request.form['year']
    client.major_minor = request.form['major_minor']
    client.classes = request.form['classes']
    client.partner_request = request.form['partner_request']
    client.priorities = request.form['priorities']
    client.aim = request.form['aim']
    db.session.merge(client)
    db.session.commit()
    print('committed')
    return redirect('/view-client')  # redirect to view-goal


def create_pairings():
    a = [] 
    unmatched = db.session.query(models.Client) \
        .filter(models.Client.matched==0, models.Client.partner_request != None ).all()
    num_unmatched = len(unmatched)
    for i in range(num_unmatched):
        for j in range(num_unmatched):
            if unmatched[i].partner_request == unmatched[j].email_id and unmatched[j].email_id == unmatched[i].partner_request and unmatched[j].email_id != unmatched[i].email_id and [unmatched[j].email_id, unmatched[i].email_id] not in a:
                #unmatched[j].matched = 1
                #unmatched[i].matched = 1
                #unmatched[i].partner = unmatched[j].email_id
               # unmatched[j].partner = unmatched[i].email_id
                a.append([unmatched[i].email_id, unmatched[j].email_id])
               # db.session.merge(unmatched[i])
               # db.session.merge(unmatched[j])
    #db.session.commit()
    return a


if __name__ == '__main__':
    app.run(debug=True)



  
            # add the pair of email IDs to the pairinglist.
    # match based on partner request
    # create list of tuples that i can add to
    # Look at client database
    # if partner request is 0, unmatched
    # check if partner request is equal to another person, and if that person's partner request is equal to original
    # add to pairing output, do not output duplicates



