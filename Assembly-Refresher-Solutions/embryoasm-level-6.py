import glob
from pwn import *

context.arch = "amd64"

binary = glob.glob("/challenge/embryoasm*")[0]
p = process([binary])

assembly = """
mov al, dil
mov bx, si
"""

print(p.recvuntil(b'Please give me your assembly in bytes (up to 0x1000 bytes):').decode())
p.send(asm(assembly))
print(p.clean().decode())
