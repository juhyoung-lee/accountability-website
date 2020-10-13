from datetime import datetime
import forms
import models

from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy


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


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/registration.html', methods=['POST', 'GET'])
def registration():
    return render_template('registration.html')


@app.route('/view-client.html')
def view_client():
    return render_template('view-client.html')

@app.route("/temp.html", methods=["POST", "GET"])
def temp():
    if request.method == "POST":
	    user = request.form["nm"]
	    return redirect(url_for("view_goal", usr=user))
    else:
	    return render_template("temp.html")

#@app.route("/<usr>")
#def user(usr):
 #   return f"<h1>{usr}</h1>"


#@app.route("/<usr>")
#def view_goal(usr):
#    return render_template('view-goal.html',content=usr)


@app.route('/<usr>')
def view_goal(usr):
    results = db.session.query(models.Goal) \
                        .filter(models.Goal.email_id == usr).all()
    return render_template('view-goal.html', usr=usr, data=results)



@app.route('/edit-goal.html')
def edit_goal():
    return render_template('edit-goal.html')


@app.route('/edit-client.html')
def edit_client1():
    return render_template('edit-client.html')


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
