from flask_wtf import FlaskForm
from wtforms import *
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
import random
from .models import Question

from wtforms.validators import *


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[InputRequired(), Length(min=5)])
    password = PasswordField("Пароль", validators=[InputRequired(), Length(min=8, max=32)])
    remember = BooleanField("Запомни меня")
    submit = SubmitField("Войти")


class ProfileForm(FlaskForm):
    name = StringField("Имя", validators=[InputRequired(), Length(max=40)])
    surname = StringField("Фамилия", validators=[InputRequired(), Length(max=40)])
    username = StringField("Имя пользователя", validators=[InputRequired(), Length(min=5)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Неверный email'), Length(max=50)])
    password = PasswordField("Пароль", validators=[InputRequired(message='Неверный пароль'), Length(min=8, max=32)])
    submit = SubmitField('Сохранить')


class RegisterForm(ProfileForm):
    confirm_password = PasswordField("Подтвердите пароль", validators=[InputRequired(),
                                                                       EqualTo('password',
                                                                               message='Пароли не одинаковые'),
                                                                       Length(min=8, max=32)])
    submit = SubmitField("Зарегистрироваться")


class AnswerForm(FlaskForm):
    answer = StringField('Ответ', validators=[InputRequired()])


class QuestionForm(FlaskForm):
    question = StringField('Вопрос', validators=[InputRequired()])
    answers = FieldList(FormField(AnswerForm, 'Ответ'), label='Ответы', separator=' ', min_entries=4)
    right_number = SelectField('Правильный ответ', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], coerce=int)
    submit = SubmitField('Сохранить')


class TestForm(FlaskForm):
    title = StringField('Название', validators=[InputRequired()])
    description = TextAreaField('Описание')
    image = StringField('', render_kw={'style': 'display:none'}, default='dns.png')
    questions = QuerySelectMultipleField('Вопросы', query_factory=lambda: random.sample(Question.query.all(), 10 if len(Question.query.all())>10 else len(Question.query.all())),
                                         widget=widgets.ListWidget(prefix_label=False),
                                         option_widget=widgets.CheckboxInput(),
                                         render_kw={'style': 'list-style-type: none;'})
    is_common = BooleanField('Доступен для всех')
    submit = SubmitField('Сохранить')
