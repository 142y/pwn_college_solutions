import glob
from pwn import *

context.arch = "amd64"

binary = glob.glob("/challenge/embryo*")[0]
p = process([binary])

assembly = asm("""
cmp rdi, 3
jbe here
mov rdi, 4

here:
lea rax, [rsi + rdi * 8]
mov rax, [rax]
int3
jmp rax
""")

print(p.recvuntil(b'Please give me your assembly in bytes (up to 0x1000 bytes):').decode())
p.send(assembly)
print(p.clean().decode())
