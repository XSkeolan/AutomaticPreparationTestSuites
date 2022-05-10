from datetime import datetime
import uuid
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

from app.database import db

test_user = db.Table('testuser',
                     db.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True,
                               nullable=False),
                     db.Column('testid', UUID(as_uuid=True), db.ForeignKey('tests.id'), nullable=False),
                     db.Column('userid', UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False),
                     db.Column('score', db.Float(), default=0, nullable=False))

test_question = db.Table('testquestion',
                         db.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True,
                                   nullable=False),
                         db.Column('questionid', UUID(as_uuid=True), db.ForeignKey('questions.id'), nullable=False),
                         db.Column('testid', UUID(as_uuid=True), db.ForeignKey('tests.id'), nullable=False))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    # created_on = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    # updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('roles.id'), nullable=False)
    tests_created = db.relationship('Test', backref='creator')
    tests = db.relationship('Test', backref='passed_test', secondary=test_user, lazy='dynamic')

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, 'sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    permissions = db.Column(db.String(200), nullable=False)
    users = db.relationship('User', backref='role')


class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=True)
    creator_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=True)
    is_common = db.Column(db.Boolean(), nullable=False, default=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    questions = db.relationship('Question', secondary=test_question, backref='in_tests')
    #questions = db.relationship('Question', secondary=test_question, backref=db.backref('tests', lazy='dynamic'),
                                #lazy='dynamic')

    def is_contain_question(self, question):
        return self.questions.filter(test_question.c.questionid == question.id and
                                     test_question.c.testid == self.id).count() > 0

    def add_question(self, question):
        if not self.is_contain_question(question):
            self.questions.append(question)
            db.session.commit()

    def remove_question(self, question):
        if self.is_contain_question(question):
            self.questions.remove(question)
            db.session.commit()

    def update(self, title, description):
        self.title = title
        self.description = description
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    answers = db.relationship('Answer', backref='in_question')

    def update(self, new_question):
        self.title = new_question
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    fraction = db.Column(db.Integer, nullable=False)
    questionid = db.Column(UUID(as_uuid=True), db.ForeignKey('questions.id'), nullable=False)
