# breaks repeating-key XOR cipher
# takes in file as argument

import sys, binascii, hammingDistance, singleByteXorCipher

infile = sys.argv[1]

# load every line into a string array
with open(infile, 'rb') as f:
    content = f.readlines()
#    content = map(str.strip, content)
    content = ''.join(content) # is now one big string

# trying keysizes from 2 to, say, 40
data_len = len(content)
max_key_len = 41
hams = {}
for keysize in range(2, max_key_len):
    total_hams = 0
    final_i = 0
    for i in range(0, data_len, 2*keysize):
        if final_i >= 4: # program runs for too long otherwise
            break
        b1 = content[i:i+keysize]
        b2 = content[i+keysize:i+(2*keysize)]
        if len(b1) != len(b2): # reached end?
            break
        ham_dist = float(hammingDistance.hammingDistance(b1, b2))
        ham_dist /= keysize
        hams[keysize] = ham_dist
        final_i += 1
        total_hams += ham_dist
    final_ham = total_hams / final_i
    hams[keysize] = final_ham

print(hams)
hams = sorted(hams.iteritems(), key=lambda (k,v): (v,k))
probable_keysizes = [hams[0][0], hams[1][0], hams[2][0]] # 3 of the most probable keysizes
print(probable_keysizes)
total_block = ''.join(content) # makes all strings into one big string
chunks = [total_block[i:i+keysize] for i in range(0, len(total_block), keysize)]

# now, transposing the blocks. First byte from each chunk goes into block 1, so on
for keysize in probable_keysizes:
    blocks = []
    for i in range(0, keysize):
        bl = ""
        for ch in chunks:
            if i < len(ch):
                bl += ch[i]

        blocks.append(binascii.hexlify(bl))

    # then, solve each block as single-key XOR
    solved_blocks = []
    for bl in blocks:
        solved_blocks.append(singleByteXorCipher.singleByteXorCipher(bl))

    final_string = ""
    for i in range(0, keysize):
        for bl in solved_blocks:
            if i < len(bl):
                final_string += bl[i]

    print(final_string)
