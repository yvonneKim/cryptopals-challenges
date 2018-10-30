from math import ceil
from itertools import count
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class CBC(object):
    def __init__(self, key, nonce, counter):
        self.key = key
        self.bsize = len(self.key)

        if len(nonce) != (len(key)/2):
            raise ValueError('Nonce is not half of the key length!')

        self.nonce = nonce
        self.counter = counter

    def encrypt(self, plaintext):
        key = self.key
        bsize = self.bsize
        nonce_part = self.nonce
        counter = self.counter

        for i in range(0, ceil(len(plaintext) / bsize)):
            xor_block = self.__get_xor_block(nonce, next(counter))
            print(xor_block)

    def __get_xor_block(self, nonce, count):
        """
        Nonce must be bytes string. Count is an int or long.
        Returns bytes string that concats nonce + (count as half-bsize byte string)
        """

        half_bsize = len(nonce) // 2
        
        count = count.to_bytes(half_bsize, byteorder='big')
        xor_block = nonce + count

        return xor_block


if __name__ == "__main__":
    key = 'YELLOW SUBMARINE'
    nonce = b'0' * int(len(key)/2)
    counter = count()
    cbc = CBC(key, nonce, counter)
    cbc.encrypt('oraoraoraoraoraoraoraoraoraoraoraoraoroaoraorroaroaorao')
