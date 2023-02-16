import glob
from pwn import *

context.arch = "amd64"

binary = glob.glob("/challenge/embryo*")[0]
p = process([binary])

assembly = """
mov rax, 0xdeadbeef00001337
mov [rdi], rax
mov rbx, 0xc0ffee0000
mov [rsi], rbx
"""

print(p.recvuntil(b'Please give me your assembly in bytes (up to 0x1000 bytes):').decode())
p.send(asm(assembly))
print(p.clean().decode())
