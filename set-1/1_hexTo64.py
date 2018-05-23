#converts a plain text file in hex to base64
#fails if it's not a valid input
#outputs to <name of file>.out

import sys, base64, binascii

input = sys.argv[1]
with open(input, 'rb') as f:
    data = f.read().strip() # data is a hex string 
    h = binascii.unhexlify(data) # then, converted to bin
    output = base64.b64encode(h).decode('utf-8') # then, converted from bin to b64
    
with open(input+".out", 'w+') as outf:
    outf.write(str(output)+"\n")
