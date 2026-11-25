%include "constants.inc"
extern file_read, str_find, parse_u64, print_cstr, print_u64, print_newline

global memory_show

section .rodata
meminfo_path: db "/proc/meminfo", 0
key_total:    db "MemTotal:", 0
key_avail:    db "MemAvailable:", 0
msg_title:    db 10, "=== MEMORIA RAM ===", 10, 0
msg_total:    db "Memoria total:      ", 0
msg_avail:    db "Memoria disponivel: ", 0
msg_used:     db "Memoria utilizada:  ", 0
msg_percent:  db "Uso percentual:     ", 0
msg_kb:       db " kB", 10, 0
msg_pct:      db "%", 10, 0
msg_error:    db "Erro: nao foi possivel ler /proc/meminfo.", 10, 0

section .bss
mem_buffer: resb BUFFER_SIZE
mem_total:  resq 1
mem_avail:  resq 1
mem_used:   resq 1
mem_pct:    resq 1

section .text
memory_show:
    push rbx
    lea rdi, [rel meminfo_path]
    lea rsi, [rel mem_buffer]
    mov rdx, BUFFER_SIZE
    call file_read
    test rax, rax
    js .error

    lea rdi, [rel mem_buffer]
    lea rsi, [rel key_total]
    call str_find
    test rax, rax
    jz .error
    add rax, 9
    mov rdi, rax
    call parse_u64
    mov [rel mem_total], rax

    lea rdi, [rel mem_buffer]
    lea rsi, [rel key_avail]
    call str_find
    test rax, rax
    jz .error
    add rax, 13
    mov rdi, rax
    call parse_u64
    mov [rel mem_avail], rax

    mov rax, [rel mem_total]
    sub rax, [rel mem_avail]
    mov [rel mem_used], rax
    xor rdx, rdx
    mov rcx, 100
    mul rcx
    mov rcx, [rel mem_total]
    test rcx, rcx
    jz .error
    div rcx
    mov [rel mem_pct], rax

    lea rdi, [rel msg_title]
    call print_cstr
    lea rdi, [rel msg_total]
    call print_cstr
    mov rdi, [rel mem_total]
    call print_u64
    lea rdi, [rel msg_kb]
    call print_cstr

    lea rdi, [rel msg_avail]
    call print_cstr
    mov rdi, [rel mem_avail]
    call print_u64
    lea rdi, [rel msg_kb]
    call print_cstr

    lea rdi, [rel msg_used]
    call print_cstr
    mov rdi, [rel mem_used]
    call print_u64
    lea rdi, [rel msg_kb]
    call print_cstr

    lea rdi, [rel msg_percent]
    call print_cstr
    mov rdi, [rel mem_pct]
    call print_u64
    lea rdi, [rel msg_pct]
    call print_cstr
    jmp .done
.error:
    lea rdi, [rel msg_error]
    call print_cstr
.done:
    pop rbx
    ret
