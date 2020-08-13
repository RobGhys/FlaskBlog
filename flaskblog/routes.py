import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Rob',
        'title': 'Title #1',
        'content': 'First blog post!',
        'date_posted': 'August 11, 2020'
    },
    {
        'author': 'Caro',
        'title': 'Title #2',
        'content': 'Second blog post!',
        'date_posted': 'August 12, 2020'
    },
    {
        'author': 'Poupouns',
        'title': 'Title #3',
        'content': 'Third blog post!',
        'date_posted': 'August 13, 2020'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    # Uses title 'About' instead of displaying standard title
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Redirects to home page if already loged-in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Uses RegistrationForm class from forms.py
    form = RegistrationForm()
    # Tells if form was validated, with Bootstrap 'success' class
    if form.validate_on_submit():
        # Save user inputs to db
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created!', 'success')
        # Redirects the user to /login if form is validated
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Redirects to home page if already loged-in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Uses LoginForm class from forms.py
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Checks if user exists, and password entered match
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Logs the user in
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Incorrect email and password combination', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # We only use f_ext
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # Resize the image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        # Redirects so that we avoid having a 'confirm?' message in our browser when updating the form
        return redirect(url_for('account'))

    # Populates with current user data
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)