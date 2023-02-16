import glob
from pwn import *

context.arch = "amd64"

binary = glob.glob("/challenge/embryo*")[0]
p = process([binary])

assembly = asm("""
mov eax, [rdi+4]
mov ebx, [rdi+8]
mov ecx, [rdi+12]
mov edx, [rdi]

cmp edx, 0x7f454c46
je add

cmp edx, 0x00005A4D
je sub

mul:
    imul ebx
    imul ecx
    jmp done

add:
    add eax, ebx
    add eax, ecx
    jmp done

sub:
    sub eax, ebx
    sub eax, ecx
    jmp done

done:
    int3
""")

print(p.recvuntil(b'Please give me your assembly in bytes (up to 0x1000 bytes):').decode())
p.send(assembly)
print(p.clean().decode())
