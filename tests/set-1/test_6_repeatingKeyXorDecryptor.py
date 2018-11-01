import sys
import os
import pytest

sys.path.append(os.path.abspath("src/set-1"))
solver = __import__('6_repeatingKeyXorDecrypter')


# class TestGetTransposedBlocks(object):
#     def test_1(self):
        # result = 12
        # result = solver.guess_keysize()
        # assert result == 12
