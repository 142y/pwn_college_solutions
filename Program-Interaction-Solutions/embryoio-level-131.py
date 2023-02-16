import glob
import os
from pwn import *

binary = glob.glob("/challenge/embryoio*")[0]
p = process([binary])

time.sleep(1)

while line := p.readline():
    line = line.decode()
    print(line)
    
    chal = line.find('solution for: ')
    if chal > 0:
        p.sendline(str(eval(line[chal+4:].strip())).encode())
