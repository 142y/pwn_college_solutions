import glob
from pwn import *
from base64 import b64decode, b64encode
from Crypto.Util.strxor import strxor
from Crypto.Random.random import getrandbits

context.arch = 'amd64' 
context.log_level = 'info'

binary = glob.glob("/challenge/run")[0]
p = process([binary])

p.readuntil(b'p: ')
prime = p.readline().decode()
prime_int = int(prime.strip(), 16)

p.readuntil(b'g: ')
rootmod = p.readline().decode()
rootmod_int = int(rootmod.strip(), 16)

p.readuntil(b'A: ')
A = p.readline().decode()
A_int = int(A.strip(), 16)

# calculate B = g^b % p
b = getrandbits(2048)
B = hex(pow(rootmod_int, b, prime_int))
p.readuntil(b'B: ')
p.sendline(str(B).encode("utf-8"))

p.readuntil(b'secret ciphertext (b64): ')
secret = p.readline().decode()
secret_ct = b64decode(secret)

s = pow(A_int, b, prime_int)
key = s.to_bytes(1024, "little")

print(strxor(secret_ct, key[:len(secret_ct)]).decode("utf-8"))
