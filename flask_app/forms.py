from ast import Pass
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, RadioField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)


from .models import User


class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")


class RecipeReviewForm(FlaskForm):
    text = TextAreaField(
        "Comment:", validators=[InputRequired(), Length(min=5, max=500)]
    )
    rating = RadioField('Rating', choices=[(1, '★'), (2, '★★'), (3, '★★★'), (4, '★★★★'), (5, '★★★★★')], coerce=int, validators=[InputRequired()])
    submit = SubmitField("Enter Comment")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=3, max=25)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=3, max=25)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


# TODO: implement fields
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=3, max=25)])
    submit = SubmitField('Login')


# TODO: implement
class UpdateUsernameForm(FlaskForm):
    username = StringField('New Username', validators=[InputRequired(), Length(min=3, max=25)])
    submit_username = SubmitField('Update Username')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')

class UpdateProfilePicForm(FlaskForm):
    picture = FileField('New Profile Picture', validators=[FileAllowed(['jpg', 'png'], 'Images Only!')])
    submit_picture = SubmitField('Update Picture')
