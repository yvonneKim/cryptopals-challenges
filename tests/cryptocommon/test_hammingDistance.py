import sys
import os
import pytest

sys.path.append(os.path.abspath("src/cryptocommon"))

from hammingDistance import hammingDistance as hamDist


class TestHammingDistance(object):
    def test_not_same_length(self):
        with pytest.raises(ValueError):
            hamDist(b'3', b'ljlkdjsfkgj')

    def test_b1_as_string(self):
        result = hamDist('something', b'something')
        expected = 0

        assert result == expected

    def test_b2_as_string(self):
        result = hamDist(b'd', 'e')
        expected = 1

        assert result == expected
