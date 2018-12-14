import sys
import os
import pytest
from itertools import count

sys.path.append(os.path.abspath("src/set-3"))
CTR = __import__('2_CTR').CTR

@pytest.fixture
def ctr():
    key = b'YELLOW SUBMARINE'
    nonce = b'\x00'*8
    counter = count

    return __import__('2_CTR').CTR(key, nonce, counter)

class TestCTR():
    def test_get_xor_block_valid_1(self, ctr):
        nonce = b'\x00' * 4
        count_block = 1
        result = ctr.get_xor_block(nonce, count_block)

        expected = b'\x00\x00\x00\x00\x01\x00\x00\x00'
        assert expected == result

    def test_get_xor_block_valid_2(self, ctr):
        nonce = b'abcd'
        count_block = 2222
        result = ctr.get_xor_block(nonce, count_block)

        expected = b'abcd' + b'\xae\x08\x00\x00'
        assert expected == result

    def test_encrypt_decrypt(self, ctr):
        plaintext = 'aoraoroaroaoraoroaoroaroaoroaroaoroaoroaroororaoroaroaora'
        encrypted = ctr.encrypt(plaintext)
        decrypted = ctr.decrypt(encrypted)

        assert decrypted == plaintext

    def test_solved(self, ctr):
        plaintext = 'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='
        decrypted = ctr.decrypt(plaintext)
        print(decrypted)
        encrypted = ctr.encrypt(decrypted)

        assert encrypted == plaintext
