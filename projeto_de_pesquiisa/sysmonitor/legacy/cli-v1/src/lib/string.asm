global str_len, str_find, parse_u64

section .text
; str_len(rdi=string) -> rax=length
str_len:
    xor rax, rax
.loop:
    cmp byte [rdi + rax], 0
    je .end
    inc rax
    jmp .loop
.end:
    ret

; str_find(rdi=texto NUL-terminated, rsi=chave NUL-terminated) -> rax=ponteiro ou 0
str_find:
    push rbx
    push r12
    mov r12, rdi
.outer:
    cmp byte [r12], 0
    je .not_found
    mov rbx, rsi
    mov rdx, r12
.inner:
    mov al, [rbx]
    test al, al
    jz .found
    cmp al, [rdx]
    jne .next
    inc rbx
    inc rdx
    jmp .inner
.next:
    inc r12
    jmp .outer
.found:
    mov rax, r12
    jmp .exit
.not_found:
    xor rax, rax
.exit:
    pop r12
    pop rbx
    ret

; parse_u64(rdi=ponteiro para dígitos) -> rax=valor, rdx=ponteiro após dígitos
parse_u64:
    xor rax, rax
    mov rdx, rdi
.digits:
    movzx rcx, byte [rdx]
    cmp cl, '0'
    jb .end
    cmp cl, '9'
    ja .end
    imul rax, rax, 10
    sub rcx, '0'
    add rax, rcx
    inc rdx
    jmp .digits
.end:
    ret
