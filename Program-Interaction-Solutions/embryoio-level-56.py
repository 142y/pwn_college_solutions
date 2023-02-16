#!/usr/bin/env python3
import glob
import os
from pwn import *

binary = glob.glob("/challenge/embryoio*")[0]

p1 = process(binary, stdin=PIPE)
p2 = process("cat", stdout=p1.stdin)

p1.interactive()