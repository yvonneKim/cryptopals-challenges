#converts a plain text file in hex to base64
#fails if it's not a valid input
#outputs to <name of file>.out

import sys, base64, binascii

def hexTo64(data):
    """
    Takes in a hex string and returns it base-64 encoded.
    """
    data = binascii.unhexlify(data)
    output = base64.b64encode(data).decode('utf-8')
    return output


if __name__=='__main__':
    input = sys.argv[1]
    with open(input, 'rb') as f:
        data = f.read().strip() # data is a hex string

    output = hexTo64(data)
        
    with open(input+".out", 'w+') as outf:
        outf.write(str(output)+"\n")    
