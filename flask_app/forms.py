from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, IntegerField
from wtforms.fields.simple import SubmitField
from wtforms.validators import InputRequired, Length, NumberRange, ValidationError, Email, EqualTo
import re
from .models import User

class SearchForm(FlaskForm):
    search_query = StringField("Name:", validators=[InputRequired(), Length(min=1, max = 30)])
    submit = SubmitField("Submit")


#This form lets the user review a landlord from the homepage
class ProfessorReviewForm(FlaskForm):
    try:
        name = StringField("Enter Your Name, or type \"Anonymous\": ", validators=[InputRequired(), Length(min=1, max = 50)])
        ProfessorName = StringField("Enter Your Landlord's Name:", validators=[InputRequired(), Length(min=1, max = 50)])
        course = StringField("Enter The Class You Took:", validators=[InputRequired(), Length(min=1, max = 100)])
        landlordReview = TextAreaField("How Was Your Professor? Write a detailed review below", validators=[InputRequired(), Length(min=1, max = 500)])
        rating = IntegerField("Give Them A Rating (1-5)", validators = [NumberRange(min=1, max=5)])
        submit = SubmitField("Submit")
    except ValidationError as err:
        err_msg = str(err)
        print(err_msg)

#This form lets the user rate a landlord from the landlord-specific-page
class CurrentProfessorReviewForm(FlaskForm):
    try:
        name = StringField("Enter Your Name:", validators=[InputRequired(), Length(min=1, max = 50)])
        course = StringField("Enter The Class You Took:", validators=[InputRequired(), Length(min=1, max = 100)])
        landlordReview = TextAreaField("How Was Your Landlord?", validators=[InputRequired(), Length(min=1, max = 500)])
        rating = IntegerField("Give Them A Rating (1-5)", validators = [NumberRange(min=1, max=5)])
        submit = SubmitField("Submit")
    except ValidationError as err:
        err_msg = str(err)
        print(err_msg)

class RegisterForm(FlaskForm):
    username = StringField("Enter a username:", validators=[InputRequired(), Length(min=1, max=32)])
    email = StringField("Enter your email:", validators=[InputRequired(), Email()])
    password = PasswordField("Enter a password:", validators=[InputRequired(), Length(min=5, max=32)])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Sign up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")
    
    def validate_password(self, password):
        upp_char = any(ele.isupper() for ele in password.data)
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        spec_char = regex.search(password.data) == None
        if (not upp_char) or spec_char:
            raise ValidationError("Password must contain an uppercase character and a special character")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")

class LoginForm(FlaskForm):
    username = StringField("Enter your username:", validators=[InputRequired(), Length(min=1, max=32)])
    password = PasswordField("Enter your password:", validators=[InputRequired()])
    submit = SubmitField("Login")

class UpdateUsernameForm(FlaskForm):
    username = StringField("Enter your new username:", validators=[InputRequired(), Length(min=1, max=32)])
    submit = SubmitField("Change Username")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

class UpdatePasswordForm(FlaskForm):
    password = PasswordField("Enter a new password:", validators=[InputRequired()])
