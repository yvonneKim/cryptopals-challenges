import math.ceil as ceil

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class CBC(object):
    def __init__(self, key, nonce):
        self.key = 'YELLOW SUBMARINE'
        self.bsize = len(self.key)
        self.nonce = b'0'*(self.bsize/2)
        self.counter = iter(range(0, 2**(self.bsize/2)))

    def encrypt(self, plaintext):
        key = self.key
        bsize = self.bsize
        nonce = self.nonce
        counter = self.counter

        for ceil(len(plaintext) / bsize):            
            counter_block = nonce + b([counter.next()])
            
            
