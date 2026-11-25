global print_cstr, print_u64, print_newline, print_bytes
extern str_len

section .bss
number_buffer: resb 32

section .text
; print_bytes(rdi=buffer, rsi=length)
print_bytes:
    mov rax, 1
    mov rdx, rsi
    mov rsi, rdi
    mov rdi, 1
    syscall
    ret

; print_cstr(rdi=string)
print_cstr:
    push rdi
    call str_len
    mov rsi, rax
    pop rdi
    jmp print_bytes

; print_newline()
print_newline:
    push rax
    push rdi
    push rsi
    push rdx
    mov rax, 1
    mov rdi, 1
    lea rsi, [rel newline]
    mov rdx, 1
    syscall
    pop rdx
    pop rsi
    pop rdi
    pop rax
    ret

; print_u64(rdi=unsigned integer)
print_u64:
    push rbx
    push r12
    sub rsp, 8                 ; alinhamento System V AMD64
    mov rax, rdi
    lea rbx, [rel number_buffer + 31]
    mov byte [rbx], 0
    mov r12, 10
    test rax, rax
    jnz .convert
    dec rbx
    mov byte [rbx], '0'
    jmp .output
.convert:
    xor rdx, rdx
    div r12
    add dl, '0'
    dec rbx
    mov [rbx], dl
    test rax, rax
    jnz .convert
.output:
    mov rdi, rbx
    call print_cstr
    add rsp, 8
    pop r12
    pop rbx
    ret

section .rodata
newline: db 10
