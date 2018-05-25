# implementation of PKCS7 padding to the next size
import math

def pad(data, bsize):
#    data = data.encode('utf-8')
    c = (bsize - (len(data) % bsize)) % bsize
    print(bytes([c]))
    return data.encode('utf-8') + (c*bytes([c]))
    # width = (len(data) + bsize - 1) // bsize 
    # return data.ljust(width, c)
