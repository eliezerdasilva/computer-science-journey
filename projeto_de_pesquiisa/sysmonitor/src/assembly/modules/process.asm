extern sm_sys_open, sm_sys_close, sm_sys_getdents64, sm_read_file, sm_parse_u64, sm_sys_kill
global sm_read_processes, sm_send_signal
section .rodata
procdir: db '/proc',0
section .bss
dirbuf: resb 32768
statbuf: resb 4096
pathbuf: resb 64
pidtmp: resb 24
section .text
; SmProcess stride 80: pid@0, name@4, state@68, rss_kb@72.
sm_read_processes:
    push rbx
    push r12
    push r13
    push r14
    push r15
    mov rbx,rdi
    mov dword [rbx],0
    lea rdi,[rel procdir]
    xor esi,esi
    xor edx,edx
    call sm_sys_open
    test rax,rax
    js .error
    mov r12,rax
.read_batch:
    mov rdi,r12
    lea rsi,[rel dirbuf]
    mov edx,32768
    call sm_sys_getdents64
    test rax,rax
    jle .close
    lea r13,[rel dirbuf]
    lea r14,[r13+rax]
.next_entry:
    cmp r13,r14
    jae .read_batch
    movzx ecx,word [r13+16]
    test ecx,ecx
    jz .close
    lea rdi,[r13+19]
    movzx eax,byte [rdi]
    cmp al,'0'
    jb .advance
    cmp al,'9'
    ja .advance
    call sm_parse_u64
    cmp byte [rdx],0
    jne .advance
    mov r15,rax                 ; PID
    cmp dword [rbx],128
    jae .advance
    ; Build /proc/<pid>/stat.
    lea rdi,[rel pathbuf]
    mov byte [rdi],'/'
    mov byte [rdi+1],'p'
    mov byte [rdi+2],'r'
    mov byte [rdi+3],'o'
    mov byte [rdi+4],'c'
    mov byte [rdi+5],'/'
    lea rdi,[rel pidtmp+23]
    mov byte [rdi],0
    mov rax,r15
    mov r10,10
.pid_digits:
    xor edx,edx
    div r10
    add dl,'0'
    dec rdi
    mov [rdi],dl
    test rax,rax
    jnz .pid_digits
    lea rsi,[rel pidtmp+23]
    ; rdi currently points to first digit
    mov rdx,rsi
    mov rsi,rdi
    sub rdx,rsi
    mov rcx,rdx
    lea rdi,[rel pathbuf+6]
    rep movsb
    mov byte [rdi],'/'
    mov byte [rdi+1],'s'
    mov byte [rdi+2],'t'
    mov byte [rdi+3],'a'
    mov byte [rdi+4],'t'
    mov byte [rdi+5],0
    lea rdi,[rel pathbuf]
    lea rsi,[rel statbuf]
    mov edx,4096
    call sm_read_file
    test rax,rax
    js .advance
    ; Locate command name in parentheses and closing ') '.
    lea rsi,[rel statbuf]
.find_lparen:
    cmp byte [rsi],'('
    je .name_start
    cmp byte [rsi],0
    je .advance
    inc rsi
    jmp .find_lparen
.name_start:
    inc rsi
    mov rdi,rsi
.find_rparen:
    cmp byte [rdi],')'
    jne .check_end
    cmp byte [rdi+1],' '
    je .name_end
.check_end:
    cmp byte [rdi],0
    je .advance
    inc rdi
    jmp .find_rparen
.name_end:
    ; Destination record. Preserve the closing-parenthesis pointer.
    mov r9,rdi
    mov eax,[rbx]
    imul rax,rax,80
    lea r10,[rbx+16+rax]
    mov [r10],r15d
    ; Copy at most 63 chars and terminate.
    mov rcx,r9
    sub rcx,rsi
    cmp rcx,63
    jbe .copy_name
    mov ecx,63
.copy_name:
    lea rdi,[r10+4]
    rep movsb
    mov byte [rdi],0
    ; state is two bytes after closing parenthesis
    mov al,[r9+2]
    mov [r10+68],al
    ; Parse fields 4..24, RSS is the 21st numeric field after state.
    lea rsi,[r9+4]
    mov r11d,21
.parse_fields:
    mov rdi,rsi
    call sm_parse_u64
    mov rsi,rdx
    dec r11d
    jnz .parse_fields
    ; RSS is in pages; convert to KiB (4 KiB pages on supported x86 Linux).
    shl rax,2
    mov [r10+72],rax
    inc dword [rbx]
.advance:
    movzx ecx,word [r13+16]
    add r13,rcx
    jmp .next_entry
.close:
    mov rdi,r12
    call sm_sys_close
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
sm_send_signal:
    ; rdi=pid, rsi=signal
    jmp sm_sys_kill
