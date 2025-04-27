#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: Joshua Moses
"""

from .database import get_db_connection
from .encryption import encrypt, decrypt
from .password_utils import is_strong_password

def add_credential(username, credential_name, address, password):
    if not is_strong_password(password):
        print("Password is not strong enough! Must be 12+ characters, mix of upper, lower, digits, symbols.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    
    encrypted_username = encrypt(username)
    encrypted_credential_name = encrypt(credential_name)
    encrypted_address = encrypt(address)
    encrypted_password = encrypt(password)
    
    cursor.execute('''
        INSERT INTO credentials (username, credential_name, address, password)
        VALUES (%s, %s, %s, %s)
    ''', (encrypted_username, encrypted_credential_name, encrypted_address, encrypted_password))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Credential added successfully!")

def edit_credential(id, username, credential_name, address, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    encrypted_username = encrypt(username)
    encrypted_credential_name = encrypt(credential_name)
    encrypted_address = encrypt(address)
    encrypted_password = encrypt(password)
    
    cursor.execute('''
        UPDATE credentials
        SET username=%s, credential_name=%s, address=%s, password=%s
        WHERE id=%s
    ''', (encrypted_username, encrypted_credential_name, encrypted_address, encrypted_password, id))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Credential updated successfully!")

def delete_credential(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM credentials WHERE id=%s', (id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Credential deleted successfully!")
