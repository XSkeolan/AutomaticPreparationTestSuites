from flask import Blueprint, render_template, url_for, flash
from werkzeug.utils import *
from app.models import *
from app.database import db
from app.forms import LoginForm
from flask_login import login_user

module = Blueprint('auth', __name__, url_prefix='/auth')


@module.route('/', methods=['GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('admin'))
        else:
            flash("Invalid username/password", 'error')
    #return redirect(url_for('login'))
    return render_template('authmodule/login.html', form=form)
    return render_template('authmodule/login.html')