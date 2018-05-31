# Takes in an AES-encrypted ciphertext and determines if it was encrypted
# with ECB or CBC.

import sys, os, random
from collections import Counter
PKCS7 = __import__('1_PKCS7')
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def __CBC_encrypt(ptext, key):
    print("Encrypting with CBC...")
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    return cipher.encryptor().update(ptext)
    
def __ECB_encrypt(ptext, key):
    print("Encrypting with ECB...")
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    return cipher.encryptor().update(ptext)

def random_encrypt(ptext):
    # Encrypts with EBC and CBC 50/50 percent of the time, with a randomly
    # generated key.
    # Beforehand, pads the data with 1-15 (random) bytes both before and after.
    
    key = os.urandom(16) # has to be 16 for the challenge
    front = os.urandom(random.randint(5, 10))
    back = os.urandom(random.randint(5, 10))
                       
    ptext = front + ptext + back
    ptext = PKCS7.pad(ptext, len(key))
    algos = {0: __CBC_encrypt, 1: __ECB_encrypt}
    return algos[random.randint(0, 1)](ptext, key)

def analyze(data, bsize):
    # what size "blocks" to use for frequency analysis? start with 16?
    blocks = Counter([data[i:i+bsize] for i in range(0, len(data)-bsize+1, bsize)])
    if blocks.most_common(1)[0][1] >= 5: # adjust this number?
        return 'ECB'
    return 'CBC'

def main():
    filename = sys.argv[1]
    with open(filename, 'rb') as f:
        ctext = random_encrypt(b''.join((x.strip() for x in f.readlines())))
        analyzed = analyze(ctext, 8)
        if analyzed == 'CBC':
            print("This smells like a CBC to me!")
        elif analyzed == 'ECB':
            print("This smells like an ECB to me!")
        else:
            print("I.... I don't know ....")


if __name__=='__main__':
    main()
    
