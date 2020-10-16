from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, TextField
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, AnyOf, NumberRange, EqualTo, DataRequired


class ClientEditForm:
    @staticmethod
    def form(client, phone_number, timezone, year, major_minor, classes,
             partner_request, priorities, aim):
        class F(FlaskForm):
            phone_number = IntegerField(default=Client.phone_number)
            timezone = IntegerField(default=Client.timezone)
            year = IntegerField(default=Client.year)
            major_minor = StringField(default=Client.major_minor)
            classes = StringField(default=Client.classes)
            partner_request = StringField(default=Client.partner_request)
            priorities = StringField(default=Client.priorities)
            aim = StringField(default=Client.aim)

        return F()


class ServingsFormFactory:
    @staticmethod
    def form(beer_names):
        class F(FlaskForm):
            beer_sel = SelectField('Beer Name', choices=[
                                   (bn, bn) for bn in beer_names])
            submit = SubmitField('Submit')
        return F()


class AddClientForm(FlaskForm):
    email_id = StringField(
        'email', [DataRequired(), Regexp(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', message='Valid email required')])
    password = StringField('password', [DataRequired(), EqualTo(
        'password_rpt', message='Passwords must match')])
    password_rpt = StringField('password repeat', [DataRequired()])
    name = StringField('name', [DataRequired()])
    phone_number = IntegerField('phone_number', [DataRequired(), NumberRange(
        min=0000000000, max=9999999999, message='########## format required')])
    timezone = IntegerField(
        'timezone', [DataRequired(), NumberRange(min=0, max=23)])
    year = IntegerField('year', [DataRequired(), NumberRange(
        min=-11, max=12, message='Chose UTC time from -11 to 12')])
    major_minor = StringField('major_minor', [DataRequired()])
    classes = StringField('classes', [DataRequired()])
    partner_request = StringField('partner_request')
    priorities = StringField('priorities', [DataRequired()])
    aim = StringField('aim', [DataRequired()])
    submit = SubmitField('register')
