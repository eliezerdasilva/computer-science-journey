%include "constants.inc"
extern file_read, str_find, parse_u64, print_cstr, print_bytes, print_u64, print_newline

global cpu_show, cpu_usage_show

section .rodata
cpuinfo_path: db "/proc/cpuinfo", 0
stat_path:    db "/proc/stat", 0
key_model:    db "model name", 0
msg_title:    db 10, "=== PROCESSADOR ===", 10, 0
msg_model:    db "Modelo: ", 0
msg_logical:  db "Processadores logicos identificados: ", 0
msg_error:    db "Erro: nao foi possivel ler /proc/cpuinfo.", 10, 0
msg_usage:    db "Utilizacao aproximada da CPU: ", 0
msg_percent:  db "% (amostra de 1 segundo)", 10, 0
msg_stat_error: db "Nao foi possivel calcular a utilizacao da CPU.", 10, 0
timespec:      dq 1, 0

section .bss
cpu_buffer: resb BUFFER_SIZE
stat_buffer: resb 512
current_total: resq 1
current_idle:  resq 1
previous_total: resq 1
previous_idle:  resq 1

section .text
cpu_show:
    push rbx
    lea rdi, [rel cpuinfo_path]
    lea rsi, [rel cpu_buffer]
    mov rdx, BUFFER_SIZE
    call file_read
    test rax, rax
    js .error

    lea rdi, [rel msg_title]
    call print_cstr
    lea rdi, [rel cpu_buffer]
    lea rsi, [rel key_model]
    call str_find
    test rax, rax
    jz .count_only
    ; Avanca ate o ':' e depois ignora espacos.
.find_colon:
    cmp byte [rax], ':'
    je .after_colon
    cmp byte [rax], 0
    je .count_only
    inc rax
    jmp .find_colon
.after_colon:
    inc rax
.skip_spaces:
    cmp byte [rax], ' '
    jne .print_model
    inc rax
    jmp .skip_spaces
.print_model:
    mov rbx, rax
.model_end:
    cmp byte [rax], 10
    je .model_print
    cmp byte [rax], 0
    je .model_print
    inc rax
    jmp .model_end
.model_print:
    sub rax, rbx
    mov rsi, rax
    mov rdi, rbx
    push rsi
    push rdi
    lea rdi, [rel msg_model]
    call print_cstr
    pop rdi
    pop rsi
    call print_bytes
    call print_newline
.count_only:
.show_count:
    lea rdi, [rel msg_logical]
    call print_cstr
    ; Conta as linhas que comecam com "processor".
    lea rdi, [rel cpu_buffer]
    call count_processor_lines
    mov rdi, rax
    call print_u64
    call print_newline
    call cpu_usage_show
    jmp .done
.error:
    lea rdi, [rel msg_error]
    call print_cstr
.done:
    pop rbx
    ret

; count_processor_lines(rdi=texto) -> rax=quantidade de linhas "processor"
count_processor_lines:
    push rbx
    push r12
    mov rbx, rdi
    xor r12, r12
.scan:
    cmp byte [rbx], 0
    je .finish
    ; Detecta a palavra "processor" no início de uma linha.
    cmp rbx, rdi
    je .check
    cmp byte [rbx-1], 10
    jne .advance
.check:
    cmp byte [rbx], 'p'
    jne .advance
    cmp byte [rbx+1], 'r'
    jne .advance
    cmp byte [rbx+2], 'o'
    jne .advance
    cmp byte [rbx+3], 'c'
    jne .advance
    cmp byte [rbx+4], 'e'
    jne .advance
    cmp byte [rbx+5], 's'
    jne .advance
    cmp byte [rbx+6], 's'
    jne .advance
    cmp byte [rbx+7], 'o'
    jne .advance
    cmp byte [rbx+8], 'r'
    jne .advance
    inc r12
.advance:
    inc rbx
    jmp .scan
.finish:
    mov rax, r12
    pop r12
    pop rbx
    ret


; cpu_usage_show: calcula uso aproximado comparando duas amostras de /proc/stat.
; A primeira amostra e a segunda sao separadas por nanosleep de 1 segundo.
cpu_usage_show:
    push r12
    call read_cpu_counters
    test rax, rax
    js .usage_error
    mov rax, [rel current_total]
    mov [rel previous_total], rax
    mov rax, [rel current_idle]
    mov [rel previous_idle], rax

    mov rax, SYS_NANOSLEEP
    lea rdi, [rel timespec]
    xor rsi, rsi
    syscall

    call read_cpu_counters
    test rax, rax
    js .usage_error

    mov rax, [rel current_total]
    sub rax, [rel previous_total]
    test rax, rax
    jz .usage_error
    mov r12, rax                 ; delta total
    mov rdx, [rel current_idle]
    sub rdx, [rel previous_idle]
    mov rax, r12
    sub rax, rdx                 ; delta non-idle
    imul rax, rax, 100
    xor rdx, rdx
    div r12

    mov r12, rax
    lea rdi, [rel msg_usage]
    call print_cstr
    mov rdi, r12
    call print_u64
    lea rdi, [rel msg_percent]
    call print_cstr
    jmp .usage_done
.usage_error:
    lea rdi, [rel msg_stat_error]
    call print_cstr
.usage_done:
    pop r12
    ret

; read_cpu_counters: le primeira linha de /proc/stat e calcula total e idle.
; Retorna zero em RAX ou codigo negativo de erro.
read_cpu_counters:
    push r12
    push r13
    push r14
    push r15
    sub rsp, 8
    lea rdi, [rel stat_path]
    lea rsi, [rel stat_buffer]
    mov rdx, 512
    call file_read
    test rax, rax
    js .counter_done

    lea r12, [rel stat_buffer]
    add r12, 4                 ; pula "cpu "
    xor r13, r13               ; indice do campo
    xor r14, r14               ; soma total
    xor r15, r15               ; soma idle + iowait
.counter_loop:
.skip_spaces:
    cmp byte [r12], ' '
    jne .parse_field
    inc r12
    jmp .skip_spaces
.parse_field:
    mov rdi, r12
    call parse_u64
    cmp rdx, r12
    je .invalid_stat
    mov r12, rdx
    add r14, rax
    cmp r13, 3
    je .add_idle
    cmp r13, 4
    jne .next_field
.add_idle:
    add r15, rax
.next_field:
    inc r13
    cmp r13, 8
    jb .counter_loop

    mov [rel current_total], r14
    mov [rel current_idle], r15
    xor rax, rax
    jmp .counter_done
.invalid_stat:
    mov rax, -22
.counter_done:
    add rsp, 8
    pop r15
    pop r14
    pop r13
    pop r12
    ret
