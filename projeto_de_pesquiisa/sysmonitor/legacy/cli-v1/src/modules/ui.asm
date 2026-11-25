%include "constants.inc"
extern sys_read, print_cstr, print_newline
extern memory_show, uptime_show, cpu_show

global ui_run

section .rodata
banner: db 10, "========================================", 10
        db "             SYSMONITOR                 ", 10
        db "      Linux System Resource Monitor     ", 10
        db "========================================", 10, 0
menu:   db 10, "[1] Monitorar memoria RAM", 10
        db "[2] Informacoes do processador", 10
        db "[3] Tempo de atividade do sistema", 10
        db "[4] Atualizar / voltar ao menu", 10
        db "[0] Sair", 10
        db "Opcao: ", 0
invalid: db "Opcao invalida. Tente novamente.", 10, 0
bye:     db 10, "Encerrando SysMonitor. Ate mais!", 10, 0

section .bss
input_buffer: resb INPUT_SIZE

section .text
ui_run:
    push rbx
    lea rdi, [rel banner]
    call print_cstr
.loop:
    lea rdi, [rel menu]
    call print_cstr
    mov rax, SYS_READ
    mov rdi, STDIN
    lea rsi, [rel input_buffer]
    mov rdx, INPUT_SIZE
    syscall
    test rax, rax
    jle .exit

    mov al, [rel input_buffer]
    cmp al, '0'
    je .exit
    cmp al, '1'
    je .memory
    cmp al, '2'
    je .cpu
    cmp al, '3'
    je .uptime
    cmp al, '4'
    je .loop

    lea rdi, [rel invalid]
    call print_cstr
    jmp .loop
.memory:
    call memory_show
    jmp .loop
.cpu:
    call cpu_show
    jmp .loop
.uptime:
    call uptime_show
    jmp .loop
.exit:
    lea rdi, [rel bye]
    call print_cstr
    pop rbx
    ret
