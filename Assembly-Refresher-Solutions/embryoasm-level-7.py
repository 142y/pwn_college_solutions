import glob
from pwn import *

context.arch = "amd64"

binary = glob.glob("/challenge/embryo*")[0]
p = process([binary])

assembly = """
mov rax, rdi
shl rax, 0x18
shr rax, 0x38
"""

print(p.recvuntil(b'Please give me your assembly in bytes (up to 0x1000 bytes):').decode())
p.send(asm(assembly))
print(p.clean().decode())
