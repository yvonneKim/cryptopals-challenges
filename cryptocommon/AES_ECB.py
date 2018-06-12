import os, sys, base64, cryptocommon.PKCS7
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def main():
    with open(sys.argv[1], 'r') as f:
        data = base64.b64decode(''.join([x.strip() for x in f.readlines()]))

    key = sys.argv[2].encode('utf-8')
    ptext = decryptor(data, key, len(key))

    with open(sys.argv[1]+'.out', 'wb') as f:
        f.write(ptext)


def decryptor(data, key, bsize):
    # PKCS7 padding to the next bsize multiple
    data = PKCS7.pad(data, bsize)

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    ptext = decryptor.update(data) + decryptor.finalize()
    return ptext


def encryptor(data, key, bsize):
    # PKCS7 padding to the next bsize multiple
    data = PKCS7.pad(data, bsize)

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    ptext = encryptor.update(data) + encryptor.finalize()
    return ptext


if __name__=='__main__':
    main()
