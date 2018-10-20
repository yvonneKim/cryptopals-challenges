import sys
import os
import pytest

sys.path.append(os.path.abspath("src/set-1"))

cipher = (__import__('3_singleByteXorCipher')).singleByteXorCipher

class TestHexXor(object):
    def test_valid_input(self):
        result = cipher('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
        expected_key = 'X'
        expected_string = "Cooking MC's like a pound of bacon"

        assert result == (expected_key, expected_string)
