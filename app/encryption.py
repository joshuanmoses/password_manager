#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: Joshua Moses
"""
import os
import boto3
from dotenv import load_dotenv
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

load_dotenv()

USE_KMS = os.getenv('USE_KMS', 'False').lower() == 'true'
AES_KEY = os.getenv('AES_KEY').encode()

if USE_KMS:
    kms_client = boto3.client('kms', region_name=os.getenv('AWS_REGION'))

def encrypt(data):
    if USE_KMS:
        response = kms_client.encrypt(
            KeyId=os.getenv('KMS_KEY_ID'),
            Plaintext=data.encode()
        )
        return b64encode(response['CiphertextBlob']).decode()
    else:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(AES_KEY), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(data.encode()) + encryptor.finalize()
        return b64encode(iv + ct).decode()

def decrypt(data):
    if USE_KMS:
        decoded_blob = b64decode(data)
        response = kms_client.decrypt(CiphertextBlob=decoded_blob)
        return response['Plaintext'].decode()
    else:
        data = b64decode(data)
        iv = data[:16]
        ct = data[16:]
        cipher = Cipher(algorithms.AES(AES_KEY), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return (decryptor.update(ct) + decryptor.finalize()).decode()

