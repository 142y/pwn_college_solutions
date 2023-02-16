import os
import glob
from pwn import *

bin_path = glob.glob('/challenge/em*')[0]

myfifo = 'fifofile'
if os.path.exists(myfifo):
    os.remove(myfifo)

os.mkfifo(myfifo, 0o666)

pipe_read = os.open("fifofile", os.O_RDWR)
pipe_write = os.open("fifofile", os.O_WRONLY)

p1 = process([bin_path], stdout=pipe_write)
p2 = process(["cat", "-"], stdin=pipe_read)
time.sleep(1)

print(p2.read(4096).decode())

os.close(pipe_write)
os.close(pipe_read)
