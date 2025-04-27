#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Joshua Moses
"""

import argparse
from app.database import initialize_database

def main():
    parser = argparse.ArgumentParser(description="Password Manager System CLI")
    
    parser.add_argument('--init-db', action='store_true', help='Initialize the database (create tables)')
    
    args = parser.parse_args()
    
    if args.init_db:
        print("[*] Initializing database...")
        initialize_database()
        print("[+] Database initialized successfully!")
    else:
        print("[!] No action specified. Use --help to see available options.")

if __name__ == "__main__":
    main()
