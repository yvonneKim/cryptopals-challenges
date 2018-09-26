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
    data = PKCS7.padPKCS7(rand_prefix + data + secret, len(key))
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

    print("RP_START: "+str(rp_start))
    print("RP_END: "+str(rp_end))
    print("RP_TOTAL: "+str(rp_total_size))
    print()
    print("STARTING SOLVE AT: "+str(nextPhaseStart))


    n = bsize - rp_end # padding amount
    print("Amount to pad by: "+str(n))
    print("Length with boundary padding in input: "+str(len(encrypt(b'A'*n, key))))
    s = len(encrypt(b'A'*n, key)[nextPhaseStart:])
    print("length from bondary start onwards: "+str(s))
    secret_size = 0
    
    # what is the size of the secret?
    for i in range(1, bsize):
        wit = encrypt(b'A'*(n+i+1), key)
        without = encrypt(b'A'*(n+i), key)
        
        if (len(wit) != len(without)):
            secret_size = len(encrypt(b'A'*n, key)[nextPhaseStart:]) - bsize + i
            print("FOUND secret size: "+str(secret_size))


    # Figuring out the secret message by feeding in byte at a time.
    result = b''
    offset = b'A' * (s - 1 + n) # add n to ceiling it to next bsize
    cur_offset = offset
    checkBlockStart = nextPhaseStart + s - bsize
    checkBlockEnd = nextPhaseStart + s
    print("block to check: "+str(checkBlockStart)+"-"+str(checkBlockEnd))

    for x in range(0, secret_size):  # for every byte of the secret message

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
