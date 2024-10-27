import glob
from pwn import *
from base64 import b64decode, b64encode
from Crypto.PublicKey import RSA

binary = glob.glob("/challenge/run")[0]
p = process([binary])

key = RSA.generate(1024)

p.readuntil(b'e: ')
p.sendline(hex(key.e).encode())

p.readuntil(b'n: ')
n_hex = p.sendline(hex(key.n).encode())

p.readuntil(b'challenge: ')
challenge_hex = p.readline().decode()
challenge_data = int(challenge_hex.strip(), 16)

# response = challenge^e mod n
response = pow(challenge_data, key.d, key.n)
p.readuntil(b'response: ')
p.sendline(hex(response).encode())

p.readuntil(b'secret ciphertext (b64): ')
ciphertext_b64 = p.readline().decode("utf-8")
ciphertext = b64decode(ciphertext_b64)

# Perform modular exponentiation
decrypted = pow(int.from_bytes(ciphertext, "little"), key.d, key.n).to_bytes(57, "little")

# Convert decrypted value from integer to bytes
plaintext = decrypted.decode("utf-8")

# Print the decrypted plaintext
print("flag:", plaintext)