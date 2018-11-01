from math import ceil
from itertools import count
import sys
import os

sys.path.append(os.path.abspath("src/cryptocommon"))
from byteXor import xor
from blocks import Blocks
from AES_ECB import encryptor as enc
from AES_ECB import decryptor as dec


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
        blocks = Blocks(plaintext).get_iterator()
        encrypted_blocks = []
        
        for plaintext_block in blocks:
            xor_block = self.get_xor_block(nonce, next(counter))
            encrypted_xor_block = enc(xor_block, key, bsize, padded=False)
            encrypted_xor_block = encrypted_xor_block[:len(plaintext_block)]
            cipher_block = xor(encrypted_xor_block, plaintext_block)
            encrypted_blocks.append(cipher_block)

        return b''.join(encrypted_blocks)
            
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
    key = b'YELLOW SUBMARINE'
    plaintext = 'oraoraoraoraoraoraoraoraoraoraoraoraoroaoraorroaroaorao'
    nonce = bytes([0]) * int(len(key)/2)
    counter = count()
    ctr = CTR(key, nonce, counter)
    encrypted = ctr.encrypt(plaintext)
    print(encrypted)
