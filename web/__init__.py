#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Joshua Moses
"""

from flask import Flask
from flask_login import LoginManager
from web.auth import User

app = Flask(__name__)
app.secret_key = 'your-very-secret-key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

from web import routes, auth
