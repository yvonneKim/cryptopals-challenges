# takes two file args of hex strings, XOR's them
# result is another hex string in file named arg1XORarg2

import sys, binascii

def hexXor(d1, d2):
    """
    Takes in two hex strings and returns a hex string that is the
    result of XOR-ing their bytes.
    """
    b1 = bytearray(binascii.unhexlify(d1))
    b2 = bytearray(binascii.unhexlify(d2))

    result = bytearray()
    for i in range(len(b1)):
        result.append(b1[i] ^ b2[i])

    return binascii.hexlify(result).decode('utf-8')


if __name__=='__main__':
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]

    with open(arg1, 'rb') as f1:
        with open(arg2, 'rb') as f2:
            d1 = f1.read().strip()
            d2 = f2.read().strip()
            result = hexXor(d1, d2)

    with open(arg1+"XOR"+arg2, 'w+') as outf:
        outf.write(result)
