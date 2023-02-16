import glob
from pwn import *

context.arch = "amd64"

binary = glob.glob("/challenge/embryo*")[0]
p = process([binary])

assembly = """
mov rax, [0x404000]
mov rbx, rax
add rbx, 0x1337
mov [0x404000], rbx
"""

# assembly = """
# mov rax, [0x404000]
# add qword ptr [0x404000], 0x1337
# must specify 'qword ptr' else the assembler goes haywire
# """

print(p.recvuntil(b'Please give me your assembly in bytes (up to 0x1000 bytes):').decode())
p.send(asm(assembly))
print(p.clean().decode())
