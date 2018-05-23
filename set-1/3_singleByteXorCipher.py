# stolen shamelessly from stackoverflow
# takes in file, prints out the key used to decrypt, and returns decrypted message
import binascii, sys, collections
from char_frequencies import char_frequencies as char_freq

def main():
    with open(sys.argv[1], 'rb') as f:
        with open(sys.argv[1]+'.out', 'w+') as outf:
            for content in f.readlines():
                k, out = singleByteXorCipher(content)
                outf.write("KEY IS : "+str(k)+'\n')
                outf.write(out+'\n')
        

def singleByteXorCipher(content):
    result_string = ''
    result_key = ''
    max_cnt = 0
    try:
        nums = binascii.unhexlify(content.strip())
    except:
        print("TROUBLESOME LINE: "+content.strip())
        
    for key in range(256): # does for every possible key
        line = ""
        for num in nums: # byte by byte operation
            x = num ^ key
            line += chr(x)

        # summing unigrams
        cnt = sum([char_freq[c] for c in line if c in char_freq])

        if cnt >= max_cnt:
#            print(line)            
            max_cnt = cnt
            result_string = line
            result_key = key


    return (chr(result_key), result_string)
            
        
    # ETAOIN SHRDLU
#    freq_char = {'e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'u', ' '}
    # result_string = ""
    # result_cnt = 0
    # result_key = 0
    # for result in result_list:
    #     cnt = 0
    #     char_cnt = collections.Counter(result)
    #     for char in char_cnt.keys():
    #         if char in char_freq:
    #             cnt += char_cnt[char]
    #     if cnt >= result_cnt:
    #         result_cnt = cnt
    #         result_string = result
    #         result_key = result_list[result]

    # return (result_key, result_string)

if __name__ == "__main__":
    main()
