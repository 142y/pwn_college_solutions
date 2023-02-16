#!/usr/bin/env python3

from pwn import *

p = process(['/challenge/embryoio_level23'], env={})
p.interactive()

# On prompt - input `lbjyugcl`