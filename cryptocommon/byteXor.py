# XORs two bytes objects together, returning a bytes

import sys, binascii

def xor(b1, b2):
    if (type(b1) != bytes) | (type(b2) != bytes):
        raise ValueError('Inputs are not both bytes!')
    
    result_b = bytearray()
    for i in range(len(b1)):
        result_b.append(b1[i] ^ b2[i])
    return bytes(result_b)

