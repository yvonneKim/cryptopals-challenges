# encrypts file with repeating-key xor as argument, line by line

import binascii, sys

with open(sys.argv[1], 'rb') as f:
    content = f.readlines()

key = bytes(sys.argv[2]) 
output = []
k_index = 0
for l in content:
    line = l
    out_line = ""
    for byte in line:
        x = ord(byte) ^ ord(key[k_index])
        out_line += format(x, 'x').zfill(2)
        
        if k_index == 2:
            k_index = 0
        else:
            k_index += 1

    output.append(out_line)
    

with open(sys.argv[1]+".out", 'w+') as outf:
    for line in output:
        outf.write(line+"\n")
