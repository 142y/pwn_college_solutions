#!/usr/bin/env python3

import os
from pwn import *

p1 = process("cat")
p2 = process("/challenge/embryoio_level54", stdout=p1.stdin)

p1.interactive()