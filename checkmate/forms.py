from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo

from werkzeug.security import check_password_hash

from checkmate.db import get_db
from scripts.timetable import create_timetable


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()

    def validate_username(self, username):
        db = get_db()
        user = db.users.find_one({"username": username.data})
        if not user:
            raise ValidationError("username does not exist!")

    def validate_password(self, password):
        db = get_db()
        user = db.users.find_one({"username": self.username.data})
        if user and not check_password_hash(user["password_hash"], password.data):
            raise ValidationError("wrong password!")


class SignUpForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    re_password = PasswordField(validators=[DataRequired(), EqualTo("password")])
    name = StringField(validators=[DataRequired()])
    email = StringField(validators=[Email(), DataRequired()])
    timetable = TextAreaField(validators=[DataRequired()])
    avatar = FileField(
        validators=[
            FileRequired(),
            FileAllowed(["png", "jpg", "jpeg"], "images only!"),
        ],
    )
    submit = SubmitField("submit")

    def validate_timetable(self, timetable):
        try:
            create_timetable(timetable.data)
        except Exception:
            raise ValidationError("re-check your timetable format!")


class UserSearch(FlaskForm):
    name = StringField("Name")
    submit = SubmitField("search")
