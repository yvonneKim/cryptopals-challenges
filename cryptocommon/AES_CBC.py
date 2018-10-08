# AES CBC encryptor/decryptor- doing it manually!

import os, sys, base64, binascii
from byteXor import xor as bxor
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend      


def decrypt(data, key, iv):

    if type(data) != bytes:
        raise ValueError('Data is not bytes type!')

    if type(key) != bytes:
        raise ValueError('Key is not bytes type!')

    if type(iv) != bytes:
        raise ValueError('iv is not bytes type!')

    data = iv + data
    bsize = len(key)

    if len(data) % bsize != 0:
        raise ValueError('Length of data is not a multiple of length of key!')

    if len(iv) != bsize:
        raise ValueError('Length of iv is not same as length of key!')
    
    blocks = [data[i:i+bsize] for i in range(0, len(data)-bsize+1, bsize)]
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    
    ptext_blocks = []
    for i in range(len(blocks)-1, 0, -1):
        cur = blocks[i]
        prev = blocks[i-1]

        cur = cipher.decryptor().update(cur)
        cur = bxor(cur, prev)
        ptext_blocks.append(cur) 

    ptext_blocks.reverse()
    return (b''.join(ptext_blocks)).decode('utf-8')


def encrypt(data, key, iv):
    if (type(data) != str) & (type(data) != bytes):
        raise ValueError('Data is neither string nor bytes!')

    bsize = len(key)

    if len(data) % bsize != 0:
        raise ValueError('Length of data is not multiple of length of key!')

    if len(iv) != bsize:
        raise ValueError('Length of iv is not same as length of key!')
    
    blocks = [data[i:i+bsize] for i in range(0, len(data)-bsize+1, bsize)]
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())

    ctext_blocks = [iv]
    for i in range(0, len(blocks)):
        cur = blocks[i]
        prev = ctext_blocks[i]

        cur = bxor(cur, prev)
        cur = cipher.encryptor().update(cur)
        ctext_blocks.append(cur)
        

    ctext_blocks.pop(0) # because this would be the iv block
    return b''.join(ctext_blocks)
