import re
import glob
import signal
from pwn import *

binary = glob.glob('/challenge/em*')[0]

p = process([binary])

time.sleep(1)

output = p.read().decode('utf-8')
print(output)
# b"8867) the following signals, in exactly this order: ['SIGHUP']\n"
pidnum = re.search(r'\(PID (\d+)\)', output).group(1)
sigs = re.search(r"exactly this order: \[(.*)]", output).group(1).replace("'", "").split(', ')

for sig in sigs:
    sig = getattr(signal, sig)
    os.kill(int(pidnum), int(sig))

p.wait()
print(p.read().decode())