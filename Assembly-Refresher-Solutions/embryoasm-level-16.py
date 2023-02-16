import glob
from pwn import *

context.arch = "amd64"

binary = glob.glob("/challenge/embryo*")[0]
p = process([binary])

assembly = """
add rax, [rsp]
add rax, [rsp + 8]
add rax, [rsp + 16]
add rax, [rsp + 24]
mov rbx, 4
idiv rbx
push rax
"""

print(p.recvuntil(b'Please give me your assembly in bytes (up to 0x1000 bytes):').decode())
p.send(asm(assembly))
print(p.clean().decode())
