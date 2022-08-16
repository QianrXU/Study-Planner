""" 

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

THE BELOW NEEDS TO BE REVISED BUT I THINK THIS IS A 
GOOD STARTING PLACE FOR DEVELLOPING THE LOGIN AND 
REGISTRATION FORMS ////CHRISTINE



# login form on the login page
class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign in')

# form to register the user
class RegistrationForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired(),Length(min=4, max=20)])
  # repeat password for validation
  password2 = PasswordField(
    'Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')
  
  # confirm that the email address is not already in use
  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
      raise ValidationError('Please use a different email address.')
      
""" 