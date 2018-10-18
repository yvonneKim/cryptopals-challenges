# XORs two bytes objects together, returning a bytes
def xor(b1, b2):
    if (type(b1) != bytes) | (type(b2) != bytes):
        raise TypeError('Inputs are not both bytes!')

    if (len(b1) != len(b2)):
        raise ValueError('Lengths are not the same!')

    result_b = bytearray()
    for i in range(len(b1)):
        result_b.append(b1[i] ^ b2[i])
    return bytes(result_b)
