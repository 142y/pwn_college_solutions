#!/usr/bin/env python3
import glob
import os
from pwn import *

binary = glob.glob("/challenge/embryoio*")[0]
p = process([], executable=binary)

p.interactive()