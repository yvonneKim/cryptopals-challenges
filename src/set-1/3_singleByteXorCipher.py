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
    """
    Takes in a hex string that has been XOR'd against a single character and
    returns (key, decrypted string).
    """
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
            try:
                x = num ^ key
            except:
                x = ord(num) ^ key
            line += chr(x)

        # summing unigrams
        cnt = sum([char_freq[c] for c in line if c in char_freq])

        if cnt >= max_cnt:
            max_cnt = cnt
            result_string = line
            result_key = key


    return (chr(result_key), result_string)


if __name__ == "__main__":
    main()
