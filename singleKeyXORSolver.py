# does single byte XOR agiainst hex string to solve puzzle
# compares each result to a character frequency metric, taken from:
# https://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
# then, prints the winner back to ascii string

import hexXORkey, sys

# iterates through 2^8 times for each possible byte character
# then, prints the most likely readable string (solved puzzle?)
# right now, just picks the one with the most 'e's

i = 0
e_cnt = 0
result_e_cnt = 0;
result_i = 0;

while i < 255:
    hex_arg = format(i, '02x')
    data = hexXORkey.hexXORkey(sys.argv[1], hex_arg)
    print (data)
    print (data.decode('hex'))
    e_cnt = data.count('e')
    
    if e_cnt > result_e_cnt:
        result_i = i
        result_e_cnt = e_cnt
    i += 1
print("RESULT : ")
print hexXORkey.hexXORkey(sys.argv[1], format(result_i, '02x'))
