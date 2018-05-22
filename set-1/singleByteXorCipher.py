# stolen shamelessly from stackoverflow

import binascii, sys, collections


def main():
    with open(sys.argv[1], 'rb') as f:
        content = f.readlines()
    singleByteXorCipher(content)


def singleByteXorCipher(content):
    
    content = content.strip()
    result_list = {}
    nums = binascii.unhexlify(content)
    for key in range(256): # does for every possible key
        result = ""
        for num in nums: # byte by byte operation
            x = ord(num) ^ key
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
            
    return chr(result_key)

if __name__ == "__main__":
    main()
