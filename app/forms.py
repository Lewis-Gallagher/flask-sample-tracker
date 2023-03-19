from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, ValidationError, DateField, SelectField
from wtforms.validators import DataRequired, EqualTo
from app.models import User
import re
from datetime import datetime


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField(
        label='Username', 
        validators=[DataRequired()]
        )
    email = EmailField(
        label='Email', 
        validators=[DataRequired()]
        )
    password = PasswordField(
        label='Password', 
        validators=[DataRequired()]
        )
    password_repeat = PasswordField(
        label='Repeat Password', 
        validators=[DataRequired(), EqualTo('password', message="Passwords do not match. Please retry.")]
        )
    submit = SubmitField(
        label='Register'
        )

    def validate_username(self, username: str) -> bool:
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("That username is already in use.")
        
    def validate_email(self, email: str) -> bool:
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("That emamil address is already in use.")
        
        if not email.data.endswith('@icr.ac.uk'):
            raise ValidationError("Please register with a valid @icr.ac.uk email address.")
        

class SampleInputForm(FlaskForm):

    project = SelectField(
        label='Project ID',
        choices=['Project A', 'Project B', 'Project C'], 
        validators=[DataRequired()]
        )
    sample_name = StringField(
        label='Sample Name', 
        validators=[DataRequired()]
        )
    date = DateField(
        label='Date',
        validators=[DataRequired()],
        default = datetime.today()
        )
    submit = SubmitField(
        label='Submit'
        )


    def validate_sample_name(self, sample_name: str):
        special_chars = re.findall('\W', sample_name.data)
        if special_chars:
            raise ValidationError(f"Are you stupid? Don't use these: {special_chars}")
        

class ProjectInputForm(FlaskForm):

    project_name = StringField(
        label='Project identifier', 
        validators=[DataRequired()]
        )
    date = DateField(
        label='Date created',
        validators=[DataRequired()],
        default = datetime.today(),
        render_kw={'disabled':''}
        )
    submit = SubmitField(
        label='Submit'
        )