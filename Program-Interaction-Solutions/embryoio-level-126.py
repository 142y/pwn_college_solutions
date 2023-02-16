import glob

from pwn import *

p = process(["bash", "pp.sh"])

for i in range(500):
    p.readuntil(b'solution for: ')
    q = p.readline()
    # print(q.decode("utf-8"))
    result = str(eval(q.decode().strip()))
    # print(result)
    p.sendline(result.encode())

p.readuntil('Here is your flag:\n')
print(p.read().decode("utf-8"))