# computes hamming distance of two strings
# strings must be equal length. Otherwise, returns -1

def hammingDistance(s1, s2):

            
    if len(s1) != len(s2):
        print("STRINGS NOT SAME LENGTH. BYE.")
        return -1

    cnt = 0
    for i in range(len(s1)):
        if type(s1) == bytes: # if in bytes
            x = s1[i] ^ s2[i]
        else: # else, in string
            x = ord(s1[i]) ^ ord(s2[i])
        cnt += bin(x).count("1")

    return cnt
