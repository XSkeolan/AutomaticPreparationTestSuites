from flask_wtf import FlaskForm
from wtforms import *

from wtforms.validators import *


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=5)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=32)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Войти")


class ProfileForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(min=5, max=40)])
    surname = StringField("Surname", validators=[InputRequired(), Length(min=5, max=40)])
    username = StringField("Username", validators=[InputRequired(), Length(min=5)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField("Password", validators=[InputRequired(message='Invalid password'), Length(min=8, max=32)])
    submit = SubmitField('Сохранить')


class RegisterForm(ProfileForm):
    confirm_password = PasswordField("ConfirmPassword", validators=[InputRequired(),
                                                                    EqualTo('password', message='Passwords not equal'),
                                                                    Length(min=8, max=32)])
    submit = SubmitField("Зарегистрироваться")


class AnswerForm(FlaskForm):
    answer = StringField('Ответ', validators=[InputRequired()])


class QuestionForm(FlaskForm):
    question = StringField('Вопрос', validators=[InputRequired()])
    answers = FieldList(FormField(AnswerForm), label='Ответы', separator=' ', min_entries=4)
    right_number = SelectField('Правильный ответ', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], coerce=int)
    submit = SubmitField('Сохранить')


class TestForm(FlaskForm):
    title = StringField('Название', validators=[InputRequired()])
    description = StringField('Описание')
    image = ''
    questions = ''
    is_common = BooleanField('Доступен для всех')
    submit = SubmitField('Сохранить')
