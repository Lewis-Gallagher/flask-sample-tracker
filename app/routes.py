from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User
from app.forms import LoginForm, RegistrationForm, SampleInputForm


@app.route('/')
@app.route('/index')
@login_required
def index():

    return render_template('index.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():

    # Check if the user is already logged in.
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # If user isn't logged in initialise the login form.
    form = LoginForm()

    # Check User table for supplied username and password.
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))
        
        # If username and password are both correct, login the user and redirect to the index page.
        login_user(user, remember = form.remember_me.data)

        # Once the user is logged in, redirect to their requested page.
        next_page = request.args.get('next')

        # A next page wasn't requested or the next page is at a different domain then redirect to index.
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', 
                           title = 'Sign In', 
                           form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():

    # If user is already registered, redirect to index.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # Initialise registration form.
    form = RegistrationForm()

    # If valid, commit User to database.
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered! Congratulations!')
        return redirect(url_for('index'))
    
    return render_template('register.html', title = 'Register', form = form)


@app.route('/sample-input', methods=['GET', 'POST'])
@login_required
def sample_input():

    form = SampleInputForm()

    if form.validate_on_submit():
        return redirect(url_for('sample_input'))

    return render_template('input.html', form = form)