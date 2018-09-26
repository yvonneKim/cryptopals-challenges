import sys, os, base64, random
sys.path.append(os.path.abspath('../cryptocommon'))

PKCS7 = __import__('PKCS7')
CBC = __import__('AES_CBC')
from byteXor import xor as bxor
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def main():
    # process cmd arguments- a file with the text to encrypt
    with open(sys.argv[1], 'r') as f:
        data = ''.join([x.strip() for x in f.readlines()])
    
    bsize = 16 # by default
    key = os.urandom(bsize)

    # add the pre and post strings
    pre = "comment1=cooking%20MCs;userdata="
    post = ";comment2=%20like%20a%20pound%20of%20bacon"    
    predata = (pre+data+post)

    # quoting out ; and = make it impossible to inject ";admin=true;"in the input data    
    data = predata.replace(';', '";"').replace('=', '"="')

    # padding 
    data = PKCS7.padPKCS7(data.encode('utf-8'), bsize)
    predata = PKCS7.padPKCS7(predata.encode('utf-8'), bsize)

    print("First block:")
    print(data[:16])
    print()

    print("Desired first block:")
    print(predata[:16])
    print()

    # get XOR mask by XORing first block w/ desired first block
    xor_mask = bxor(data[:16], predata[:16])
    print("XOR mask:")
    print(xor_mask)
    print()

    print("XOR'd to: ")
    result = bxor(data[:16], xor_mask)
    print(result)
    print()

    print("Does this match our desired block?")
    print(result == predata[:16])

    # encryption with iv of all zeroes
    encrypted = CBC.encrypt(data, key, iv = b'\x00' * bsize)

    # output to file
    # with open(sys.argv[1]+'.out', 'wb') as f:
    #     f.write(ptext)

if __name__=='__main__':
    main()
