import glob
from pwn import *

context.arch = "amd64"

binary = glob.glob("/challenge/embryo*")[0]
p = process([binary])

assembly = asm("""
jmp here
.rept 0x51
nop
.endr
here:
pop rdi
mov rax, 0x403000
jmp rax
""")

print(p.recvuntil(b'Please give me your assembly in bytes (up to 0x1000 bytes):').decode())
p.send(assembly)
print(p.clean().decode())
