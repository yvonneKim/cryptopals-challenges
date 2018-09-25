import sys, os, base64, random

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
    pad_length = int(text[-1:])

    return text[:-pad_length]

def stripIfPaddedPKCS7(text, bsize):
    if isPaddedPKCS7(text, bsize): 
        return stripPaddingPKCS7(text, bsize)

    raise ValueError('Padding is invalid!')


def main():
    bsize = 16
    
    if len(sys.argv) > 1:
        text = (sys.argv[1])
        result = stripIfPaddedPKCS7(text, bsize)
        print(result)


if __name__ == '__main__':
    main()
