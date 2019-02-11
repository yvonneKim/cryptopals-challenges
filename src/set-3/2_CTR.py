from math import ceil
from itertools import count, tee
from struct import pack
import sys
import os

sys.path.append(os.path.abspath("src/cryptocommon"))
from byteXor import xor
from blocks import Blocks
from AES_ECB import encryptor as enc
from AES_ECB import decryptor as dec


class CTR(object):
    def __init__(self, key, nonce=0):
        self.key = key
        self.bsize = len(self.key)
        self.nonce = nonce
        
    def gen_keystream_block(self):
        block_count = 0
        while True:
            enc_block = bytes(pack('<Q', self.nonce)) + bytes(pack('<Q', block_count))
            enc_keystream = enc(enc_block, self.key)
            for byte in enc_keystream:
                yield byte
            block_count += 1

    def decrypt(self, ciphertext):
        result = bytearray()
        gen_ksb = self.gen_keystream_block()
        # cant use byteXor's xor because it won't take a generator
        for byte in ciphertext:
            n = next(gen_ksb)
            result.append(byte ^ n)
        return bytes(result).decode('utf-8')

    def encrypt(self, plaintext):
        result = bytearray()
        gen_ksb = self.gen_keystream_block()
        # cant use byteXor's xor because it won't take a generator
        for byte in plaintext:
            result.append(ord(byte) ^ next(gen_ksb))
        return result
