import sys
import os
import pytest

sys.path.append(os.path.abspath("../../src/cryptocommon"))
print(sys.path)

from AES_CBC import decrypt as dec
from AES_CBC import encrypt as enc


class TestAES_CBC(object):
    def test_decrypt(self):
        data = b'x'*16
        key = b'a'*16
        iv = b'0'*16

        encrypted = enc(data, key, iv)
        result = dec(encrypted, key, iv)

        assert len(result) == 16


    def test_decrypt_invalid_data(self):
        data = 'x'*16
        key = b'a'*16
        iv = b'0'*16

        with pytest.raises(ValueError):
            dec(data, key, iv)

    def test_decrypt_invalid_key(self):
        data = b'x'*16
        key = 'o'*16
        iv = b'0'*16

        with pytest.raises(ValueError):
            dec(data, key, iv)

    def test_decrypt_invalid_iv(self):
        data = b'x'*16
        key = b'a'*16
        iv = 'o'*16

        with pytest.raises(ValueError):
            dec(data, key, iv)

    def test_decrypt_invalid_data_length(self):
        data = b'x'*20
        key = b'a'*16
        iv = b'0'*16

        with pytest.raises(ValueError):
            dec(data, key, iv)

    def test_decrypt_invalid_iv_length(self):
        data = b'x'*10
        key = b'a'*10
        iv = b'0'*11

        with pytest.raises(ValueError):
            dec(data, key, iv)            

    def test_encrypt(self):
        data = b'x'*16
        key = b'a'*16
        iv = b'0'*16

        result = enc(data, key, iv)

        assert len(result) == 16
        assert type(result) == bytes

    def test_encrypt_invalid_data(self):
        data = 1
        key = b'x'*16
        iv = b'i'*16

        with pytest.raises(ValueError):
            enc(data, key, iv)

    def test_encrypt_invalid_data_length(self):
        data = b'r'*8
        key = b'x'*16
        iv = b'i'*16

        with pytest.raises(ValueError):
            enc(data, key, iv)

    def test_encrypt_invalid_iv_length(self):
        data = b'3'*16
        key = b'x'*16
        iv = b'i'*0

        with pytest.raises(ValueError):
            enc(data, key, iv)            
    
