# Takes in an AES-encrypted ciphertext and determines if it was encrypted
# with ECB or CBC.

import sys, os, random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def __CBC_encrypt(ptext):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    return cipher.encryptor().update(ptext)
    
def ECB_encrypt(ptext):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    return cipher.encryptor().update(ptext)

def random_encrypt(ptext):
    # Encrypts with EBC and CBC 50/50 percent of the time, with a randomly
    # generated key.
    # Beforehand, pads the data with 1-15 (random) bytes both before and after.
    
    key = os.urandom(16) # has to be 16 for the challenge
    ptext = os.urandom(random.randint(5, 10)) + ptext + os.urandom(random.randint(5, 10))
    print(ptext)
    algos = ['__CBC_encrypt', '__ECB_encrypt']
    ctext = getattr(self, algos[random.randint(0, 1)])(ptext)
    print(ctext)

def main():
    filename = sys.argv[1]
    with open(filename, 'rb') as f:
        random_encrypt(b''.join((x.strip() for x in f.readlines())))
        analyze(b''.join((x.strip() for x in f.readlines())))
                

def analyze(data):
    pass
    


if __name__=='__main__':
    main()
    
