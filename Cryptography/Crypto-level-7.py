import glob
from pwn import *
from base64 import b64decode, b64encode

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

p.readuntil(b'secret ciphertext (b64): ')
ciphertext_b64 = p.readline().decode("utf-8")

ciphertext = b64decode(ciphertext_b64)

# Perform modular exponentiation
decrypted = pow(int.from_bytes(ciphertext, "little"), d, n).to_bytes(64, "little")

# Convert decrypted value from integer to bytes
plaintext = decrypted.decode("utf-8")

# Print the decrypted plaintext
print("Decrypted Secret:", plaintext)