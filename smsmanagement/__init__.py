import os.path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

#############################
######DATABASE SETUP#########
#############################
# Often people will also separate these into a separate config.py file
app.config['SECRET_KEY'] = 'secretary'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
Migrate(app, db)

#############################
######LOGIN SETUP############
#############################

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'

from smsmanagement.core.views import core  # here this core is blueprint core
from smsmanagement.users.views import users
from smsmanagement.groups.views import groups
from smsmanagement.contacts.views import contacts
from smsmanagement.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(groups)
app.register_blueprint(contacts)
app.register_blueprint(error_pages)
