; Compilar - Transforma o programa em arquivo objeto
; nasm -f elf64 hello.asm -o hello.o 
; Linkeditar - Transforma o arquivo objeto em um executavel
; ld -s -o hello.o  hello

section .data
    ; 'Constantes'
    msg db 'Hello, World!', 0xA
    tan equ $- msg



section .text
    ; Variaveis
global _start
    
_start:
    ; destino , origem
    ; numero da syscall
    ; 1 exit, 3 read, 4 write, 5 open,  
    mov EAX, 0x4
    mov EBX, 0x1
    mov ECX, msg
    mov EDX, tan        
    int 0x80 
    