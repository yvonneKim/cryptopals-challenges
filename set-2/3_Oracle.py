# Takes in an AES-encrypted ciphertext and determines if it was encrypted
# with ECB or CBC.



import sys, os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def random_encrypt(ptext):
    # Encrypts with EBC and CBC 50/50 percent of the time, with a randomly
    # generated key.
    # Beforehand, pads the data with 1-15 (random) bytes both before and after.

    key = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.EBC(), backend=default_backend())
    out = cipher.encryptor().update(ptext)
    


def main():
    filename = sys.argv[1]
    with open(filename, 'rb') as f:
        analyze(b''.join((x.strip() for x in f.readlines())))
                

def analyze(data):
    
    


if __name__=='__main__':
    main()
    
