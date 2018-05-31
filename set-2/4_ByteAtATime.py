# does padding oracle exploit to find out padding

import sys, os, base64
PKCS7 = __import__('1_PKCS7')
Oracle = __import__('3_Oracle') 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def main():
    global_key = os.urandom(16)
    data = sys.argv[1].encode('utf-8')
    e = encrypt(data, global_key)
    print(e)
    d = decryptMsg(e)
    print(d)

def encrypt(data, key):
    secret = """
    Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK
    """
    secret = base64.b64decode(secret)
    data = PKCS7.pad(data + secret, len(key))
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    return cipher.encryptor().update(data)

def decryptMsg(data):
    return data

if __name__=='__main__':
    main()
