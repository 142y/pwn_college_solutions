import glob
import json
from pwn import *
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Util.strxor import strxor
from Crypto.Hash.SHA256 import SHA256Hash
from Crypto.Util.Padding import pad, unpad
from Crypto.Random.random import getrandbits

binary = glob.glob("/challenge/run")[0]
p = process([binary])

# generate a key for the cert, this could be done before you use it
user_key = RSA.generate(1024)

# get the large prime
p.readuntil(b'p: ')
prime_hex = p.readline().decode()
prime = int(prime_hex.strip(), 16)

# get the primitive root modulo
p.readuntil(b'g: ')
g_hex = p.readline().decode()
g = int(g_hex.strip(), 16)

# get the root d, the private exponent
p.readuntil(b'root key d: ')
d_hex = p.readline().decode()
root_d = int(d_hex.strip(), 16)

# get the base64 encoded root certificate
p.readuntil(b'root certificate (b64): ')
rootcert = b64decode(p.readline().decode())

root_n = json.loads(rootcert)['key']['n']

# get teh base64 encoded root signature
p.readuntil(b'root certificate signature (b64): ')
rootcert_sign = b64decode(p.readline().decode())

# get the random name
p.readuntil(b'name: ')
uname = p.readline().decode().strip()

# create the user certificate with the random name
name_cert = {
    "name": str(uname),
    "key": {
        "e": user_key.e,
        "n": user_key.n
    },
    "signer": "root"
}

# get AS from Alice with Alices secret integer
p.readuntil(b'A: ')
A_hex = p.readline().decode()
A = int(A_hex.strip(), 16)

# create a secret integer b and send Alice B
# calculate B = g^b % p
b = getrandbits(1024)
B = pow(g, b, prime)
p.readuntil(b'B: ')
p.sendline(str(hex(B)).encode("utf-8"))


user_certificate_data = json.dumps(name_cert).encode()
user_certificate_hash = SHA256Hash(user_certificate_data).digest()

# calculate the shared secret
s = pow(A, b, prime)

# derive a AES-1289 key from the exchanged secret
mykey = SHA256Hash(s.to_bytes(256, "little")).digest()[:16]

# pad, encrypt and encode the user certificate before sending
#user_cert_cipher = AES.new(key=mykey, mode=AES.MODE_CBC, iv=b'\0' * 16)
cipher_encrypt = AES.new(key=mykey, mode=AES.MODE_CBC, iv=b'\0' * 16)
cipher_decrypt = AES.new(key=mykey, mode=AES.MODE_CBC, iv=b"\0" * 16)

user_cert_padded = pad(user_certificate_data, cipher_encrypt.block_size)
user_cert_encrypt = cipher_encrypt.encrypt(user_cert_padded)
user_cert_b64 = b64encode(user_cert_encrypt)

p.readuntil(b'user certificate (b64): ')
p.sendline(user_cert_b64)

# sign the user certificate with the roots private key
user_certificate_signature = pow(int.from_bytes(user_certificate_hash, "little"), 
				root_d, 
				root_n
			).to_bytes(256, "little")
			
#user_cert_sign_hash = SHA256Hash(user_certificate_signature).digest()

#user_cert_sign_cipher = AES.new(key=mykey, mode=AES.MODE_CBC, iv=b'\0' * 16)

# pad. encrpt and b64encode before sending
user_cert_sign_padded = pad(user_certificate_signature, cipher_encrypt.block_size)
user_cert_sign_encrypt = cipher_encrypt.encrypt(user_cert_sign_padded)
user_cert_sign_b64 = b64encode(user_cert_sign_encrypt)

p.readuntil(b'user certificate signature (b64): ')
p.sendline(user_cert_sign_b64)

#user_signature = pow(
#			int.from_bytes(user_cert_sign_hash, "little"), 
#			root_d, 
#			root_n
#		).to_bytes(256, "little")

# the server must sign the handshake to prove ownership of the private user key
# this is from the level14 code
handshake_data = (
        uname.encode().ljust(256, b"\0") +
        A.to_bytes(256, "little") +
        B.to_bytes(256, "little")
    )

#user_sign_key = SHA256Hash(user_signature).digest()
handshake_data_hash = SHA256Hash(handshake_data).digest()
handshake_data_signed = pow(int.from_bytes(handshake_data_hash, "little"), user_key.d, user_key.n).to_bytes(256, "little")

#user_sign_cipher = AES.new(key=mykey, mode=AES.MODE_CBC, iv=b'\0' * 16)
# pad, encrypt and b64 encode the handshake data to prove ownership of the private key
user_sign_padded = pad(handshake_data_signed, cipher_encrypt.block_size)
user_sign_encrypt = cipher_encrypt.encrypt(user_sign_padded)
user_sign_b64 = b64encode(user_sign_encrypt)

p.readuntil(b'user signature (b64): ')
p.sendline(user_sign_b64)

p.readuntil(b'secret ciphertext (b64): ')
secret = b64decode(p.readline())
secret = cipher_decrypt.decrypt(secret)
flag = unpad(secret, cipher_decrypt.block_size)
print("flag:", flag)