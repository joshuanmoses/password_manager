#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Joshua Moses
"""

import mysql.connector
import os
import time
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'userpassword')
DB_NAME = os.getenv('DB_NAME', 'password_manager')


def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database.
    """
    attempt = 0
    while attempt < 5:
        try:
            connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            return connection
        except mysql.connector.Error as err:
            print(f"Database connection failed: {err}")
            print("Retrying...")
            time.sleep(2)
            attempt += 1
    raise Exception("Failed to connect to the database after multiple attempts.")


def initialize_database():
    """
    Initializes the database by creating the credentials table if it does not exist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credentials (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username TEXT NOT NULL,
            credential_name TEXT NOT NULL,
            address TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()
