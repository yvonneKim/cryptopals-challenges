# takes file with hex string and second argument as single char
# result is first arg XOR'd with char 

import sys, binascii

def hexXorKey(arg1, arg2):
    key = bytearray(binascii.unhexlify(arg2.strip()))

    # read input file
    with open(arg1, 'rb') as f:
        data = f.read().decode('utf-8').rstrip()
        print(data)
        byte_data = bytearray(binascii.unhexlify(data))

    # XOR operation done one by one
    result = bytearray()
    for i in range(len(byte_data)):
        result.append(byte_data[i] ^ key[0])

    # return hex string output
    final_result = ""
    for b in result:
        final_result+=(format(b, 'x'))

    return final_result
