import sys
import os
import pytest

sys.path.append(os.path.abspath("src/set-1"))

hexTo64 = (__import__('1_hexTo64')).hexTo64


class TestHexTo64(object):
    def test_valid_input(self):
        result = hexTo64('ffeeddccbbaa')

        assert result == '/+7dzLuq'

