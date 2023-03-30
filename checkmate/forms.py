from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo

from werkzeug.security import check_password_hash

from checkmate.db import get_db
from scripts.timetable import create_timetable


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

    def validate_username(self, username):
        db = get_db()
        user = db.users.find_one({"username": username.data})
        if not user:
            raise ValidationError("Please check your username")

    def validate_password(self, password):
        db = get_db()
        user = db.users.find_one({"username": self.username.data})
        if user and not check_password_hash(user["password_hash"], password.data):
            raise ValidationError("Please check your password")


class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Re-Enter Password", validators=[DataRequired(), EqualTo("password")]
    )
    name = StringField("Name", validators=[DataRequired()])
    timetable = TextAreaField("Timetable", validators=[DataRequired()])
    bio = StringField("Bio")
    submit = SubmitField("Sign In")

    def validate_username(self, username):
        db = get_db()
        user = db.users.find_one({"username": username.data})
        if user:
            raise ValidationError("Please use a different username")

    def validate_email(self, email):
        db = get_db()
        user = db.users.find_one({"email": email.data})
        if user:
            raise ValidationError("Email already exists")

    def validate_timetable(self, timetable):
        try:
            create_timetable(timetable.data)
        except Exception:
            raise ValidationError("Please re-check your timetable format")


class UserSearch(FlaskForm):
    name = StringField("Name")
    submit = SubmitField("Submit")
