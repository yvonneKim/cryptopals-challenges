# implementation of PKCS7 padding to the next size
import math

def pad(data, bsize):
    c = (bsize - (len(data) % bsize)) % bsize
    print(bytes([c]))
    return data.encode('utf-8') + (c*bytes([c]))
