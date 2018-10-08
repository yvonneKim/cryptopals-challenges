import os
import sys
from random import randint
from cryptocommon import byteXor as bxor
sys.path.append(os.path.abspath("../cryptocommon"))

PKCS7 = __import__("PKCS7")
CBC = __import__("AES_CBC")

bsize = 16  # by default
key = os.urandom(bsize)
iv = b"\x00" * bsize


def f1(data):
    data = PKCS7.padPKCS7(data.encode('utf-8'), bsize)
    data = CBC.encrypt(data, key, iv)
    return data


def f2(data):
    data = CBC.decrypt(data, key, iv)
    print(data)
    return PKCS7.isPaddedPKCS7(data, bsize)


def decryptPair(C1, C2, bsize):
    # C2 is at index of C1 + bsize (16).

    if (type(C1) != bytes):
        C1 = C1.encode('utf-8')

    if (type(C2) != bytes):
        C2 = C2.encode('utf-8')

    pad = b''
    decrypted_text = bytes(bsize)
    for i in range(bsize-1, 0, -1):
        for j in range(0, 256):
            inject = bytes([j])
            print(inject)
            C1_modified = C1[:i] + inject + pad
            combined = b''.join([C1_modified, C2])
            print("Trying for: ")
            print(C1_modified)
            print(combined)
            hasValidPadding = f2(combined)
            if hasValidPadding:
                print("FOUND!")
                print(inject)
                # find out the value of decrypted(C2[i-1:i])
                decrypted_byte = bxor.xor(bytes([bsize-i]), inject)
                decrypted_text = decrypted_text + decrypted_byte
                print("Decrypted text is now:")
                print(decrypted_text)
                break
        pad = bxor.xor(decrypted_byte, (bsize-i) * bytes([bsize-i]))
    print(decrypted_text)
    result = bxor(decrypted_text, C1)
    print(result)
    return(result.decode('utf-8'))


def main():
    with open(sys.argv[1], "r") as f:
        data = [x.strip() for x in f.readlines()]

    plaintext = ''
    data = data[randint(0, len(data)-1)]
    print("data is: "+data)
    for x in range(len(data)-1, 0, -bsize):
        C2 = data[x-bsize:x]
        C1 = data[x-(2*bsize):x-bsize]
        print("C1 is: "+C1)
        print("C2 is: "+C2)
        plaintext_block = decryptPair(C1, C2, bsize)
        plaintext = plaintext_block + plaintext


if __name__ == "__main__":
    main()
