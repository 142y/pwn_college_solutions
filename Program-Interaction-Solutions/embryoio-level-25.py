#!/usr/bin/env python3

from pwn import *

p = process(['/challenge/embryoio_level25'], env={'kexugp': 'dyllawfhll'})
p.interactive()