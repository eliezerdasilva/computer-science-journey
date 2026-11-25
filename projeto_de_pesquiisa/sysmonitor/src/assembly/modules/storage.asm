extern sm_sys_statfs
global sm_read_storage
section .rodata
root_path: db '/',0
section .bss
statfs_buf: resb 128
section .text
; SmStorageInfo stride 120; first entry at lists+11920 (16 + 128*80 + 16*104).
; C layout: three counters plus reserved word (16 bytes), processes (128*80), sensors (16*104), then storage.
; This module records root filesystem only in the first storage slot.
sm_read_storage:
    push rbx
    mov rbx,rdi
    lea rdi,[rel root_path]
    lea rsi,[rel statfs_buf]
    call sm_sys_statfs
    test rax,rax
    js .err
    ; statfs x86-64: f_bsize@8, f_blocks@16, f_bavail@32
    mov rax,[rel statfs_buf+8]
    imul rax,[rel statfs_buf+16]
    mov [rbx+11920],rax
    mov rax,[rel statfs_buf+8]
    imul rax,[rel statfs_buf+32]
    mov [rbx+11928],rax
    mov rdx,[rbx+11920]
    sub rdx,[rbx+11928]
    mov [rbx+11936],rdx
    mov byte [rbx+11944],'/'
    mov byte [rbx+11945],0
    mov dword [rbx+8],1
    xor eax,eax
    jmp .done
.err: mov rax,-1
.done: pop rbx
    ret
