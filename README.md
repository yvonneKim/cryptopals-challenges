# Cryptopals Challenges

## Installation
pip install and you should be fine

## Run
```python <file.py> [input-if-it-needs-one]```

## Testing
run ```pytest``` from root for all tests

to run individual tests, do:

```pytest test_setup.py tests/<path-to-test>```

To get a coverage report (from root):

```pytest --verbose --cov=<path-to-directory>```

## Files 
:ok_hand: - Tested

:heavy_check_mark: - Challenge Complete

### cryptocommon
- AES_CBC :ok_hand:
- AES_ECB :ok_hand:
- byteXor :ok_hand:
- hammingDistance :ok_hand:
- PKCS7

### Set 1
1. Convert hex to base64 :heavy_check_mark: :ok_hand:
2. Fixed XOR :heavy_check_mark: :ok_hand:
3. Single-byte XOR cipher :heavy_check_mark: :ok_hand:
4. Detect single-character XOR :heavy_check_mark: :ok_hand:
5. Implement repeating-key XOR :heavy_check_mark: :ok_hand:
6. Break repeating-key XOR :heavy_check_mark:
7. AES in ECB mode :heavy_check_mark:
8. Detect AES in ECB mode :heavy_check_mark:

### Set 2
1. Implement PKCS#7 padding :heavy_check_mark:
2. Implement CBC mode :heavy_check_mark:
3. An ECB/CBC detection oracle :heavy_check_mark:
4. Byte-at-a-time ECB decryption (Simple) :heavy_check_mark:
5. ECB cut-and-paste :heavy_check_mark:
6. Byte-at-a-time ECB decryption (Harder) :heavy_check_mark:
7. PKCS#7 padding validation :heavy_check_mark:
8. CBC bitflipping attacks :heavy_check_mark: