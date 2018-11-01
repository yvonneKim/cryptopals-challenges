import sys
import os
import pytest
from itertools import count

sys.path.append(os.path.abspath("src/set-3"))
CTR = __import__('2_CTR').CTR

@pytest.fixture
def ctr():
    key = b'YELLOW SUBMARINE'
    nonce = b'00000000'
    counter = count()        

    return __import__('2_CTR').CTR(key, nonce, counter)

class TestCTR():
    def test_get_xor_block_valid_1(self, ctr):
        nonce = b'\x00' * 4
        count = 1
        result = ctr.get_xor_block(nonce, count)

        expected = b'\x00\x00\x00\x00\x01\x00\x00\x00'
        assert expected == result

    def test_get_xor_block_valid_2(self, ctr):
        nonce = b'abcd'
        count = 2222
        result = ctr.get_xor_block(nonce, count)

        expected = b'abcd' + b'\xae\x08\x00\x00'
        assert expected == result
        
