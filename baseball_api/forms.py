from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


# This is the form for the Sign In and Sign Up pahes
class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()
    

# This is the form for inputting players to find their stats
class Player(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    season = StringField('Season', validators=[DataRequired()])
    submit_button = SubmitField()

