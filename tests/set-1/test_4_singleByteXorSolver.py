import sys
import os
import pytest

sys.path.append(os.path.abspath("src/set-1"))

cipher = (__import__('3_singleByteXorCipher')).singleByteXorCipher
