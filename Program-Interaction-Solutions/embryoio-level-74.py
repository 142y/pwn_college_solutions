#!/usr/bin/env python3
import glob
import os
from pwn import *

binary = glob.glob("/challenge/embryoio*")[0]
# 85 null values, 86th -> ckpujhcevf
p = process([binary, *([''] * 85), 'ckpujhcevf'])

p.interactive()