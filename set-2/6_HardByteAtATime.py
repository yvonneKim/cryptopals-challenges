# does padding oracle exploit to find out padding

import sys, os, base64, random

PKCS7 = __import__('1_PKCS7')
Oracle = __import__('3_Oracle')
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# sorry for using globals
rand_prefix = os.urandom(random.randint(1, 64))

def main():
    with open(sys.argv[1], 'rb') as f:
        global_key = os.urandom(16)
        data = b''.join((x.strip() for x in f.readlines()))
        e = encrypt(data, global_key)
        d = decrypt_msg(e, global_key)


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
    
    # Where is the last partially full block of the random prefix?
    no_inject_e = encrypt(b'', key)
    injected_e = encrypt(b'A', key)
    rp_start = 0
    while no_inject_e[rp_start:rp_start+bsize] == injected_e[rp_start:rp_start+bsize]:
        rp_start = rp_start + bsize


    # Figuring out random prefix size
    rp_total_size = 0 # rp_start + rp_end = rp_total_size
    rp_end = 0
    nextPhaseStart= rp_start + bsize
    e_cur = injected_e
    for x in range(2, bsize+2): # start with injected_e and two because adding one
        e_next = encrypt(b'A'*x, key)

        b_cur = e_cur[rp_start : rp_start + bsize]
        b_next = e_next[rp_start: rp_start + bsize]
        
        if b_cur == b_next:
            # for example, if this clause is entered on first iteration, RP was one byte away from boundary
            rp_end = (bsize - x +1) # always between 1 and bsize- is the finishing length
            rp_total_size = rp_start + rp_end
            break
        
        e_cur = e_next

    print(rp_start)
    print(rp_end)
    print(rp_total_size)

    n = rp_end # padding amount

    # Figuring out the secret message by feeding in byte at a time.
    result = b''
    secret_size = len(encrypt(b'A'*n, key)[nextPhaseStart:])
    offset = b'A' * (secret_size - 1 + 3) # add n to ceiling it to next bsize
    cur_offset = offset
    

    for x in range(0, secret_size):  # for every byte of the secret message
        checkBlockStart = nextPhaseStart + secret_size - bsize
        checkBlockEnd = nextPhaseStart + secret_size
        cur = encrypt(cur_offset, key)[checkBlockStart:checkBlockEnd]
        for i in range(0, 256):  # for every possible byte - which one matches for cur?
            c = i.to_bytes(1, byteorder='big')
            e = encrypt(offset + c, key)[checkBlockStart:checkBlockEnd]
            if e == cur:
                offset = (offset + c)[1:]
                cur_offset = cur_offset[1:]
                result += c
                break


    print(result)
    return result


if __name__ == '__main__':
    main()
