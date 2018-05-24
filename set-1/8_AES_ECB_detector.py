# takes in a file, detects the block region that's been encoded with ECB

import sys, binascii
AES_ECB = __import__('7_AES_ECB_decryptor')

with open(sys.argv[1], 'rb') as f:
    data = b''.join([binascii.unhexlify(r.strip()) for r in f.readlines()])

# break into blocks of size... 128, 256?
block_gen = lambda d, b, e: (d[i:i+b] for i in range(0, e-b, b))
max_byte_freq = {}
for b in block_gen(data, 2048, len(data)):

    # distribution dict
    byte_freq = {}
    for k in b:
        k = bytes([k])
        if k in byte_freq:
            byte_freq[k] += 1
        else:
            byte_freq[k] = 1

    # remember the block that has the highest byte freq of any one particular byte
    c = max(byte_freq.keys(), key=lambda key: byte_freq[key])
    c_freq = byte_freq[c]
    max_byte_freq[b] = (c, c_freq)

k = max(max_byte_freq.keys(), key=lambda k: max_byte_freq[k])
print("The block with the highest freq of a single byte is: ")
print(b)
print("With "+str(max_byte_freq[k][0])+" coming up "+str(max_byte_freq[k][1])+" times")
