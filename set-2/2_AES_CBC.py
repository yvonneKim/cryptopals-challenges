# AES CBC encryptor.decryptor- doing it manually!

import os, sys, base64, binascii
from byteXor import xor as bxor
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend      

def main():
    filename = '10.txt'
    with open(filename, 'r') as f:
        data = b''.join((base64.b64decode(x.strip()) for x in f.readlines()))
        key = b'YELLOW SUBMARINE'
        iv = b'\x00' * len(key)

        # decrypt the test file
        d = decrypt(data, key, iv)
        with open(filename+'.out', 'wb') as outf:
            outf.write(d)

        # then encrypt it again and diff
        e = encrypt(d, key, iv)

        if e == data:
            print("VERIFIED!")
        else:
            print("ERROR - original differs from encrypted")
            print(bxor(d, e))


def decrypt(data, key, iv):
    bsize = len(key)    
    blocks = [data[i:i+bsize] for i in range(0, len(data)-bsize, bsize)]
    blocks.insert(0, iv)
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    
    ptext_blocks = []
    for i in range(len(blocks)-1, 1, -1):
        cur = blocks[i]
        prev = blocks[i-1]

        cur = cipher.decryptor().update(cur)
        cur = bxor(cur, prev)
        ptext_blocks.append(cur) 

    ptext_blocks.reverse()
    return b''.join(ptext_blocks)


def encrypt(data, key, iv):
    bsize = len(key)
    blocks = [data[i:i+bsize] for i in range(0, len(data)-bsize, bsize)]
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


if __name__=='__main__':
    main()
