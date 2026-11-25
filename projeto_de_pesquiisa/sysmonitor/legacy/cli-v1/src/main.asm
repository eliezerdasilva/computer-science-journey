extern ui_run

global _start

section .text
_start:
    call ui_run
    mov rax, 60
    xor rdi, rdi
    syscall
