import glob
from pwn import *
from base64 import b64encode,b64decode

context.arch = 'amd64'
context.log_level = 'info'

binary = glob.glob("/challenge/run")[0]

with process([binary]) as p:
    # read the secret
    p.readuntil(b'secret ciphertext (b64): ')
    ct_first = b64decode(p.readline())
    print("secret", ct_first)

    secret = b""
    prefix_length = 63

    for i in range(64): 
        # send base64 encoded flag to plaintext (b64)
        p.readuntil(b'plaintext prefix (b64): ')
        myflag = b'a'*prefix_length
        p.writeline(b64encode(myflag))

        p.readuntil(b'ciphertext (b64): ')
        ciphertext_with_secret = b64decode(p.readline())[:64]
        # print("ciphertext", ciphertext_with_secret)

        results = {}
        for i in range(256):
            p.readuntil(b'plaintext prefix (b64): ')
            myflag = b'a'*prefix_length + secret + bytes([i]) 
            p.writeline(b64encode(myflag))

            p.readuntil(b'ciphertext (b64): ')
            ct = b64decode(p.readline())[:64]
            results[ct] = bytes([i])

        secret += results[ciphertext_with_secret][:64]
        prefix_length -= 1
        
        print(secret)