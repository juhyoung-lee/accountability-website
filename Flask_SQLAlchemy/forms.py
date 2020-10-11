from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

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
            beer_sel = SelectField('Beer Name', choices=[(bn,bn) for bn in beer_names])
            submit = SubmitField('Submit')
        return F()