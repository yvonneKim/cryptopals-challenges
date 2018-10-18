# does single byte XOR agiainst hex string to solve puzzle
# compares each result to a character frequency metric, taken from:
# https://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
# then, prints the winner back to ascii string

import hexXorKey, sys
sxor = __import__('3_singleByteXorCipher')

# iterates through 2^8 times for each possible byte character
# then, prints the most likely readable string (solved puzzle?)

max_cnt = 0
result = ''

with open(sys.argv[1], 'rb') as f:
    lines = f.readlines()
    for l in lines:
        decrypted = sxor.singleByteXorCipher(l)[1]

        cnt = sum(c.isalpha() for c in decrypted)
        if cnt >= max_cnt:
            max_cnt = cnt
            result = decrypted

with open(sys.argv[1]+'.out', 'w') as f:
    f.write(result)
