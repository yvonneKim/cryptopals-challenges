# does padding oracle exploit to find out padding

import sys, os, base64, random

PKCS7 = __import__('1_PKCS7')
Oracle = __import__('3_Oracle')
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# sorry for using globals
rand_prefix = os.urandom(random.randint(1, 64))

def main():
    print(rand_prefix)
    print(len(rand_prefix))
    with open(sys.argv[1], 'rb') as f:
        global_key = os.urandom(16)
        data = b''.join((x.strip() for x in f.readlines()))
        e = encrypt(data, global_key)
        d = decrypt_msg(e, global_key)
        print(d)


def encrypt(data, key):
    # For this challenge, it encrypts with a random length, random bytes strings prepended.    
    secret = """
    Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK
    """
    secret = base64.b64decode(secret)
    data = PKCS7.pad(rand_prefix + data + secret, len(key))
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    return cipher.encryptor().update(data)


def decrypt_msg(data, key):
    def get_bsize(data):
        # prev = None
        # for i in range(2, 32):
        #     x = encrypt(b'A' * i, key)
        #     if prev == None:  # first time
        #         prev = x[0:i]
        #     elif prev == x[0:len(prev)]:
        #         return i - 1
        #     else:
        #         prev = x[0:i]
        return 16

    bsize = get_bsize(data)

    # Is it ECB or CBC? Need to know from here on.
    # d = Oracle.analyze(data, bsize)
    # if d == 'ECB':
    #     print("ECB DETECTED")
    # elif d == 'CBC':
    #     print("CBC DETECTED- CANNOT CONTINUE ... for now :)")
    #     return None

    
    # Where is the last partially full block of the random prefix?
    no_inject_e = encrypt(b'', key)
    injected_e = encrypt(b'A', key)
    rp_start = 0
    while no_inject_e[rp_start:rp_start+bsize] == injected_e[rp_start:rp_start+bsize]:
        rp_start = rp_start + bsize

    rp_total_size = rp_start
    print("rp total size initially is ")
    print(rp_total_size)
    print("rp start initially is ")
    print(rp_start)

    
    # Figuring out random prefix size
    rp_end = 0
    e_prev = no_inject_e
    for x in range(1, bsize+1):
        e_cur = encrypt(b'A'*x, key)

        b_prev = e_prev[rp_start : rp_start+bsize]
        b_cur = e_cur[rp_start: rp_start+bsize]
        
        if b_prev == b_cur:
            rp_end = (bsize - x + 1) # always between 1 and bsize- is the finishing length
            print("rp_end is")
            print(rp_end)
            rp_total_size = rp_total_size + rp_end
            print("rp total size is NOW: ")
            print(rp_total_size)
            break
        
        e_prev = e_cur

        
    print("rp_total_size is: ")
    print(rp_total_size)

    rounded_offset = rp_total_size + ((bsize - rp_total_size % bsize) % bsize)
    print("rp_total_size rounded up is: ")
    print(rounded_offset)

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
