extern sm_read_file, sm_parse_u64
global sm_read_network
section .rodata
path: db '/proc/net/dev',0
section .bss
buf: resb 8192
prev_rx: resq 1
prev_tx: resq 1
prev_valid: resq 1
section .text
; Aggregates RX/TX counters for all interfaces, skipping loopback.
sm_read_network:
    push rbx
    push r12
    push r13
    mov rbx,rdi
    lea rdi,[rel path]
    lea rsi,[rel buf]
    mov edx,8192
    call sm_read_file
    test rax,rax
    js .done
    lea r12,[rel buf]
    xor r13d,r13d
    xor r8d,r8d
    xor r9d,r9d
.line: cmp byte [r12],0
    je .finish
    ; find colon, reject lo interface
    mov r10,r12
.colon: cmp byte [r10],':'
    je .gotcolon
    cmp byte [r10],10
    je .nextline
    cmp byte [r10],0
    je .finish
    inc r10
    jmp .colon
.gotcolon:
    cmp byte [r12],' '
    jne .parse
    ; interface name can have leading spaces; detect 'lo:' by checking preceding chars
    cmp byte [r10-2],'l'
    jne .parse
    cmp byte [r10-1],'o'
    je .nextline
.parse: lea rdi,[r10+1]
    call sm_parse_u64
    add r8,rax
    ; RX fields after bytes: packets, errs, drop, fifo, frame, compressed, multicast.
    mov rdi,rdx
    mov r11d,7
.skip: call sm_parse_u64
    mov rdi,rdx
    dec r11d
    jnz .skip
    call sm_parse_u64
    add r9,rax
.nextline: mov r12,r10
.scanend: cmp byte [r12],10
    je .afterline
    cmp byte [r12],0
    je .finish
    inc r12
    jmp .scanend
.afterline: inc r12
    jmp .line
.finish:
    mov [rbx],r8
    mov [rbx+8],r9
    cmp qword [rel prev_valid],0
    je .first
    mov rax,r8
    sub rax,[rel prev_rx]
    mov [rbx+16],rax
    mov rax,r9
    sub rax,[rel prev_tx]
    mov [rbx+24],rax
    jmp .save
.first: mov qword [rbx+16],0
    mov qword [rbx+24],0
.save: mov [rel prev_rx],r8
    mov [rel prev_tx],r9
    mov qword [rel prev_valid],1
    xor eax,eax
.done: pop r13
    pop r12
    pop rbx
    ret
