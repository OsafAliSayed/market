#All the basic imports
#Basic Imports
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
#necessary Secret Key import in order to display forms in html 
app.config['SECRET_KEY'] = '6dddcd7ca0db22abf9df3268'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager=LoginManager(app)
#setting a default login-page for login_manager function 
login_manager.login_view = 'login_page'
#giving category to login message 
login_manager.login_message_category = 'info'
#importing routes
from market import routes
