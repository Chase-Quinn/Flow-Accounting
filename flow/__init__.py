from flask import Flask, flash, redirect, request, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail, Message


app = Flask(__name__)
app.config['SECRET_KEY']='a^.=O}>r~t[hP]1B9s.Im+_^WQ]TX1M;Ek="kB4)Fkvi'

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///flow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 0
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = 'a^.=O}>r~t[hP]1B9s.Im+_^WQ]TX1M;Ek="kB4)Fkvi'
app.config['TESTING'] = False


#SETTING MAIL SERVER CONFIG

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'flow.acc.services@gmail.com'
app.config['MAIL_PASSWORD'] = 'crts2020!'
app.config['MAIL_DEFAULT_SENDER'] = ('Flow Account Services', 'flow.acc.services@gmail.com')
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

# TURNED AUTOFLUSH OFF
db = SQLAlchemy(app, session_options={"autoflush": False})

# INITIALIZING IMPORTS
bcrypt = Bcrypt(app)
bootstrap = Bootstrap(app)
mail = Mail(app)
login_manager=LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'error'

db.create_all()

from flow import views