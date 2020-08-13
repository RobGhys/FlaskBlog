from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__) # Name of the module
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# Create a site.db file in the FlaskBlog directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Initialises the database
db = SQLAlchemy(app)

# Initialises crypto
bcrypt = Bcrypt(app)

# Initialises login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info' # Info class from Bootstrap (blue text)

from flaskblog import routes