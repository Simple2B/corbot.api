from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField


class TestingForm(FlaskForm):

    RegNumber = StringField('reg_number')
    Subject = StringField('Subject')
    Body = TextAreaField('Body')
    Submit = SubmitField('Submit')
