# does padding oracle exploit to find out padding

import sys, os, base64
PKCS7 = __import__('1_PKCS7')
Oracle = __import__('3_Oracle') 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def main():
    global_key = os.urandom(16)
    data = b'YELLOW SUBMARINE'
    e = encrypt(data, global_key)
    d = decrypt_msg(e, global_key)

def encrypt(data, key):
    secret = """
    Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK
    """
    secret = base64.b64decode(secret)
    data = PKCS7.pad(data + secret, len(key))
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    return cipher.encryptor().update(data)

def decrypt_msg(data, key):
    # Determine blocksize. Most likely 16 bytes.
    # The first i that results in a repeated first block is (bsize + 1)

    def get_bsize(data):
        prev = None
        for i in range(2, 32):
            x = encrypt(b'A'*i, key)
            if prev == None: # first time
                prev = x[0:i]
            elif prev == x[0:len(prev)]:
                return i - 1
            else:
                print(prev)
                prev = x[0:i]
            
    bsize = get_bsize(data)
    print(bsize)

    d = Oracle.analyze(data, bsize)
    if d == 'ECB':
        pass
    elif d == 'CBC':
        pass
    else:
        pass
    return data

if __name__=='__main__':
    main()
