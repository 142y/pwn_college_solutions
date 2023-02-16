import glob
from pwn import *

context.arch = "amd64"

binary = glob.glob("/challenge/embryo*")[0]
p = process([binary])

assembly = asm("""
xor rax, rax
cmp rdi, 0
je done

loop:
mov rbx, 0
mov bl, [rdi]
cmp bl, 0
je done

cmp bl, 90
jg ninety

push rdi
push rax
mov rdi, 0
mov dil, bl
mov r10, 0x403000
call r10
mov bl, al
pop rax
pop rdi
mov [rdi], bl
add rax, 1

ninety:
    add rdi, 1
    jmp loop

done:
    nop
    ret
""")

print(p.recvuntil(b'Please give me your assembly in bytes (up to 0x1000 bytes):').decode())
p.send(assembly)
print(p.clean().decode())
