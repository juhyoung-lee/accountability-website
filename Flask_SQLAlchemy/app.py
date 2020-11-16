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


@app.route('/index')
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
    return redirect(url_for('login'))


@app.route('/', methods=['POST', 'GET'])
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
            if person.admin == 1:
                return redirect(url_for('admin'))
            return redirect(url_for('view_goal'))
        else:
            return redirect(url_for('login'))
    else:
        if 'email' in session:
            return redirect(url_for('view_goal'))
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
        user = models.User(email_id, password, name, admin=0)
        db.session.add(user)
        client = models.Client(email_id, phone_number, timezone, year,
                               major_minor, classes, partner_request, priorities, matched=0, partner='')
        db.session.add(client)
        db.session.commit()
        session['email'] = email_id
        return redirect(url_for('view_goal'))
    else:
        error = form.errors.items()
        flash(f'{error}')
        print(error)
        return render_template('registration.html')


def getUnmatchedClients():
    return db.session.query(models.Client) \
        .filter(models.Client.matched == 0).\
        limit(5).from_self()


def getMatchedClients():
    return db.session.query(models.Client) \
        .filter(models.Client.matched == 1).\
        limit(5).from_self()


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'email' in session:
        email = session['email']
        person = db.session.query(models.User).filter(
            models.User.email_id == email).first()
        if person.admin == 1:
            if request.method == 'POST':
                if "create-pairings" in request.form:
                    return render_template('admin.html', pairings=create_pairings(), unmatched=getUnmatchedClients(), matched=getMatchedClients())
                elif "reject-pairing" in request.form:
                    a = request.form['reject-pairing'][0]
                    pairing = request.form['reject-pairing'][1]
                    return render_template('admin.html', pairings=a, unmatched=getUnmatchedClients(), matched=getMatchedClients())
                elif "pair-users" in request.form:
                    pair = request.form['pair-users']
                    emails = pair.split()
                    print(emails)
                    client1 = db.session.query(Client).filter_by(
                        email_id=emails[0]).first()
                    client2 = db.session.query(Client).filter_by(
                        email_id=emails[1]).first()
                    client1.partner = emails[1]
                    client1.partner = emails[0]
                    client1.matched = 1
                    client2.matched = 1
                    db.session.commit()
            return render_template('admin.html', unmatched=getUnmatchedClients(), matched=getMatchedClients())
            # return render_template('admin.html')
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


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
        else:
            deadline = datetime.strptime(deadline, '%Y-%m-%d')
        goal = models.Goal(
            email, name, date_created=datetime.now().date(), deadline=deadline)
        db.session.add(goal)
        db.session.commit()
        return redirect(url_for('view_goal'))
    else:
        error = form.errors.items()
        print(error)
        return render_template('add-goal.html')


@app.route('/view-partner-goal')
def view_partner_goal():
    usr = session['email']
    user = db.session.query(models.Client) \
        .filter(models.Client.email_id == usr).one()
    if user.partner == '':
        return render_template('no-partner.html')

    partner = db.session.query(models.Client) \
        .filter(models.Client.email_id == user.partner_request).one()
    goal_results = db.session.query(models.Goal) \
        .filter(models.Goal.email_id == partner.email_id).all()
    milestone_results = db.session.query(models.Milestone) \
        .filter(models.Milestone.Email_ID == partner.email_id).all()
    return render_template('view-partner-goal.html', usr=usr, goal_data=goal_results, milestone_data=milestone_results, user=user, partner=partner)


@app.route('/edit-goal/<id>', methods=['GET', 'POST'])
def edit_goal(id):
    # if form.validate_on_submit():
    #     return redirect(url_for('success')) ## change this to appropriate url
    goal = Goal.query.filter_by(goal_id=id).first_or_404()
    milestones = Milestone.query.filter_by(Goal_ID=id).all()
    return render_template('edit-goal.html', goal=goal, milestones=milestones)
    # except con.Error as err: # if error
    # then display the error in 'database_error.html' page
    # return render_template('database_error.html', error=err)


@app.route('/submit-edit/<id>', methods=['POST'])
def submit_goal(id):
    goal = db.session.query(Goal).filter_by(goal_id=id).first()
    # goal = Goal.query.filter_by(goal_id=id).first_or_404()
    goal.name = request.form['name']
    goal.progress = request.form['progress']
    deadline = request.form['deadline']
    milestones = db.session.query(Milestone).filter_by(Goal_ID=id).all()
    for i in range(0, len(milestones)):
        if ('milestone-name' + str(i)) in request.form:
            print(request.form['milestone-name' + str(i)])
            milestones[i].Name = request.form['milestone-name' + str(i)]
        if ('milestone-deadline' + str(i)) in request.form:
            date = request.form['milestone-deadline' + str(i)]
            if date == '':
                date = None
            else:
                date = datetime.strptime(date, '%Y-%m-%d')
            milestones[i].Deadline = date
        if ('milestone-completed' + str(i)) in request.form:
            if request.form['milestone-completed' + str(i)] == None:
                milestones[i].Completed = 0
            else:
                milestones[i].Completed = 1
    if deadline == '':
        deadline = None
    else:
        deadline = datetime.strptime(deadline, '%Y-%m-%d')
    goal.deadline = deadline
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
    client = db.session.query(Client).filter_by(email_id=e_id).first()
    # client = Client.query.filter_by(email_id=e_id).first_or_404()
    # form = forms.ClientEditForm(client, phone_number, timezone, year, major_minor, classes,
    # partner_request, priorities, aim)
    client.phone_number = request.form['phone_number']
    client.timezone = request.form['timezone']
    client.year = request.form['year']
    client.major_minor = request.form['major_minor']
    client.classes = request.form['classes']
    client.partner_request = request.form['partner_request']
    client.priorities = request.form['priorities']
    db.session.commit()
    return redirect('/view-client')  # redirect to view-goal


def create_pairings():
    a = []
    unmatched = db.session.query(models.Client) \
        .filter(models.Client.matched == 0, models.Client.partner_request != None).all()
    num_unmatched = len(unmatched)
    for i in range(num_unmatched):
        for j in range(num_unmatched):
            if unmatched[i].partner_request == unmatched[j].email_id and unmatched[j].email_id == unmatched[i].partner_request and unmatched[j].email_id != unmatched[i].email_id and [unmatched[j].email_id, unmatched[i].email_id] not in a:
                #unmatched[j].matched = 1
                #unmatched[i].matched = 1
                #unmatched[i].partner = unmatched[j].email_id
                # unmatched[j].partner = unmatched[i].email_id
                b = []
                b.append(unmatched[i])
                b.append(unmatched[j])
                a.append(b)
                # db.session.merge(unmatched[i])
                # db.session.merge(unmatched[j])
    # db.session.commit()
    return a


@app.route('/search-client')
def search_client():
    return render_template('search-client.html')


@ app.route('/search-client', methods=['GET', 'POST'])
def search_client1():
    if request.form['phone_number'] != '':
        client = models.Client.query.filter_by(
            phone_number=request.form['phone_number']).all()
    if request.form['timezone'] != '':
        client = models.Client.query.filter_by(
            timezone=request.form['timezone']).all()
    if request.form['year'] != '':
        client = models.Client.query.filter_by(year=request.form['year']).all()
    if request.form['major_minor'] != '':
        client = models.Client.query.filter_by(
            major_minor=request.form['major_minor']).all()
    if request.form['classes'] != '':
        client = models.Client.query.filter_by(
            classes=request.form['classes']).all()
    if request.form['partner_request'] != '':
        client = models.Client.query.filter_by(
            partner_request=request.form['partner_request']).all()
    if request.form['priorities'] != '':
        client = models.Client.query.filter_by(
            priorities=request.form['priorities']).all()
    if request.form['aim'] != '':
        client = models.Client.query.filter_by(aim=request.form['aim']).all()
    # only print topic 20 clients on the display-search page
    if len(client) > 20:
        client = client[:20]
    # redirect to display-search
    return render_template('/display-search.html', c=client)


if __name__ == '__main__':
    app.run(debug=True)
