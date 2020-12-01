from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from app.models import User

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=8, max=40)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign Up')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('That username is already taken. Please choose a different one.')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('That email is already taken. Please choose a different one.')

class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=8, max=40)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
  submit = SubmitField('Update')

  def validate_username(self, username):
    if username.data != current_user.username:
      user = User.query.filter_by(username=username.data).first()
      if user:
        raise ValidationError('That username is already taken. Please choose a different one.')

  def validate_email(self, email):
    if email.data != current_user.email:
      user = User.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError('That email is already taken. Please choose a different one.')

class NewHireForm(FlaskForm):
  first_name = StringField('First Name', validators=[DataRequired()])
  last_name = StringField('Last Name', validators=[DataRequired()])
  position = StringField('Position', validators=[DataRequired()])
  pay_rate = FloatField('Pay Rate', validators=[DataRequired()])
  hire_date = DateField('Hire Date', format='%m/%d/%Y', validators=[DataRequired()])
  start_date = DateField('Start Date', format='%m/%d/%Y', validators=[DataRequired()])
  wisely_no = IntegerField('Wisely Number', validators=[DataRequired()])
  submit = SubmitField('Submit')

class NewHireFilterForm(FlaskForm):
  from_date = DateField('From Date', format='%m/%d/%Y')
  to_date =  DateField('To Date', format='%m/%d/%Y')
  submit = SubmitField('Filter')

class PettyCashForm(FlaskForm):
  date = DateField('Date', format='%m/%d/%Y', validators=[DataRequired()])
  receipt_no = IntegerField('Receipt Number', validators=[DataRequired()])
  description = StringField('Description', validators=[DataRequired(), Length(min=5, max=40)])
  amount_deposited = FloatField('Amount Deposited', validators=[Optional()])
  amount_withdrawn = FloatField('Amount Withdrawn', validators=[Optional()])
  received_by = StringField('Received By', validators=[DataRequired()])
  approved_by = StringField('Approved By', validators=[DataRequired()])
  comments = StringField('Comments')
  receipt = FileField('Upload Receipt', validators=[FileAllowed(['pdf', 'jpg', 'png'])])
  submit = SubmitField('Submit')

class PettyCashFilterForm(FlaskForm):
  from_date = DateField('From Date', format='%m/%d/%Y')
  to_date =  DateField('To Date', format='%m/%d/%Y')
  submit = SubmitField('Filter')