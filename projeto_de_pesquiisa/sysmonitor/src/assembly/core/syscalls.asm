; Linux x86-64 syscall wrappers. System V AMD64 ABI.
%define SYS_READ 0
%define SYS_WRITE 1
%define SYS_OPEN 2
%define SYS_CLOSE 3
%define SYS_NANOSLEEP 35
%define SYS_KILL 62
%define SYS_GETDENTS64 217
%define SYS_STATFS 137
%define SYS_EXIT 60

global sm_sys_read, sm_sys_open, sm_sys_close, sm_sys_getdents64, sm_sys_statfs, sm_sys_kill
section .text
sm_sys_read:    mov eax, SYS_READ
                syscall
                ret
sm_sys_open:    mov eax, SYS_OPEN
                syscall
                ret
sm_sys_close:   mov eax, SYS_CLOSE
                syscall
                ret
sm_sys_getdents64: mov eax, SYS_GETDENTS64
                syscall
                ret
sm_sys_statfs:  mov eax, SYS_STATFS
                syscall
                ret
sm_sys_kill:    mov eax, SYS_KILL
                syscall
                ret
