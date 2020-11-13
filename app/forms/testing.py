from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField


class TestingForm(FlaskForm):

    Method = StringField('Method')
    Data = TextAreaField('Data')
    Submit = SubmitField('Submit')
