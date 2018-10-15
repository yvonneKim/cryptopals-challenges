import sys
import os
import pytest

sys.path.append(os.path.abspath("../../cryptocommon"))

from AES_ECB import decryptor as dec
from AES_ECB import encryptor as enc


class TestAES_ECB(object):    
    def test_encryptor(self):
        key = b'x'*16
        result = enc(b'YELLOW SUBMARIN', key, 16)

        assert len(result) == 16
        assert type(result) == bytes

    def test_encryptor_invalid_input(self):
        key = b'x'*16
        with pytest.raises(ValueError):
            enc(879, key, 16)

    def test_encryptor_string(self):
        key = b'x'*16
        data = 'x'*16
        expected_data = b'x'*16
        expected = enc(expected_data, key, 16)
        result = enc(data, key, 16)

        assert result == expected
                        
    
    def test_decryptor(self):
        key = b'x'*16
        encrypted = enc('YELLOW SUBMARIN', key, 16)
        result = dec(encrypted, key, 16)

        assert len(result) == 16
        assert type(result) == str

    def test_decryptor_invalid_data(self):
        key = b'x'*16
        encrypted = 'x'*16
        with pytest.raises(ValueError):
            dec(encrypted, key, 16)

    def test_decryptor_invalid_length(self):
        key = b'x'*16
        encrypted = b'x'*10
        with pytest.raises(ValueError):
            dec(encrypted, key, 16)            
            
