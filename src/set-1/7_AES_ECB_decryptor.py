# I took this mostly from: https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#cryptography.hazmat.primitives.ciphers.algorith1;2802;0cms.AES
import os, sys, base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def main():
    with open(sys.argv[1], 'r') as f:
        data = base64.b64decode(''.join([x.strip() for x in f.readlines()]))

    key = sys.argv[2].encode('utf-8')
    decryptor(data, key)

def decryptor(data, key):
    backend = default_backend()

    # PKCS7 padding to the next bsize multiple
    bsize = len(key)
    num_blocks = (len(data) + bsize -1) // bsize
    if len(data) % bsize != 0:
        print("PADDING NOW")
        data = data.ljust(num_blocks, bytes(len(data) % bsize)[0])

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    ptext = decryptor.update(data) + decryptor.finalize()

    with open(sys.argv[1]+'.out', 'wb') as f:
        f.write(ptext)


if __name__=='__main__':
    main()
####
#### THIS CODE IS FOR CBC BUT IT MIGHT BE HANDY LATER ####
####
#block_gen = lambda d, b, n: (d[i:i+b] for i in range(0, b*(n-1), b))
#ptext_blocks = []
# decryption block by block backwards n-1 times (stop at 2nd block)
# block_gen = lambda d, b: ((d[i-(2*b):i-b], d[i-b:i]) for i in range(b*num_blocks, b, -b))
# for blocks in block_gen(data, bsize):
#     iv = blocks[0]
#     ctext = blocks[1]

#     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
#     decryptor = cipher.decryptor()
#     ptext = decryptor.update(ctext) + decryptor.finalize()
#     ptext_blocks.append(ptext)

# with open(sys.argv[1]+'.out', 'wb') as f:
#     out = b''.join(ptext_blocks)
#     f.write(out)
