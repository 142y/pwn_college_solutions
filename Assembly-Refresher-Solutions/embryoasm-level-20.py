import glob
from pwn import *

context.arch = "amd64"

binary = glob.glob("/challenge/embryo*")[0]
p = process([binary])

assembly = asm("""
xor rax, rax
xor rbx, rbx
loop:
    cmp rbx, rsi
    jge end
    add rax, [rdi + rbx * 8]
    add rbx, 1
    jmp loop
end:
    div rsi
""")

print(p.recvuntil(b'Please give me your assembly in bytes (up to 0x1000 bytes):').decode())
p.send(assembly)
print(p.clean().decode())
