import glob
import re
import signal
import time

from pwn import *

binary = glob.glob("/challenge/embryoio*")[0]
p = process([binary])

time.sleep(1)

p.readuntil(b'[TEST] You must send me')

output = p.readline().decode()
print(output)
pidnum = re.search(r'\(PID (\d+)\)', output).group(1)
sigs = re.search(r"in exactly this order: \[(.*)]", output).group(1).replace("'", '').split(', ')

print(pidnum, sigs)

for sig in sigs:
    sig = getattr(signal, sig)
    os.kill(int(pidnum), int(sig))
    print(p.read().decode())

p.wait()
print(p.read().decode())