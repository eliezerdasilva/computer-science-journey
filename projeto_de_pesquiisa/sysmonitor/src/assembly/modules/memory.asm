%define MEM_TOTAL 0
%define MEM_AVAILABLE 8
%define MEM_USED 16
%define SWAP_TOTAL 24
%define SWAP_FREE 32
extern sm_read_file, sm_parse_u64
global sm_read_memory
section .rodata
p_mem: db '/proc/meminfo',0
k_total: db 'MemTotal:',0
k_avail: db 'MemAvailable:',0
k_swap: db 'SwapTotal:',0
k_swapfree: db 'SwapFree:',0
section .bss
mem_buf: resb 8192
section .text
; Parse a key in mem_buf. rdi=key, rsi=keylen -> rax=value or 0
get_value:
    push r11                    ; mantém alinhamento de pilha antes de chamar parser
    mov r11,rdi                 ; chave
    mov r10,rsi                 ; comprimento da chave
    lea r8,[rel mem_buf]
.scan:
    cmp byte [r8],0
    je .missing
    mov r9,r8                   ; início da linha/candidato
    xor ecx,ecx
.match:
    cmp rcx,r10
    je .found
    mov al,[r9+rcx]
    cmp al,[r11+rcx]
    jne .next
    inc rcx
    jmp .match
.next:
    cmp byte [r8],10
    je .newline
    cmp byte [r8],0
    je .missing
    inc r8
    jmp .next
.newline:
    inc r8
    jmp .scan
.found:
    lea rdi,[r9+r10]
    call sm_parse_u64
    pop r11
    ret
.missing:
    xor eax,eax
    pop r11
    ret

sm_read_memory:
    push rbx
    mov rbx,rdi
    lea rdi,[rel p_mem]
    lea rsi,[rel mem_buf]
    mov edx,8192
    call sm_read_file
    test rax,rax
    js .err
    lea rdi,[rel k_total]
    mov esi,9
    call get_value
    mov [rbx+MEM_TOTAL],rax
    lea rdi,[rel k_avail]
    mov esi,13
    call get_value
    mov [rbx+MEM_AVAILABLE],rax
    mov rdx,[rbx+MEM_TOTAL]
    sub rdx,rax
    mov [rbx+MEM_USED],rdx
    lea rdi,[rel k_swap]
    mov esi,10
    call get_value
    mov [rbx+SWAP_TOTAL],rax
    lea rdi,[rel k_swapfree]
    mov esi,9
    call get_value
    mov [rbx+SWAP_FREE],rax
    xor eax,eax
    jmp .done
.err: ; preserve negative errno from read
.done: pop rbx
    ret
