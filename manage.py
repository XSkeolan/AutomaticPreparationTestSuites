import builtins
import json
import os
from urllib.parse import urlparse, urljoin

from flask import render_template, redirect, url_for, session, flash, request, abort, Response, make_response
from flask_script import Manager
from flask_bootstrap import Bootstrap5
from app import models

from flask_login import LoginManager, login_user, login_required, current_user, logout_user, AnonymousUserMixin

from app import create_app
from app.forms import *
from app.models import *
from app.database import db
from sqlalchemy.sql.expression import select
from sqlalchemy import func, desc, asc, text
from pathlib import Path
from sqlalchemy.exc import IntegrityError
from flask_restful import reqparse
import uuid

app = create_app()

manager = Manager(app)
bootstrap = Bootstrap5(app)
login = LoginManager(app)
login.login_view = 'login'


@login.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login')
def login():
    form = LoginForm()
    next = request.args.get('next')
    if next is not None:
        session['next'] = next
    return render_template('login.html', form=form)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@app.errorhandler(403)
def forbidden(e):
    return render_template('/errors/403.html')


@app.errorhandler(404)
def not_found(e):
    return render_template('/errors/404.html')


# не работает redirect
@app.route('/loginme', methods=['POST'])
def login_me():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if not user:
            flash('Неверный никнейм или пароль')
            return render_template('login.html', form=form)

        if not user.check_password(form.password.data):
            flash('Неверный никнейм или пароль')
            return render_template('login.html', form=form)

        print(form.remember.data)
        login_user(user, remember=form.remember.data)
        if 'next' in session:
            next = session['next']
            print('next = ' + str(next))
            if is_safe_url(next):
                return redirect(next)
        return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        new_user = User(name=form.name.data, surname=form.surname.data, username=form.username.data,
                        email=form.email.data, role_id=Role.query.filter_by(name='user').first().id)
        new_user.set_password(form.password.data)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('login')
        except IntegrityError:
            db.session.rollback()
            flash('Пользователь с таким email или username уже существует ')
    return render_template('register.html', form=form)


@app.route('/', methods=['GET'])
def index():
    tests = Test.query.filter_by(is_common=True).all()
    if current_user.is_authenticated:
        tests = Test.query.all()
        return render_template('index.html', current_user=current_user, tests=tests)
    return render_template('index.html', tests=tests)


@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    users = User.query.all()
    current_user_percent_right = 0
    top_tests = []
    people = []
    for user in users:
        completed_tests_id = db.session.query(test_user.c.testid, test_user.c.score).filter(test_user.c.userid == user.id).order_by(test_user.c.score)
        tests = completed_tests_id.all()
        count_quests = 0
        for i in range(len(tests)):
            count_quests += len(Test.query.get(tests[i][0]).questions.all())

        score_sum = db.session.query(func.sum(test_user.c.score).label('sum')).filter(test_user.c.userid == user.id).group_by(test_user.c.userid).scalar()
        if count_quests == 0:
            percent_right = 0
            score_sum = 0
        else:
            percent_right = score_sum * 100.0 / count_quests
        if user.id == current_user.id:
            current_user_percent_right = percent_right
            top_tests_id = completed_tests_id.limit(5).all()

            for test in top_tests_id:
                count_quests = 0
                current_test = Test.query.get(test[0])
                count_quests += len(current_test.questions.all())
                percent_right_test = test[1] * 100 / count_quests

                top_tests.append((current_test.title, percent_right_test))

        people.append((user.name, user.surname, percent_right, score_sum))

    people = sorted(people, key=lambda tup: tup[2], reverse=True)
    top_tests = sorted(top_tests, key=lambda tup: tup[1], reverse=True)
    created_tests = current_user.tests_created
    passed_tests = current_user.tests.all()

    return render_template('dashboard.html', current_user=current_user, created_tests=created_tests,
                           current_role=Role.query.get(current_user.role_id), completed_tests=passed_tests,
                           percent=current_user_percent_right, top_tests=top_tests[:5], top_people=people[:5])


@app.route('/editprofile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if request.method == 'GET':
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.username.data = current_user.username
        form.email.data = current_user.email
        return render_template('profile.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            try:
                user = User.query.get(current_user.id)
                user.name = form.name.data
                user.surname = form.surname.data
                user.username = form.username.data
                user.email = form.email.data
                user.set_password(form.password.data)
                db.session.commit()
                flash('Изменения успешно применены', 'success')
            except IntegrityError:
                db.session.rollback()
                flash('Пользователь с вашим новым именем или email уже существует')
        return render_template('profile.html', form=form)


@app.route('/bank')
@login_required
def bank():
    role = Role.query.get(current_user.role_id)
    if role.name == 'user':
        abort(403)

    questions = Question.query.all()
    response = dict()
    for question in questions:
        response[question.title] = question.answers
    print(response)
    return render_template('bank.html', questions=questions, answers=response)


@app.route('/tests/createTest', methods=['GET', 'POST'])
@login_required
def create_test():
    form = TestForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                test = Test(title=form.title.data, description=form.description.data, creator_id=current_user.id,
                            is_common=form.is_common.data, image=form.image.data)
                if len(form.questions.data) < 5:
                    raise ValueError
                db.session.add(test)
                db.session.commit()

                for quest in form.questions.data:
                    test.add_question(Question.query.get(form.questions.get_pk(quest)))

                flash('Тест успешно создан', category='success')
            except IntegrityError:
                db.session.rollback()
                flash('Тест с таким названием уже существует', category='danger')
            except ValueError:
                flash('Нужно выбрать хотя бы 5 вопросов для теста', category='danger')
    base_url = url_for('static', filename='img/tests/dns.png')
    base_url = base_url[:len(base_url) - 1 - base_url[::-1].index('/')]
    entries = Path('./app'+base_url+'/')
    print(entries)
    files = []
    for entry in entries.iterdir():
        files.append(entry.name)

    questions = Question.query.all()

    return render_template('create_test.html', form=form, images=files, questions=questions)


@app.route('/tests/<testid>', methods=['GET', 'POST'])
def get_test(testid):
    test = Test.query.get_or_404(testid)
    return render_template('start_test.html', test=test, creator=User.query.get(test.creator_id))


@app.route('/tests/<testid>/edit', methods=['GET', 'POST'])
def update_test(testid):
    test = Test.query.get_or_404(testid)
    if test.creator_id != current_user.id:
        return abort(403)
    form = TestForm()
    if request.method == 'GET':
        form.title.data = test.title
        form.description.data = test.description
        form.is_common = test.is_common
        form.questions.data = test.questions
        # добавить потом изображение
    else:
        test.title = form.title.data
        test.description = form.description.data
        test.is_common = form.is_common
        # добавить квесты и потом изображение
    return render_template('edit_test.html', form=form)


@app.route('/tests/<testid>/delete', methods=['GET'])
@login_required
def delete_test(testid):
    test = Test.query.filter_by(id=testid).first()
    test.delete()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/tests/<testid>/getResult', methods=['POST'])
def check_answer(testid):
    print(testid)
    print(request.get_json())
    parser = reqparse.RequestParser()
    parser.add_argument('answers', type=builtins.list, action='append')
    args = parser.parse_args()
    print(args)
    test = Test.query.get(testid)
    if args['answers'] is None:
        return make_response('<div class="alert alert-danger" role="alert">Не на все вопросы были выбраны ответы</div>', 400)
    if len(test.questions.all()) > len(args['answers']):
        return make_response('<div class="alert alert-danger" role="alert">Не на все вопросы были выбраны ответы</div>', 400)
    answers = []
    for i in range(len(args['answers'])):
        answers.append(''.join(args['answers'][i]))
    response = dict()
    score = 0
    for answer in answers:
        a = Answer.query.get(answer)
        if a.fraction == 100:
            score += 1
        quest = Question.query.get(a.questionid)
        print(quest.answers)
        for answer2 in quest.answers:
            if answer2.fraction == 100:
                response[answer] = str(answer2.id)
    if current_user.is_authenticated:
        sql = text("INSERT INTO testuser(id, testid, userid, score) VALUES('" + str(uuid.uuid4()) + "', '" + testid + "', '" + str(current_user.id) + "', " + str(score) + ")")
        db.engine.execute(sql)
    print(response)
    return json.dumps({'success': True, 'answers': response}), 200, {'ContentType': 'application/json'}


@app.route('/addQuestInTest', methods=['GET'])
def add_quest_in_test():
    test = Test.query.filter_by(id='ffbad319-1129-4830-b754-274ca97a3b56').first()
    question = Question.query.filter_by(id='77683c33-d5be-4288-9983-58d1aedcb533').first()
    test.add_question(question)
    return 'Quest added in tests'


@app.route('/bank/createQuestion', methods=['GET', 'POST'])
def create_quest():
    form = QuestionForm()
    if request.method == 'POST':
        print(form.validate_on_submit())
        if form.validate_on_submit():
            try:
                question = Question(title=form.question.data)
                db.session.add(question)
                db.session.commit()
                answers = form.answers.data

                for i in range(len(answers)):
                    answer = Answer(answer=answers[i]['answer'],
                                    fraction=100 if i+1 == int(form.right_number.data) else 0,
                                    questionid=question.id)
                    db.session.add(answer)
                db.session.commit()
                flash('Вопрос создан', 'success')
            except IntegrityError:
                db.session.rollback()
                flash('Такой вопрос уже существует')
    return render_template('question.html', form=form)


# region API
@app.route('/bank/all', methods=['GET'])
@login_required
def get_all_questions():
    role = Role.query.get(current_user.role_id)
    if role.name == 'user':
        abort(403)

    return json.dumps({'success': True, 'data': [quest.title for quest in Question.query.all()]}), 200, {'ContentType': 'application/json'}


@app.route('/mytests/addQuestion', methods=['POST'])
@login_required
def add_question():
    if request.content_type != 'application/json':
        abort(400)
    data = request.json
    # по возможности добавить try из-за ограничей на длину поля
    question = Question(title=data.title)
    db.session.add(question)
    db.session.commit()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/mytests/deleteQuestion', methods=['DELETE'])
@login_required
def delete_question():
    if request.content_type != 'application/json':
        abort(400)
    data = request.json
    question = Question.query.get_or_404(data.id)
    db.session.delete(question)
    db.session.commit()


@app.route('/mytests/question/addAnswer', methods=['POST'])
@login_required
def add_answer():
    if request.content_type != 'application/json':
        abort(400)
    data = request.json
    # по возможности добавить try из-за ограничей на длину поля
    answer = Answer(answer=data.answer, fraction=data.fraction, questionid=data.questionid)
    db.session.add(answer)
    db.session.commit()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/mytests/question/deleteAnswer', methods=['DELETE'])
@login_required
def delete_answer():
    if request.content_type != 'application/json':
        abort(400)
    data = request.json
    answer = Answer.query.get_or_404(data.id)
    db.session.delete(answer)
    db.session.commit()


@app.route('/deleteProfile', methods=['DELETE'])
@login_required
def delete_profile():
    # поробовать сделать через куки/сессию а не параметры из json
    if request.content_type != 'application/json':
        abort(400)
    data = request.json
    user = User.query.get_or_404(data.id)
    db.session.delete(user)
    db.session.commit()
# endregion


@app.route('/unblockBank', methods=['GET'])
def unblock_bank():
    user = User.query.get(current_user.id)
    user.role_id = '93a8c502-a9a9-4bbb-989b-c123ac16379c'
    db.session.commit()
    return redirect('/bank')


if __name__ == '__main__':
    manager.run()
