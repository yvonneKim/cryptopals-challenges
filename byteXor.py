# XORs two bytes objects together, returning a bytes

import sys, binascii

def xor(b1, b2):
    result_b = bytearray()
    for i in range(len(b1)):
        result_b.append(b1[i] ^ b2[i])
    return bytes(result_b)

