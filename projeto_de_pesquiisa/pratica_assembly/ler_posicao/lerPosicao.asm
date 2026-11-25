%include  'biblioteca.asm'

section .data
    arq db "exemplo.txt"
    tam equ 1301

section .bss
    fd resb 4
    buffer  resb 1301

section .text

global _start

_start:
    mov eax, OPEN_FILE
    mov ebx, arq
    mov ecx, OPEN_READ
    int SYS_CALL
    mov [fd],eax

posicionar:
    mov eax, SEEK_FILE
    mov ebx, [fd]
    mov ecx, -20
    mov edx, SEEK_END
    int SYS_CALL

ler:
    mov eax, READ_FILE
    mov ebx, [fd]
    mov ecx, buffer
    mov edx, tam
    int SYS_CALL


saidaNoConsole:
    mov eax, SYS_WRITE
    mov ebx, STD_OUT
    mov ecx, buffer
    mov edx, tam 
    int SYS_CALL

fechar:
    mov eax, CLOSE_FILE
    mov ebx, [fd]
    int SYS_CALL

termino: 
    mov eax, SYS_EXIT
    mov ebx, RET_EXIT
    int SYS_CALL