%include "constants.inc"
extern file_read, parse_u64, print_cstr, print_u64, print_newline

global uptime_show

section .rodata
uptime_path: db "/proc/uptime", 0
msg_title:   db 10, "=== TEMPO DE ATIVIDADE ===", 10, 0
msg_days:    db "Dias:    ", 0
msg_hours:   db "Horas:   ", 0
msg_minutes: db "Minutos: ", 0
msg_seconds: db "Segundos: ", 0
msg_error:   db "Erro: nao foi possivel ler /proc/uptime.", 10, 0

section .bss
uptime_buffer: resb 128
uptime_seconds: resq 1

section .text
uptime_show:
    push rbx
    push r12
    sub rsp, 8                 ; alinhamento System V AMD64
    lea rdi, [rel uptime_path]
    lea rsi, [rel uptime_buffer]
    mov rdx, 128
    call file_read
    test rax, rax
    js .error

    lea rdi, [rel uptime_buffer]
    call parse_u64
    mov [rel uptime_seconds], rax

    mov rax, [rel uptime_seconds]
    xor rdx, rdx
    mov rcx, 86400
    div rcx
    mov r12, rax
    mov rbx, rdx
    lea rdi, [rel msg_title]
    call print_cstr
    lea rdi, [rel msg_days]
    call print_cstr
    mov rdi, r12
    call print_u64
    call print_newline

    mov rax, rbx
    xor rdx, rdx
    mov rcx, 3600
    div rcx
    mov r12, rax
    mov rbx, rdx
    lea rdi, [rel msg_hours]
    call print_cstr
    mov rdi, r12
    call print_u64
    call print_newline

    mov rax, rbx
    xor rdx, rdx
    mov rcx, 60
    div rcx
    mov r12, rax
    mov rbx, rdx
    lea rdi, [rel msg_minutes]
    call print_cstr
    mov rdi, r12
    call print_u64
    call print_newline

    lea rdi, [rel msg_seconds]
    call print_cstr
    mov rdi, rbx
    call print_u64
    call print_newline
    jmp .done
.error:
    lea rdi, [rel msg_error]
    call print_cstr
.done:
    add rsp, 8
    pop r12
    pop rbx
    ret
