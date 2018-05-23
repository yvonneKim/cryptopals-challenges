# computes hamming distance of two strings
# strings must be equal length. Otherwise, returns -1

def hammingDistance(s1, s2):
    if len(s1) != len(s2):
        print("STRINGS NOT SAME LENGTH. BYE.")
        return -1

    cnt = 0
    for i in range(len(s1)):
        x = ord(s1[i]) ^ ord(s2[i])
        cnt += bin(x).count("1")

    return cnt
