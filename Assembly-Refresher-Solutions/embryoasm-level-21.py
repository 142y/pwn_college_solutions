import glob
from pwn import *

context.arch = "amd64"

binary = glob.glob("/challenge/embryo*")[0]
p = process([binary])

assembly = asm("""
mov rax, 0
cmp rdi, 0
je done

loop:
mov rbx, 0
mov bl, [rdi]
cmp bl, 0
je done
add rax, 1
add rdi, 1
jmp loop

done:
nop
int3
""")

print(p.recvuntil(b'Please give me your assembly in bytes (up to 0x1000 bytes):').decode())
p.send(assembly)
print(p.clean().decode())
