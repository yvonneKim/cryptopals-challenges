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
        print(len(iv))

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


def decrypt(data, key, iv):
    backend = default_backend()
    # backwards block traversal to the second block
    block_gen = lambda d, b, e: ((d[i-b-b:i-b], d[i-b:i]) for i in range(e, 2*b, -b))
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    
    ptext_blocks = []
    for i, b in block_gen(data, len(key), len(data)):
        d = cipher.decryptor().update(b)
        ptext_blocks.append(bxor(d, i)) # xor with the previous block = plain text

    # for the last (actually, first) block, do same with the iv
    first = d[0:len(key)]
    first = cipher.decryptor().update(first)
    ptext_blocks.append(bxor(first, iv))

    ptext_blocks.reverse()
    return b''.join(ptext_blocks)

def encrypt(data, key, iv):
    backend = default_backend()
    # goes through all blocks starting from 2nd block
    block_gen = lambda c, d, b, e: ((c[i:i+b], d[i+b:i+b+b]) for i in range(0, e, b))
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    
    ctext = b''
    
    # first block, XOR with iv and then encrypt
    d = bxor(data[0:len(key)], iv)
    ctext += cipher.encryptor().update(d)
    
    for c, b in block_gen(ctext, data, len(key), len(data)):
        d = bxor(c, b)
        ctext += cipher.encryptor().update(d)

    return ctext

if __name__=='__main__':
    main()
