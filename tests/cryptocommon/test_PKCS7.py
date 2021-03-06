import sys
import os
import pytest

sys.path.append(os.path.abspath("src/cryptocommon"))


PKCS7 = __import__("PKCS7")


class TestPKCS7(object):
    # isPaddedPKCS7()
    def test_isPaddedPKCS7_1(self):
        test_data = b'x'*16
        bsize = 16
        result = PKCS7.isPaddedPKCS7(test_data, bsize)

        assert result == False

    def test_isPaddedPKCS7_2(self):
        test_data = b'x'*15 + bytes([1])
        bsize = 16
        result = PKCS7.isPaddedPKCS7(test_data, bsize)

        assert result == True

    def test_isPaddedPKCS7_3(self):
        test_data = b'x'*15 + bytes([2])
        bsize = 16
        result = PKCS7.isPaddedPKCS7(test_data, bsize)

        assert result == False

    def test_isPaddedPKCS7_4(self):
        test_data = bytes([16])*16
        bsize = 16
        result = PKCS7.isPaddedPKCS7(test_data, bsize)

        assert result == True

    def test_isPaddedPKCS7_5(self):
        test_data = b'x' + bytes([16])*15
        bsize = 16
        result = PKCS7.isPaddedPKCS7(test_data, bsize)

        assert result == False

    def test_isPaddedPKCS7_6(self):
        test_data = b'x'*7
        bsize = 7
        result = PKCS7.isPaddedPKCS7(test_data, bsize)

        assert result == False

    def test_isPaddedPKCS7_7(self):
        test_data = bytes([0])*16
        bsize = 16
        result = PKCS7.isPaddedPKCS7(test_data, bsize)
        assert result == False

    # stripPaddingPKCS7():
    def test_stripPaddingPKCS7_1(self):
        test_data = bytes([0])*16
        expected_data = test_data
        bsize = 16
        result = PKCS7.stripPaddingPKCS7(test_data, bsize)

        assert result == expected_data

    def test_stripPaddingPKCS7_2(self):
        test_data = bytes([16])*16
        expected_data = b''
        bsize = 16
        result = PKCS7.stripPaddingPKCS7(test_data, bsize)

        assert result == expected_data

    def test_stripPaddingPKCS7_3(self):
        test_data = b'x'*10 + bytes([6])*6
        expected_data = b'x'*10
        bsize = 16
        result = PKCS7.stripPaddingPKCS7(test_data, bsize)

        assert result == expected_data


    def test_stripPaddingPKCS7_4(self):
        test_data = b'x'*16 + bytes([16])*16
        expected_data = b'x'*16
        bsize = 16
        result = PKCS7.stripPaddingPKCS7(test_data, bsize)

        assert result == expected_data

    def test_stripPaddingPKCS7_5(self):
        test_data = bytes([32])*32
        expected_data = b''
        bsize = 32
        result = PKCS7.stripPaddingPKCS7(test_data, bsize)

        assert result == expected_data

    def test_stripPaddingPKCS7_6(self):
        test_data = bytes([1])*10
        expected_data = bytes([1])*9
        bsize = 10
        result = PKCS7.stripPaddingPKCS7(test_data, bsize)

        assert result == expected_data

    # stripIfPaddedPKCS7()
    def test_stripIfPaddedPKCS7_1(self):
        test_data = b'x'*9 + bytes([7])*7
        expected_data = b'x'*9
        bsize = 16
        result = PKCS7.stripIfPaddedPKCS7(test_data, bsize)

        assert result == expected_data

    def test_stripIfPaddedPKCS7_2(self):
        test_data = bytes([1]) * 100
        expected_data = bytes([1]) * 99
        bsize = 100
        result = PKCS7.stripIfPaddedPKCS7(test_data, bsize)

        assert result == expected_data

    def test_stripIfPaddedPKCS7_3(self):
        with pytest.raises(ValueError):
            test_data = bytes([1]) * 15
            bsize = 16
            result = PKCS7.stripIfPaddedPKCS7(test_data, bsize)

    def test_stripIfPaddedPKCS7_4(self):
        test_data = bytes([16]) * 16
        expected_data = b''
        bsize = 16
        result = PKCS7.stripIfPaddedPKCS7(test_data, bsize)

        assert result == expected_data

    def test_stripIfPaddedPKCS7_5(self):
        with pytest.raises(ValueError):
            test_data = b''
            expected_data = b''
            bsize = 16
            result = PKCS7.stripIfPaddedPKCS7(test_data, bsize)

    def test_stripIfPaddedPKCS7_6(self):
        test_data = bytes([0]) * 16
        expected_data = test_data
        bsize = 16
        with pytest.raises(ValueError):
            PKCS7.stripIfPaddedPKCS7(test_data, bsize)


    def test_padPKCS7_1(self):
        test_data = b'x'*5
        expected_data = b'x'*5 + bytes([11])*11
        bsize = 16
        result = PKCS7.padPKCS7(test_data, bsize)

        assert result == expected_data

    def test_padPKCS7_2(self):
        test_data = b'x'*16
        expected_data = b'x'*16 + bytes([16])*16
        bsize = 16
        result = PKCS7.padPKCS7(test_data, bsize)

        assert result == expected_data

    def test_padPKCS7_3(self):
        test_data = b'x'*15
        expected_data = b'x'*15 + bytes([1])
        bsize = 16
        result = PKCS7.padPKCS7(test_data, bsize)

        assert result == expected_data

    def test_padPKCS7_4(self):
        test_data = 'x'*15
        expected_data = b'x'*15 + bytes([1])
        bsize = 16
        result = PKCS7.padPKCS7(test_data, bsize)

        assert result == expected_data
