from flask import Blueprint, render_template, request, redirect, url_for
from ..forms import LoginForm, RegisterForm
from ..models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User(email, password=password)

            db.session.add(user)
            db.session.commit()

            print('User created successfully, redirecting to login page')
            return redirect(url_for('auth.login'))
    except:
        raise Exception('Invalid Form Data')
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user_current = User.query.filter(User.email == email).first()

            if user_current and check_password_hash(user_current.password, password):
                login_user(user_current)
                print('Logged in successfully, redirecting to profile page')
                return redirect(url_for('site.profile'))
            else:
                print('Invalid credentials, redirecting to login page')
                return redirect(url_for('auth.login'))
    except:
        raise Exception('Invalid Form Data')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    print('Logged out successfully, redirecting to home page')
    return redirect(url_for('site.home'))