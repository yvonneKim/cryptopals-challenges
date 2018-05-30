# Takes in an AES-encrypted ciphertext and determines if it was encrypted
# with ECB or CBC.

import sys, os, random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def __CBC_encrypt(ptext, key):
    print("CBC")
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    return cipher.encryptor().update(ptext)
    
def __ECB_encrypt(ptext, key):
    print("ECB")
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    return cipher.encryptor().update(ptext)

def random_encrypt(ptext):
    # Encrypts with EBC and CBC 50/50 percent of the time, with a randomly
    # generated key.
    # Beforehand, pads the data with 1-15 (random) bytes both before and after.
    
    key = os.urandom(16) # has to be 16 for the challenge
    ptext = os.urandom(random.randint(5, 10)) + ptext + os.urandom(random.randint(5, 10))
    algos = {0: __CBC_encrypt, 1: __ECB_encrypt}
    return algos[random.randint(0, 1)](ptext, key)

def analyze(ctext):
    

def main():
    filename = sys.argv[1]
    with open(filename, 'rb') as f:
        ctext = random_encrypt(b''.join((x.strip() for x in f.readlines())))
        if analyze(ctext) == 'CBC':
            print("This smells like a CBC to me!")
        else:
            print("This smells like an ECB to me!")


def analyze(data):
    pass
    


if __name__=='__main__':
    main()
    
