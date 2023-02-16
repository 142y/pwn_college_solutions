#!/usr/bin/env python3
import glob
import os
from pwn import *

binary = glob.glob("/challenge/embryoio*")[0]
p = process([binary], cwd="/tmp/elmbib") #For this to work, you have to create the tmp dir manually
# p = process(f'mkdir -p /tmp/elmbib; cd /tmp/elmbib; exec {binary}', shell=True)

p.interactive()