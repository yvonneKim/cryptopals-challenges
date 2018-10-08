# Cryptopals Challenges

## Installation
pip install and you should be fine

## Run
```python <file.py> [input-if-it-needs-one]```

## Testing
First, be in the test directory:

```cd tests/```

Then, run:

```pytest```

Or, with special coverage sauce:
```pytest --verbose --cov=<path-to-directory> .```

## Files 
:heavy_check_mark: - Tested
~~crossed out~~    - Done!

### cryptocommon
- AES_CBC :heavy_check_mark:
- AES_ECB :heavy_check_mark:
- byteXor :heavy_check_mark:
- hammingDistance :heavy_check_mark:
- PKCS7 :heavy_check_mark:

### Set 1
1. ~~Convert hex to base64~~ 
2. ~~Fixed XOR~~
3. ~~Single-byte XOR cipher~~
4. ~~Detect single-character XOR~~
5. ~~Implement repeating-key XOR~~
6. ~~Break repeating-key XOR~~
7. ~~AES in ECB mode~~
8. ~~Detect AES in ECB mode~~

### Set 2
1. ~~Implement PKCS#7 padding~~
2. ~~Implement CBC mode~~
3. ~~An ECB/CBC detection oracle~~
4. ~~Byte-at-a-time ECB decryption (Simple)~~
5. ~~ECB cut-and-paste~~
6. ~~Byte-at-a-time ECB decryption (Harder)~~
7. ~~PKCS#7 padding validation~~
8. ~~CBC bitflipping attacks~~