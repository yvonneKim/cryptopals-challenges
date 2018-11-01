import os
import sys
import base64
sys.path.append(os.path.abspath("../cryptocommon"))
import PKCS7
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def decryptor(data, key, bsize):
    if type(data) != bytes:
        raise ValueError('Not a \'bytes\' type!')

    if len(data) % bsize != 0:
        raise ValueError('Not a multiple of bsize provided!')

    cipher = Cipher(algorithms.AES(key), modes.ECB(),
                    backend=default_backend())
    decryptor = cipher.decryptor()
    ptext = decryptor.update(data) + decryptor.finalize()
    return ptext.decode('utf-8')


def encryptor(data, key, bsize, padded=True):
    """
    Takes plaintext, key, block size, and whether to PKCS7 pad.
    By default, it will pad, as it's safer. It can be set to False for
    cases like encrypting a single block that's already padded.

    Returns the encrypted ciphertext.
    """
    if (type(data) != bytes) & (type(data) != str):
        raise ValueError('Data is neither bytes nor string!')

    if type(data) == str:
        data = data.encode('utf-8')

    if padded:
        data = PKCS7.padPKCS7(data, bsize)

    cipher = Cipher(algorithms.AES(key), modes.ECB(),
                    backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(data) + encryptor.finalize()
    return encrypted


if __name__ == '__main__':
    main()
