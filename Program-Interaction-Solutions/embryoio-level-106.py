import glob
import os

from pwn import *

binary = glob.glob("/challenge/embryoio*")[0]

pipein_read = os.open("in", os.O_RDWR)
pipein_write = os.open("in", os.O_WRONLY)
pipeout_read = os.open("out", os.O_RDWR)
pipeout_write = os.open("out", os.O_WRONLY)

p_in = process(["cat", "-"], stdout=pipein_write)
p = process([binary], stdin=pipein_read, stdout=pipeout_write)
p_out = process(["cat", "-"], stdin=pipeout_read)

print(p_out.readuntil(b'solution for: ').decode("utf-8"))
q = p_out.readline()
result = str(eval(q.decode().strip()))
print(result)
p_in.sendline(result.encode())
print(p_out.recv().decode("utf-8"))

p.wait()

os.close(pipeout_write)
os.close(pipeout_read)
os.close(pipein_write)
os.close(pipein_read)