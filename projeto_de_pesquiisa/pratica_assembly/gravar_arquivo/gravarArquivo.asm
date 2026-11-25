%include 'biblioteca.asm'

section .data
    msg db 'Hello world',LF
    tamMsg equ $ - msg
    arq db 'Hello',NULL
    tamArq equ $ -arq
    fd dq 0 ; FILE descriptor

section .text


global _start

_start: 
    mov eax, CREATE_FILE
    mov ebx, arq
    mov ecx, 0o664  ; Octal permissao  
    mov edx, tamArq
    int SYS_CALL 

escrever:
    mov [fd], eax 
    mov eax, WRITE_FILE
    mov ebx, [fd]
    mov ecx, msg
    mov edx, tamMsg
    int SYS_CALL

fechar: 
    mov eax, CLOSE_FILE
    mov ebx, [fd]
    int SYS_CALL

termino:
    mov eax,SYS_EXIT
    mov ebx,RET_EXIT
    int SYS_CALL
    