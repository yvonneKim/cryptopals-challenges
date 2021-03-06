import sys
import os
from byteXor import xor as bxor

sys.path.append(os.path.abspath("../cryptocommon"))

PKCS7 = __import__("PKCS7")
CBC = __import__("AES_CBC")

bsize = 16  # by default
key = os.urandom(bsize)
iv = b"\x00" * bsize


def main():
    # process cmd arguments- a file with the text to encrypt
    with open(sys.argv[1], "r") as f:
        data = "".join([x.strip() for x in f.readlines()])

    modified_data, padded_modified_data, e = encrypt(data)
    print("ORIGINAL DATA: ")
    print(modified_data)
    desired_data = modified_data.replace('"', "")
    desired_data = PKCS7.padPKCS7(desired_data.encode("utf-8"), bsize)
    print("DESIRED DATA: ")
    print(desired_data.decode("utf-8"))
    d = decrypt(e, desired_data)
    print("RESULT DECRYPTED: ")
    print(d)
    # output to file
    # with open(sys.argv[1]+'.out', 'wb') as f:
    #     f.write(ptext)


def encrypt(data):
    """ Takes in a plaintext string, quotes out ; and = chars,
        PKCS7 pads it, and CBC encrypts tiem.
        Returns the modified string and it's encryption.
    """
    # quoting out ; and = make it impossible to inject ";admin=true;"
    data = data.replace(";", '";"').replace("=", '"="')

    # add the pre and post strings
    pre = "comment1=cooking%20MCs;userdata="
    post = ";comment2=%20like%20a%20pound%20of%20bacon"
    data = pre + data + post

    # padding
    padded_data = PKCS7.padPKCS7(data.encode("utf-8"), bsize)

    # encryption with iv of all zeroes
    encrypted = CBC.encrypt(padded_data, key, iv)

    return data, padded_data, encrypted


def print_blocks(data, bsize):
    for i in range(len(data), 0, -bsize):
        print(data[i - bsize: i].decode("utf-8"))


def decrypt(data, desired):
    dat = data[len(data) - bsize:len(data)]
    result = [dat]
    for i in range(len(data), 0, -bsize):
        des = desired[i - bsize:i]
        decrypted_dat = CBC.decrypt(dat, key, iv)
        dat = bxor(des, decrypted_dat)
        result.append(dat)

    result.reverse()
    result = b"".join(result)
    return CBC.decrypt(result, key, iv)


if __name__ == "__main__":
    main()
