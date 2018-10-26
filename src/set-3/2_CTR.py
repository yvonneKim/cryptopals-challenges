from math import ceil
from itertools import count
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class CBC(object):
    def __init__(self, key, nonce, counter):
        self.key = key
        self.bsize = len(self.key)
        self.nonce = nonce
        self.counter = counter

    def encrypt(self, plaintext):
        key = self.key
        bsize = self.bsize
        nonce = self.nonce
        counter = self.counter

        for i in range(0, ceil(len(plaintext) / bsize)):
            # TODO Fix this for nonce's not just all zeroes
            print(nonce)
            print(bytes([next(counter)]))

            counter_block = int.from_bytes(nonce, byteorder='little') & int(next(counter))
            print(counter_block)


if __name__ == "__main__":
    key = 'YELLOW SUBMARINE'
    nonce = b'0' * int(len(key)/2)
    counter = count()
    cbc = CBC(key, nonce, counter)
    cbc.encrypt('oraoraoraoraoraoraoraoraoraoraoraoraoroaoraorroaroaorao')
