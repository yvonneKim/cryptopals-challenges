# encrypts file with repeating-key xor as argument, line by line

import binascii, sys


def main():
    with open(sys.argv[1], 'rb') as f:
        content = f.readlines()
        output = encrypt(content, sys.argv[2])

        with open(sys.argv[1]+".out", 'w+') as outf:
            for line in output:
                outf.write(line+"\n")
    

def encrypt(content, key):
    key = bytes(key, 'utf-8') 
    output = []
    k_index = 0
    for l in content:
        line = l
        out_line = ""
        for byte in line:
            x = byte ^ key[k_index]
            out_line += format(x, 'x').zfill(2)

            if k_index == 2:
                k_index = 0
            else:
                k_index += 1

        output.append(out_line)
    return output
    
if __name__=="__main__":
    main()
