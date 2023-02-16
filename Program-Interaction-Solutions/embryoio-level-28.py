#!/usr/bin/env python3

from pwn import *

p = process(['/challenge/embryoio_level28'], env=dict())
p.interactive()