extern sm_read_file, sm_parse_u64, sm_copy_string
global sm_read_cpu
%define CPU_MODEL 0
%define CPU_LOGICAL 128
%define CPU_USAGE 136
%define CPU_CORE_COUNT 144
%define CPU_CORE_USAGE 152
section .rodata
p_cpuinfo: db '/proc/cpuinfo',0
p_stat: db '/proc/stat',0
section .bss
cpuinfo: resb 16384
statbuf: resb 8192
old_total: resq 1
old_idle: resq 1
has_old: resq 1
old_core_total: resq 64
old_core_idle: resq 64
old_core_valid: resb 64
section .text
sm_read_cpu:
    push rbx
    push r12
    push r13
    push r14
    push r15
    mov rbx,rdi

    ; Identifica o modelo e conta os processadores logicos em /proc/cpuinfo.
    lea rdi,[rel p_cpuinfo]
    lea rsi,[rel cpuinfo]
    mov edx,16384
    call sm_read_file
    test rax,rax
    js .error
    lea r12,[rel cpuinfo]
.find_model:
    cmp byte [r12],0
    je .count_logical
    cmp byte [r12],'m'
    jne .next_model
    cmp dword [r12+1],'odel'
    jne .next_model
    cmp byte [r12+5],' '
    jne .next_model
    cmp dword [r12+6],'name'
    jne .next_model
    lea rdi,[r12+11]
.find_colon:
    cmp byte [rdi],':'
    je .model_start
    cmp byte [rdi],10
    je .next_model
    inc rdi
    jmp .find_colon
.model_start:
    inc rdi
    cmp byte [rdi],' '
    jne .copy_model
    inc rdi
.copy_model:
    mov rsi,rbx
    mov edx,127
    call sm_copy_string
    jmp .count_logical
.next_model:
    inc r12
    jmp .find_model
.count_logical:
    xor r8d,r8d
    lea r12,[rel cpuinfo]
.count_loop:
    cmp byte [r12],0
    je .count_done
    cmp dword [r12],'proc'
    jne .count_next
    cmp dword [r12+4],'esso'
    jne .count_next
    cmp byte [r12+8],'r'
    jne .count_next
    inc r8
.count_next:
    inc r12
    jmp .count_loop
.count_done:
    mov [rbx+CPU_LOGICAL],r8

    ; Lê /proc/stat uma vez. A primeira linha fornece a CPU agregada.
    lea rdi,[rel p_stat]
    lea rsi,[rel statbuf]
    mov edx,8192
    call sm_read_file
    test rax,rax
    js .error
    lea r12,[rel statbuf+4]
    xor r9,r9                    ; total agregado atual
    xor r10,r10                  ; idle + iowait agregado atual
    xor r14d,r14d                ; indice de campo
.aggregate_fields:
    mov rdi,r12
    call sm_parse_u64
    cmp rdx,r12
    je .error
    mov r12,rdx
    add r9,rax
    cmp r14d,3
    je .aggregate_idle
    cmp r14d,4
    jne .aggregate_next
.aggregate_idle:
    add r10,rax
.aggregate_next:
    inc r14d
    cmp r14d,8
    jb .aggregate_fields

    mov qword [rbx+CPU_USAGE],0
    cmp qword [rel has_old],0
    je .save_aggregate
    mov rax,r9
    sub rax,[rel old_total]
    test rax,rax
    jz .save_aggregate
    mov rcx,rax
    mov rdx,r10
    sub rdx,[rel old_idle]
    sub rax,rdx
    imul rax,rax,100
    xor edx,edx
    div rcx
    mov [rbx+CPU_USAGE],rax
.save_aggregate:
    mov [rel old_total],r9
    mov [rel old_idle],r10
    mov qword [rel has_old],1

    ; Pula o restante da linha agregada e processa cpu0, cpu1, ... individualmente.
    mov r13,r12
.skip_aggregate_line:
    cmp byte [r13],10
    je .start_cores
    cmp byte [r13],0
    je .cores_done
    inc r13
    jmp .skip_aggregate_line
.start_cores:
    inc r13
    xor esi,esi                  ; quantidade de linhas cpuN processadas
.core_line:
    cmp byte [r13],'c'
    jne .cores_done
    cmp byte [r13+1],'p'
    jne .cores_done
    cmp byte [r13+2],'u'
    jne .cores_done
    movzx eax,byte [r13+3]
    cmp al,'0'
    jb .cores_done
    cmp al,'9'
    ja .cores_done
    lea rdi,[r13+3]
    call sm_parse_u64
    mov r15,rax                  ; indice do nucleo
    mov r12,rdx                  ; inicio dos contadores
    cmp r15,64
    jae .skip_core_line
    xor r8,r8                    ; total do nucleo
    xor r11,r11                  ; idle + iowait do nucleo
    xor r14d,r14d
.core_fields:
    mov rdi,r12
    call sm_parse_u64
    cmp rdx,r12
    je .skip_core_line
    mov r12,rdx
    add r8,rax
    cmp r14d,3
    je .core_idle
    cmp r14d,4
    jne .core_next
.core_idle:
    add r11,rax
.core_next:
    inc r14d
    cmp r14d,8
    jb .core_fields

    lea rdi,[rel old_core_total]
    lea rdx,[rdi+r15*8]
    lea rdi,[rel old_core_idle]
    lea rcx,[rdi+r15*8]
    lea rdi,[rel old_core_valid]
    cmp byte [rdi+r15],0
    je .first_core_sample
    mov rax,r8
    sub rax,[rdx]
    test rax,rax
    jz .zero_core_usage
    mov r10,rax
    mov rax,r11
    sub rax,[rcx]
    mov rdx,r10
    sub rdx,rax
    mov rax,rdx
    imul rax,rax,100
    xor edx,edx
    div r10
    jmp .store_core_usage
.first_core_sample:
.zero_core_usage:
    xor eax,eax
.store_core_usage:
    mov [rbx+CPU_CORE_USAGE+r15*8],rax
    lea rdi,[rel old_core_total]
    mov [rdi+r15*8],r8
    lea rdi,[rel old_core_idle]
    mov [rdi+r15*8],r11
    lea rdi,[rel old_core_valid]
    mov byte [rdi+r15],1
    inc esi
.skip_core_line:
    ; Avanca para a proxima linha cpuN.
    cmp byte [r12],10
    je .next_core_line
    cmp byte [r12],0
    je .cores_done
    inc r12
    jmp .skip_core_line
.next_core_line:
    inc r12
    mov r13,r12
    jmp .core_line
.cores_done:
    mov [rbx+CPU_CORE_COUNT],rsi
    xor eax,eax
    jmp .done
.error:
    mov rax,-1
.done:
    pop r15
    pop r14
    pop r13
    pop r12
    pop rbx
    ret
