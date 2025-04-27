#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Joshua Moses
"""

from flask import render_template, request, redirect, url_for
from flask_login import login_required
from app.manager import add_credential, generate_report, edit_credential, delete_credential
from web import app

@app.route('/')
@login_required
def index():
    search = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = 5

    all_credentials = generate_report(return_data=True)
    if search:
        all_credentials = [cred for cred in all_credentials if search.lower() in cred['credential_name'].lower()]

    start = (page - 1) * per_page
    end = start + per_page
    paginated = all_credentials[start:end]
    total_pages = (len(all_credentials) + per_page - 1) // per_page

    return render_template('index.html', credentials=paginated, page=page, total_pages=total_pages, search=search)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        username = request.form['username']
        credential_name = request.form['credential_name']
        address = request.form['address']
        password = request.form['password']
        add_credential(username, credential_name, address, password)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if request.method == 'POST':
        username = request.form['username']
        credential_name = request.form['credential_name']
        address = request.form['address']
        password = request.form['password']
        edit_credential(id, username, credential_name, address, password)
        return redirect(url_for('index'))
    return render_template('edit.html', id=id)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    delete_credential(id)
    return redirect(url_for('index'))
