import glob
from pwn import *

binary = glob.glob("/challenge/embryoio*")[0]
p = process([binary])

for i in range(5):
    p.readuntil(b'solution for: ')
    q = p.readline()
    result = str(eval(q.decode().strip()))
    print(result)
    p.sendline(result.encode())

p.readuntil('Here is your flag:\n')
print(p.read())