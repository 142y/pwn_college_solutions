import time
import glob

from pwn import *

binary = glob.glob("/challenge/embryoio*")[0]
process([binary])

time.sleep(1)

p = remote('127.0.0.1', 1273)

while line := p.readline():
    line = line.decode()
    print(line)

    chal = line.find('for: ')
    if chal > 0:
        p.sendline(str(eval(line[chal+4:].strip())).encode())