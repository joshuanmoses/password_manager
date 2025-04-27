#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Joshua Moses
"""
from flask import request, redirect, render_template, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, UserMixin
from web import app
import hashlib
import pyotp
import qrcode
import os

# Generate a TOTP secret manually for the admin (only once, reuse later)
# In production, this would be securely generated and stored!
TOTP_SECRET = os.getenv('TOTP_SECRET', 'JBSWY3DPEHPK3PXP')  # Example static

# Store user hashes
USERS = {
    "admin": {
        "password": hashlib.sha256("adminpassword".encode()).hexdigest(),
        "totp_secret": TOTP_SECRET
    }
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

    @staticmethod
    def get(user_id):
        if user_id in USERS:
            return User(user_id)
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('2fa_verified', None)  # Always reset

        username = request.form['username']
        password = request.form['password']
        hashed = hashlib.sha256(password.encode()).hexdigest()

        user = USERS.get(username)
        if user and user['password'] == hashed:
            session['pre_2fa_user'] = username
            return redirect(url_for('two_factor'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/2fa', methods=['GET', 'POST'])
def two_factor():
    if 'pre_2fa_user' not in session:
        return redirect(url_for('login'))

    username = session['pre_2fa_user']
    user = USERS.get(username)
    if not user:
        return redirect(url_for('login'))

    totp = pyotp.TOTP(user['totp_secret'])

    if request.method == 'POST':
        token = request.form['token']
        if totp.verify(token):
            login_user(User(username))
            session.pop('pre_2fa_user')
            session['2fa_verified'] = True
            return redirect(url_for('index'))
        else:
            flash('Invalid 2FA code')

    return render_template('2fa.html')

@app.route('/logout')
def logout():
    logout_user()
    session.pop('2fa_verified', None)
    return redirect(url_for('login'))

@app.route('/generate_qr')
def generate_qr():
    """
    Use this route to initially generate a QR code for setting up 2FA in Google Authenticator.
    """
    if 'pre_2fa_user' not in session:
        return redirect(url_for('login'))

    username = session['pre_2fa_user']
    user = USERS.get(username)

    totp = pyotp.TOTP(user['totp_secret'])
    uri = totp.provisioning_uri(name=username, issuer_name="PasswordManagerApp")

    img = qrcode.make(uri)
    img.save('web/static/qrcode.png')
    return render_template('show_qr.html')
