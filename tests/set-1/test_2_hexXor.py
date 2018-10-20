import sys
import os
import pytest

sys.path.append(os.path.abspath("src/set-1"))

hexXor = (__import__('2_hexXor')).hexXor

class TestHexXor(object):
    def test_valid_input(self):
        result = hexXor('abcdef', 'abcdef')
        expected = '000000'

        assert result == expected
