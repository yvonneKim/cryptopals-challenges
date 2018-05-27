# computes hamming distance of two byte strings
# strings must be equal length. Otherwise, returns -1

def hammingDistance(s1, s2):
            
    if len(s1) != len(s2):
        raise Exception("bytes not same length")

    if type(s1) != bytes:
        s1 = bytes(s1)
        s2 = bytes(s2)

    cnt = 0
    for i in range(len(s1)):
        x = s1[i] ^ s2[i]
        cnt += bin(x).count("1")
            
    return cnt
