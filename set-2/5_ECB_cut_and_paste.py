# k=v parser

def main():
    print(parseKVString('foo=bar&baz=qux&zap=zazzle'))
    print(profileFor('poop@poop.com&&&&&====='))

def parseKVString(data):
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