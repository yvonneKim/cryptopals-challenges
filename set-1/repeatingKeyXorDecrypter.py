# breaks repeating-key XOR cipher
# takes in file as argument

import sys, binascii, base64
from hammingDistance import hammingDistance as hamdist
byteXorCipher = __import__('3_singleByteXorCipher')


infile = sys.argv[1]

# load every line into a string array
with open(infile, 'r') as f:
    content = f.readlines()
    content = ''.join([c.strip() for c in content]) # is now one big string
    # un-b64 it
    content = base64.b64decode(content)

blocksize = 0
min_ham = 41
for bsize in range(2, 41):
    b1 = binascii.hexlify(content[0:bsize]).decode('utf-8')
    b2 = binascii.hexlify(content[bsize:bsize*2]).decode('utf-8')
    ham = hamdist(b1, b2) / bsize
    if ham <= min_ham:
        min_ham = ham
        blocksize = bsize

# then get the blocks
i = 0
blocks = []
while i + blocksize < len(content):
    start = i
    end = start + blocksize
    blocks.append(content[start:end])
    i += blocksize
    
# transpose them
char_blocks = [x[0] for x in zip(blocks)]
# each ith byte of the leftover block appended to it's corresponding
# char block. (since we're in hex, it's 2 chars per byte)
end_block = content[i:]
i = 0
while i < len(end_block):
    char_blocks[i] += end_block[i:i+2]
    i += 2
    

# single byte XOR cipher for each of the new blocks
key = ''
for b in char_blocks:
    k, _ = byteXorCipher.singleByteXorCipher(binascii.hexlify(b).decode('utf-8'))
    key += chr(k)

print("KEY IS : "+key)
