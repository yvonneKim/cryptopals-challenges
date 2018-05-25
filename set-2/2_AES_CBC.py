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
        e = encrypt(d, key)

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
    first_block = d[0:len(key)]
    d = cipher.decryptor().update(first_block)
    ptext_blocks.append(bxor(d, iv))

    ptext_blocks.reverse()
    return b''.join(ptext_blocks)

### TO DO ###
# def encrypt(data, key, iv):    
#     block_gen = lambda d, b, n: (d[i:i+b] for i in range(0, b*(n-1), b))
#     ptext_blocks = []
    
#     for blocks in block_gen(data, bsize, bsize):
        

        
#         ctext = blocks[1]

#         cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
#         decryptor = cipher.decryptor()
#         ptext = decryptor.update(ctext) + decryptor.finalize()
#         ptext_blocks.append(ptext)
#         return ''.join(ptext_blocks)


if __name__=='__main__':
    main()
