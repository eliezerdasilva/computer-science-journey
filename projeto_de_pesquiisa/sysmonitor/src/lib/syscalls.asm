%include "constants.inc"

global sys_read, sys_write, sys_open, sys_close, sys_exit, file_read

section .text
; Wrappers simples: argumentos seguem System V AMD64 ABI.
sys_read:
    mov rax, SYS_READ
    syscall
    ret

sys_write:
    mov rax, SYS_WRITE
    syscall
    ret

sys_open:
    mov rax, SYS_OPEN
    syscall
    ret

sys_close:
    mov rax, SYS_CLOSE
    syscall
    ret

sys_exit:
    mov rax, SYS_EXIT
    syscall
    ud2

; file_read(path, buffer, capacity)
; Retorna quantidade de bytes em RAX ou erro negativo do kernel.
; Reserva um byte para o terminador NUL.
file_read:
    push rbx
    push r12
    push r13
    push r14
    sub rsp, 8                 ; alinhamento de pilha antes de CALL
    mov r12, rdi                ; caminho
    mov r13, rsi                ; buffer
    mov r14, rdx                ; capacidade

    mov rdi, r12
    mov rsi, O_RDONLY
    xor rdx, rdx
    call sys_open
    test rax, rax
    js .done
    mov rbx, rax                ; descritor

    mov rdi, rbx
    mov rsi, r13
    mov rdx, r14
    dec rdx                     ; espaço para NUL
    call sys_read
    mov r12, rax                ; resultado de read

    mov rdi, rbx
    call sys_close

    test r12, r12
    js .read_error
    mov byte [r13 + r12], 0
    mov rax, r12
    jmp .done
.read_error:
    mov rax, r12
.done:
    add rsp, 8
    pop r14
    pop r13
    pop r12
    pop rbx
    ret
