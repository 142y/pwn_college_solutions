#!/usr/bin/env python3
import glob
import os
from pwn import *

binary = glob.glob("/challenge/embryoio*")[0]
p = process([binary, *([''] * 124), 'rjjzmzifto'], env={'277':'laygbjidfp'})

p.interactive()