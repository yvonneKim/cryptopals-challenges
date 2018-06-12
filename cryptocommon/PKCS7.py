# implementation of PKCS7 padding to the next size
# takes in bytes, returns bytes

import math

def pad(data, bsize):
    c = (bsize - (len(data) % bsize)) % bsize
    return data + (c*bytes([c]))
