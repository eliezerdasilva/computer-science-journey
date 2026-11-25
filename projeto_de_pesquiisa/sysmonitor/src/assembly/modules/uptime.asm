extern sm_read_file, sm_parse_u64
global sm_read_uptime
section .rodata
path: db '/proc/uptime',0
section .bss
buf: resb 128
section .text
sm_read_uptime:
    push rbx
    mov rbx,rdi
    lea rdi,[rel path]
    lea rsi,[rel buf]
    mov edx,128
    call sm_read_file
    test rax,rax
    js .done
    lea rdi,[rel buf]
    call sm_parse_u64
    mov [rbx],rax
    xor eax,eax
.done: pop rbx
    ret
