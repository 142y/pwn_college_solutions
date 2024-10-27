import glob
from pwn import *
import json
from base64 import b64decode, b64encode
from Crypto.PublicKey import RSA
from Crypto.Hash.SHA256 import SHA256Hash

binary = glob.glob("/challenge/run")[0]
p = process([binary])

user_key = RSA.generate(1024)

lazy_cert = {
    "name": "lazy",
    "key": {
        "e": user_key.e,
        "n": user_key.n
    },
    "signer": "root"
}

p.readuntil(b'root key d: ')
d_hex = p.readline().decode()
root_d = int(d_hex.strip(), 16)

p.readuntil(b'root certificate (b64): ')
rootcert = b64decode(p.readline().decode())

root_n = json.loads(rootcert)['key']['n']

p.readuntil(b'root certificate signature (b64): ')
rootcert_sign = b64decode(p.readline().decode())

user_certificate_data = json.dumps(lazy_cert).encode()
user_certificate_hash = SHA256Hash(user_certificate_data).digest()

p.readuntil(b'user certificate (b64): ')
p.sendline(b64encode(user_certificate_data))

user_certificate_signature = pow(int.from_bytes(user_certificate_hash, "little"), root_d, root_n).to_bytes(256, "little")

p.readuntil(b'user certificate signature (b64): ')
p.sendline(b64encode(user_certificate_signature))

p.readuntil(b'secret ciphertext (b64): ')
secret = b64decode(p.readline().decode())

decrypted = pow(int.from_bytes(secret, "little"), user_key.d, user_key.n).to_bytes(57, "little")
plaintext = decrypted.decode("utf-8")
print("flag:", plaintext)