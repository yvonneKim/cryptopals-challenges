# implementation of PKCS7 padding to the next size
# takes in bytes, returns bytes

import math


def isPaddedPKCS7(text, bsize):
    """ Takes in plaintext as bytes and blocksize and returns whether it has valid PKCS7 padding.
        Input where there is no padding is considered valid. (\x00 * 0 times)
        Input that is not a multiple of bsize is considered invalid.
    """
    if type(text) is str:
        text = text.encode('utf-8')

    if type(text) is not bytes:
        raise TypeError('Is neither string nor bytes!')

    if len(text) % bsize != 0:
        return False

    pad_byte = text[-1:]
    pad_byte_as_int = int.from_bytes(pad_byte, 'big', signed=True)
    if (pad_byte_as_int > bsize) | (pad_byte_as_int < 1):
        return True

    padding = (text[-pad_byte_as_int:])
    return padding == pad_byte*pad_byte_as_int


def stripPaddingPKCS7(text, bsize):
    """ Takes in plaintext as bytes and blocksize, returning the text without PKCS7 padding.
        This assumes that the plaintext is PKCS7 padding- verify before calling this.
    """
    pad_length = int.from_bytes(text[-1:], 'big', signed=True)

    if pad_length == 0:
        return text
    return text[:-pad_length]


def stripIfPaddedPKCS7(text, bsize):
    """ Combines checking and stripping for PKCS7 padding.
        Raises ValueError if the text does not have PKCS7 padding.
    """

    if isPaddedPKCS7(text, bsize):
        return stripPaddingPKCS7(text, bsize)

    raise ValueError('Padding is invalid!')


def padPKCS7(data, bsize):
    """ Takes text as bytes and PKCS7 pads it. 
        If text's size is a multiple of bsize, add a full block of padding (\x16)    
    """

    if type(data) == str:
        data = data.encode('utf-8')
        
    c = (bsize - (len(data) % bsize))
    return data + (c*bytes([c]))
