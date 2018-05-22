# stolen shamelessly from stackoverflow
# takes in file, prints out the key used to decrypt, and returns decrypted message

import binascii, sys, collections


def main():
    with open(sys.argv[1], 'rb') as f:
        with open(sys.argv[1]+'.out', 'w+') as outf:
            for content in f.readlines():
                out = singleByteXorCipher(content)
                outf.write(out+'\n')
        

def singleByteXorCipher(content):

    result_list = {}
    nums = binascii.unhexlify(content.strip())
    for key in range(256): # does for every possible key
        result = ""
        for num in nums: # byte by byte operation
            x = num ^ key
            result += chr(x)
        result_list[result] = key

    # ETAOIN SHRDLU
    freq_char = {'e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'u', ' '}
    result_string = ""
    result_cnt = 0
    result_key = 0
    for result in result_list:
        cnt = 0
        char_cnt = collections.Counter(result)
        for char in char_cnt.keys():
            if char in freq_char:
                cnt += char_cnt[char]
        if cnt >= result_cnt:
            result_cnt = cnt
            result_string = result
            result_key = result_list[result]

    print("RESULT KEY IS "+ chr(result_key))
    return result_string

if __name__ == "__main__":
    main()
