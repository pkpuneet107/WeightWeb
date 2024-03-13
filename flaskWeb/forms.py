from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flaskWeb.models import User


class RegistrationForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
            

class UserDataForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min = 0)])
    height = IntegerField('Height', validators=[DataRequired()])
    sex = SelectField('Sex', validators=[DataRequired()], choices = [('Male', 'Male'), ('Female', 'Female')])
    activity_level = SelectField('Activity Level', validators=[DataRequired()], choices = [('1.2', 'Lazy (little or no exercise)'),
                                            ('1.375', 'Lightly active (light exercise/sports 1-3 days a week)'),
                                            ('1.55', 'Moderately active (moderate exercise/sports 3-5 days a week)'),
                                            ('1.725', 'Very active (hard exercise/sports 6-7 days a week)'),
                                            ('1.9', 'Extra active (very hard exercise/sports & physical job or 2x training)')])
    current_weight = FloatField('Current Weight', validators=[DataRequired()])
    goal_weight = FloatField('Goal Weight', validators=[DataRequired()])
    submit = SubmitField('Update')
        