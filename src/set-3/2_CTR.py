from math import ceil
from itertools import count
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class CTR(object):
    def __init__(self, key, nonce, counter):
        self.key = key
        self.bsize = len(self.key)

        if len(nonce) != (len(key)/2):
            raise ValueError('Nonce is not half of the key length!')

        self.nonce = nonce
        self.counter = counter

    def encrypt(self, plaintext):
        key = self.key
        nonce = self.nonce
        bsize = self.bsize
        counter = self.counter

        for i in range(0, ceil(len(plaintext) / bsize)):
            xor_block = self.get_xor_block(nonce, next(counter))
            

    def get_xor_block(self, nonce, count):
        """
        Nonce must be bytes string. Count is an int or long.
        Both must be the same size in bytes- half of the overall bsize.
        Returns bytes string that concats nonce + count.
        """

        half_bsize = len(nonce)        
        count = count.to_bytes(half_bsize, byteorder='little')
        xor_block = nonce + count

        return xor_block


if __name__ == "__main__":
    key = 'YELLOW SUBMARINE'
    nonce = bytes([0]) * int(len(key)/2)
    counter = count()
    ctr = CTR(key, nonce, counter)
    ctr.encrypt('oraoraoraoraoraoraoraoraoraoraoraoraoroaoraorroaroaorao')
