from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#import email_validator
#import secrets


app = Flask(__name__) # Name of the module
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# Create a site.db file in the FlaskBlog directory
app.config['SQL_ALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Initialises the database
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    # Lazy=true -> SQLAlchemy loads data as necessary in one go.
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User ('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post ('{self.title}', '{self.date_posted}')"


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
    # Uses RegistrationForm class from forms.py
    form = RegistrationForm()
    # Tells if form was validated, with Bootstrap 'success' class
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}.', 'success')
        # Redirects the user to /home if form is validated
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Uses LoginForm class from forms.py
    form = LoginForm()
    if form.validate_on_submit():
        # If LoginForm is submitted with correct email and password, flash message
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please verify username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    db.create_all(app)
    app.run(debug=True)
