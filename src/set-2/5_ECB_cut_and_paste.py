# k=v parser
import sys, os
sys.path.append(os.path.abspath('..'))
from cryptocommon import AES_ECB as ECB

def main():
    key = os.urandom(16)
    test_profile = {
        'email': 'foobar@gmail.com',
        'uid': 10,
        'role': 'user'
        }

    # the attack input is a large string made of 16-char blocks
    b1 = '          '        # -> "email=          "
    b2 = 'yvonne@gmail.com'  # -> "yvonne@gmail.com"
    b3 = 'admin           '  # -> "admin           "
    b4 = '   '               # -> "   &uid=10&role="
                             # -> "user" (leftover block)

    attack_string = ''.join((b1, b2, b3, b4))
    test_profile_string = profileFor(attack_string)
    print("ATTACK STRING : "+test_profile_string)
    encrypted_string = ECB.encryptor(test_profile_string.encode('utf-8'), key=key, bsize=16)
    print("CIPHERTEXT : ")
    print(encrypted_string)

    # how to get ciphertext that decrypts to "email=yvonne@gmail.com&uid=10&role=admin"?
    b1_enc = encrypted_string[0:16]
    b2_enc = encrypted_string[16:32]
    b4_enc = encrypted_string[48:64]
    b3_enc = encrypted_string[32:48]

    # composite ciphertext is valid but has lots of empty spaces. Will only work if the decoder
    # removes those as delimiters...
    attack_cipher = b''.join((b1_enc, b2_enc, b4_enc, b3_enc))
    attack_ptext = ECB.decryptor(attack_cipher, key=key, bsize=16).decode('utf-8')
    print("DECRYPTED : "+attack_ptext)
    parseKVString(attack_ptext)
    print("AS PROFILE : ")
    print(parseKVString(attack_ptext))
    

def parseKVString(data):
    # remove whitespace
    data = ''.join(data.split())
    result = {pair[0]: pair[1] for pair in (pair_str.split('=') for pair_str in data.split('&'))}
    return result

def KVStringify(object):
    return '&'.join(pair_str for pair_str in (str(pair[0])+'='+str(pair[1]) for pair in object.items()))

def profileFor(email):
    email = email.replace('&', '').replace('=', '') # replace w something better later?
    profile = {'email': email, 'uid': 10, 'role': 'user'}
    return KVStringify(profile)

if __name__=='__main__':
    main()
