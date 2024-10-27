import glob
from pwn import *

binary = glob.glob("/challenge/run")[0]
p = process([binary])

p.readuntil(b'e: ')
e_hex = p.readline().decode()
e = int(e_hex.strip(), 16)

p.readuntil(b'd: ')
d_hex = p.readline().decode()
d = int(d_hex.strip(), 16)

p.readuntil(b'n: ')
n_hex = p.readline().decode()
n = int(n_hex.strip(), 16)

p.readuntil(b'challenge: ')
challenge_hex = p.readline().decode()
challenge_data = int(challenge_hex.strip(), 16)
# plaintext = ciphertext^d mod n
response_data = pow(challenge_data, d, n)

p.readuntil(b'response: ')
p.sendline(hex(response_data).encode())

print(p.recvline().decode("utf-8"))