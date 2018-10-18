import sys
import os
import pytest

sys.path.append(os.path.abspath("../../src/cryptocommon"))

from byteXor import xor


class TestByteXor(object):
    def test_invalid_inputs(self):
        with pytest.raises(TypeError):
            result = xor(34, 'test')

    def test_valid_inputs(self):
        result = xor(b'd', b'e') # 01000000, 01000001
        expected = int.to_bytes(1, length=1, byteorder='big', signed=True) # 00000001

        assert result == expected
