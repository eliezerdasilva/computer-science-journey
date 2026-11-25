%include 'bibliotecaE.asm'

section .data
    msg1: db 'Parte 1', LF, NULL
    msg2: db 'Parte 2', LF, NULL
    msg3: db 'Parte 3', LF, NULL   
    msg4: db 'Parte 4', LF, NULL

section .text

global _start

_start:
    mov eax, 0x4
    mov ebx, 0x1
    mov ecx, msg1
    mov edx, 0x1A
    int 0x80

    mov eax, 0x1
    mov ebx, 0x0
    int 0x80