import glob
import hashlib
from pwn import *
from base64 import b64decode, b64encode

binary = glob.glob("/challenge/run")[0]
p = process([binary])

def compute_proof_of_work(challenge_data):
    nonce = 0
    while True:
        response_data = str(nonce).encode()
        data = challenge_data + response_data
        hash_result = hashlib.sha256(data).digest()
        if hash_result[:2] == b'\x00\x00':
            return response_data
        nonce += 1

p.readuntil(b'challenge (b64): ')
challenge_b64 = p.readline().decode("utf-8")
challenge_data = base64.b64decode(challenge_b64)

response_data = compute_proof_of_work(challenge_data)
response_b64 = base64.b64encode(response_data).decode()
p.readuntil(b'response (b64): ')
p.sendline(str(response_b64).encode())

print(p.recvline().decode("utf-8"))