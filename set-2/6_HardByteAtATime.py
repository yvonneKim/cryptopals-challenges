# does padding oracle exploit to find out padding

import sys, os, base64

PKCS7 = __import__('1_PKCS7')
Oracle = __import__('3_Oracle')
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def main():
    with open(sys.argv[1], 'rb') as f:
        global_key = os.urandom(16)
        data = b''.join((x.strip() for x in f.readlines()))
        e = encrypt(data, global_key)
        d = decrypt_msg(e, global_key)
        print(d)


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
            x = encrypt(b'A' * i, key)
            if prev == None:  # first time
                prev = x[0:i]
            elif prev == x[0:len(prev)]:
                return i - 1
            else:
                prev = x[0:i]

    bsize = get_bsize(data)

    # Is it ECB or CBC? Need to know from here on.
    d = Oracle.analyze(data, bsize)
    if d == 'ECB':
        print("ECB DETECTED")
    elif d == 'CBC':
        print("CBC DETECTED- CANNOT CONTINUE ... for now :)")
        return None

    # Figuring out the secret message by feeding in byte at a time.
    result = b''
    secret_size = len(encrypt(b'', key))
    offset = b'A' * (secret_size - 1)
    cur_offset = offset

    for x in range(0, secret_size):  # for every byte of the secret message
        cur = encrypt(cur_offset, key)[secret_size - bsize:secret_size]
        for i in range(0, 256):  # for every possible byte
            c = i.to_bytes(1, byteorder='big')
            e = encrypt(offset + c, key)[secret_size - bsize:secret_size]
            if e == cur:
                offset = (offset + c)[1:]
                cur_offset = cur_offset[1:]
                result += c
                break

    return result


if __name__ == '__main__':
    main()
