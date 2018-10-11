import os
import sys
from random import randint

sys.path.append(os.path.abspath("../cryptocommon"))
import byteXor as bxor


PKCS7 = __import__("PKCS7")
CBC = __import__("AES_CBC")
ECB = __import__("AES_ECB")

bsize = 16  # by default
key = os.urandom(bsize)
iv = b"\x00" * bsize


def f1(data):
    data = PKCS7.padPKCS7(data, bsize)
    data = CBC.encrypt(data, key, iv)
    return data


def f2(data):
    plaintext = CBC.decrypt(data, key, iv)
    isPadded = PKCS7.isPaddedPKCS7(plaintext, bsize)
    return isPadded


def decryptPair(C1, C2, bsize):
    # C2 is at index of C1 + bsize (16).

    if (type(C1) != bytes):
        C1 = C1.encode('utf-8')

    if (type(C2) != bytes):
        C2 = C2.encode('utf-8')

    if (len(C1) != bsize):
        raise ValueError('C1 is not bsize!')

    if (len(C2) != bsize):
        raise ValueError('C2 is not bsize!')

    pad = b''
    decrypted_text = b''
    for i in range(bsize, 0, -1):
        foundValid = False
        for j in range(0, 256):
            if foundValid:
                break
            inject = bytes([j])
            C1_modified = b'x'*(i-1) + inject + pad
            combined = C1_modified + C2
            hasValidPadding = f2(combined)
            if hasValidPadding:
                foundValid = True
                current_pad_num = bsize + 1 - i
                decrypted_byte = bxor.xor(bytes([current_pad_num]), inject)
                decrypted_text = decrypted_byte + decrypted_text
        if not foundValid:
            raise Exception("Couldn't find a valid padding!")

        # ex. /0x02 or /0x04/0x04/0x04
        pad_remainder = (bsize+1-i) * bytes([bsize+2-i])
        pad = bxor.xor(decrypted_text, pad_remainder)

    result = bxor.xor(decrypted_text, C1)
    return(result)


def main():
    with open(sys.argv[1], "r") as f:
        data = [x.strip() for x in f.readlines()]

    plaintext = b''
    data = data[randint(0, len(data)-1)]
    enc_data = f1(data)

    for x in range(len(enc_data), bsize, -bsize):
        C2 = enc_data[x-bsize:x]
        C1 = enc_data[x-(2*bsize):x-bsize]

        plaintext_block = decryptPair(C1, C2, bsize)
        plaintext = plaintext_block + plaintext

    result = PKCS7.stripPaddingPKCS7(plaintext, bsize).decode('utf-8')
    original = data[bsize:]  # sadly, the very first block can't be solved

    print("original: ")
    print(original)
    print("result: ")
    print(result)

    if original == result:
        print("SOLVED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


if __name__ == "__main__":
    main()
