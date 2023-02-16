import glob
from pwn import *

context.arch = "amd64"

binary = glob.glob("/challenge/embryo*")[0]
p = process([binary])

# In main, it first saves the current value of the base pointer (rbp) onto the stack, and then sets rbp to the current stack pointer (rsp). 
# It then reserves 512 bytes on the stack (sub rsp, 0x200) and calls count_all followed by max. After these two functions return, 
# it restores the original value of rsp, and then restores the original value of rbp from the stack, and returns from the function using ret.

# count_all initializes the rax register to zero, and then enters a loop which compares rax to the value passed in the rsi register.
# If rax is greater than or equal to rsi, the loop ends and the function returns. Otherwise, it retrieves a byte from memory ([rdi + rax]) and stores it in bl. 
# It then computes a memory address as rcx - 2 * bl and increments the 16-bit value at that address by 1. Finally, it increments rax and jumps back to the beginning of the loop.

# max initializes the rax, rbx, and rcx registers to zero, and then enters a loop which compares rcx to 0xff. 
# If rcx is greater than 255, the loop ends and the function returns. Otherwise, it retrieves the memory address rdx - 2 * rcx, and compares the 16-bit value at
# that address to the value in bx. If the memory value is not greater than bx, it jumps to the next iteration of the loop. If it is greater, it updates rax with 
# the current value of rcx, updates bx with the memory value, and continues the loop. Finally, the function executes an interrupt (int3) before returning.

assembly = asm("""
main:
    push rbp
    mov rbp, rsp
    sub rsp, 0x200
    call count_all
    call max
    mov rsp, rbp
    pop rbp
    ret

count_all:
    xor rax, rax
    count_loop:  
        cmp rax, rsi 
        jge count_loop_end
        mov bl, byte ptr [rdi + rax]
        mov rcx, rbp  
        sub rcx, rbx
        sub rcx, rbx
        add word ptr [rcx], 1
        add rax, 1
        jmp count_loop
    count_loop_end:
        ret
max:
    xor rax, rax
    xor rbx, rbx
    xor rcx, rcx
    max_loop:
        cmp rcx, 0xff  
        jg max_loop_end
        mov rdx, rbp
        sub rdx, rcx
        sub rdx, rcx
        cmp word ptr [rdx], bx
        jle not_larger
        mov rax, rcx
        mov bx, [rdx]
        not_larger:
            add rcx, 1
            jmp max_loop
        max_loop_end:
        int3
        ret
""")

print(p.recvuntil(b'Please give me your assembly in bytes (up to 0x1000 bytes):').decode())
p.send(assembly)
print(p.clean().decode())
