#!/usr/bin/env python3

from pwn import *

p = process(['/challenge/embryoio_level22'], env={})
p.interactive()