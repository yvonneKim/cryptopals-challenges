# implementation of PKCS7 padding to the next size
# takes in bytes, returns bytes

import math

def isPaddedPKCS7(text, bsize):
    """ Takes in plaintext as bytes and blocksize and returns whether it has valid PKCS7 padding.
        Input where there is no padding is considered valid. (\x00 * 0 times)
        Input that is not a multiple of bsize is considered invalid.
    """
    text = text.encode('utf-8')

    if len(text) % bsize != 0:
        return False

    pad_byte = text[-1:]
    pad_byte_as_int = int(pad_byte)
    padding = (text[-pad_byte_as_int:])
    
    return padding == pad_byte*pad_byte_as_int    

def stripPaddingPKCS7(text, bsize):
    """ Takes in plaintext as bytes and blocksize, returning the text without PKCS7 padding.
        This assumes that the plaintext is PKCS7 padding- verify before calling this.
    """
    pad_length = int(text[-1:])

    return text[:-pad_length]

def stripIfPaddedPKCS7(text, bsize):
    """ Combines checking and stripping for PKCS7 padding.
        Raises ValueError if the text does not have PKCS7 padding.
    """

    if isPaddedPKCS7(text, bsize): 
        return stripPaddingPKCS7(text, bsize)

    raise ValueError('Padding is invalid!')

def padPKCS7(data, bsize):
    """ Takes text as bytes and PKCS7 pads it. """

    c = (bsize - (len(data) % bsize)) % bsize
    return data + (c*bytes([c]))
