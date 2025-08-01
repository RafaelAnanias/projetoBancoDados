from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import mysql.connector
import json

 
import os

load_dotenv('.env')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager (app)

login_manager.login_view = 'homepage'

bcrypt = Bcrypt(app)

from estudo.views import homepage
from estudo.models import Lista