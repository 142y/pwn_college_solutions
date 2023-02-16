import glob

from pwn import *

p = process(["bash", "pp.sh"])

for i in range(5):
    p.readuntil(b'solution for: ')
    q = p.readline()
    result = str(eval(q.decode().strip()))
    print(result)
    p.sendline(result.encode())

p.readuntil('Here is your flag:\n')
print(p.read())