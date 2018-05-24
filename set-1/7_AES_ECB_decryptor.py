# I took this mostly from: https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#cryptography.hazmat.primitives.ciphers.algorith1;2802;0cms.AES
import os, sys, base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

with open(sys.argv[1], 'r') as f:
    data = base64.b64decode(''.join([x.strip() for x in f.readlines()]))

key = b'YELLOW SUBMARINE' # that's what they want from me for this challenge! change later
backend = default_backend()

# PKCS7 padding to the next bsize multiple
bsize = len(key)
num_blocks = (len(data) + bsize -1) // bsize
if len(data) % bsize != 0:
    print("PADDING NOW")
    data = data.ljust(num_blocks, bytes(len(data) % bsize)[0])

ptext_blocks = []
# decryption block by block backwards n-1 times (stop at 2nd block)
block_gen = lambda d, b: ((d[i-(2*b):i-b], d[i-b:i]) for i in range(b*num_blocks, b, -b))
for blocks in block_gen(data, bsize):
    iv = blocks[0]
    ctext = blocks[1]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    ptext = decryptor.update(ctext) + decryptor.finalize()
    ptext_blocks.append(ptext)

with open(sys.argv[1]+'.out', 'wb') as f:
    out = b''.join(ptext_blocks)
    f.write(out)
