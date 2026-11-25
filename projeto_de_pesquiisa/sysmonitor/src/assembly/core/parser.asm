global sm_parse_u64, sm_copy_string, sm_read_file
extern sm_sys_open, sm_sys_read, sm_sys_close
section .text
; rdi = decimal string; returns rax=value, rdx=end pointer
sm_parse_u64:
    xor eax,eax
    mov rdx,rdi
.skip: cmp byte [rdx],' '
    je .inc
    cmp byte [rdx],9
    jne .digits
.inc: inc rdx
    jmp .skip
.digits:
    movzx ecx,byte [rdx]
    cmp cl,'0'
    jb .done
    cmp cl,'9'
    ja .done
    imul rax,rax,10
    sub ecx,'0'
    add rax,rcx
    inc rdx
    jmp .digits
.done: ret

; rdi=source, rsi=dest, rdx=max bytes; copies until NUL/newline/max and NUL-terminates
sm_copy_string:
    xor eax,eax
.loop: cmp rax,rdx
    jae .finish
    mov cl,[rdi+rax]
    test cl,cl
    jz .finish
    cmp cl,10
    je .finish
    mov [rsi+rax],cl
    inc rax
    jmp .loop
.finish: mov byte [rsi+rax],0
    ret

; rdi=path, rsi=buffer, rdx=capacity. Returns bytes or negative errno.
sm_read_file:
    push rbx
    push r12
    push r13
    mov r12,rdi
    mov r13,rsi
    mov rbx,rdx
    mov rdi,r12
    xor esi,esi
    xor edx,edx
    call sm_sys_open
    test rax,rax
    js .out
    mov r12,rax
    mov rdi,rax
    mov rsi,r13
    lea rdx,[rbx-1]
    call sm_sys_read
    mov rbx,rax
    mov rdi,r12
    call sm_sys_close
    test rbx,rbx
    js .readerr
    mov byte [r13+rbx],0
    mov rax,rbx
    jmp .out
.readerr: mov rax,rbx
.out: pop r13
    pop r12
    pop rbx
    ret
