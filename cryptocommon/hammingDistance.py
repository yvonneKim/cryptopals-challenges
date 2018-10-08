# computes hamming distance of two byte strings
# strings must be equal length. Otherwise, returns -1

def hammingDistance(s1, s2):    

    if len(s1) != len(s2):
        raise ValueError("bytes not same length")

    if type(s1) == str:
        s1 = s1.encode('utf-8')
        
    if type(s2) == str:
        s2 = s2.encode('utf-8')

    cnt = 0
    for i in range(len(s1)):
        x = s1[i] ^ s2[i]
        cnt += bin(x).count("1")
            
    return cnt
