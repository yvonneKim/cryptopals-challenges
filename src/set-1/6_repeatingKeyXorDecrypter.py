# breaks repeating-key XOR cipher
# takes in file as argument

import sys, binascii, base64, itertools
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

# forgive me lord for I have cheated: https://raywang.tech/2017/03/07/set1_writeup/#challenge-16-break-repeating-key-xor

for bsize in range(2, 41):
    b1 = content[0:bsize]
    b2 = content[bsize:bsize*2]
    b3 = content[bsize*2:bsize*3]
    b4 = content[bsize*3:bsize*4]    
    bs = [b1, b2, b3, b4]
    combs = list(itertools.combinations(bs, 2))
    hamsum = sum(itertools.starmap(hamdist, combs))
    normalized_ham = hamsum / ( len(combs) * bsize )

    if normalized_ham <= min_ham:
        print("NEW HAM :"+str(normalized_ham))
        print("FOR BSIZE :"+str(bsize))
        min_ham = normalized_ham
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
char_blocks = [bytes(x) for x in (list(zip(*[list(b) for b in blocks])))]


# each ith byte of the leftover block appended to it's corresponding
end_block = content[i:]
i = 0
while i < len(end_block):
    char_blocks[i] += end_block[i:i+1]
    i += 2
    
# single byte XOR cipher for each of the new blocks
with open(infile+'.out', 'w') as f:

    key = ''
    print(char_blocks)
    for b in char_blocks:
        by = binascii.hexlify(b).decode('utf-8')
        k, s = byteXorCipher.singleByteXorCipher(by)
        key += k
        f.write(s)
    
    print("KEY IS : "+key)


