#!/usr/bin/env python3

from pwn import *

p = process(['/challenge/embryoio_level24', 'hucnsksnpi'], env={})
p.interactive()