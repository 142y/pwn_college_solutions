import glob
from pwn import *

context.arch = "amd64"

binary = glob.glob("/challenge/embryo*")[0]
p = process([binary])

assembly = """
mov al, byte ptr [0x404000]
mov bx, word ptr [0x404000]
mov ecx, dword ptr [0x404000]
mov rdx, qword ptr [0x404000]
"""

print(p.recvuntil(b'Please give me your assembly in bytes (up to 0x1000 bytes):').decode())
p.send(asm(assembly))
print(p.clean().decode())
