segment .data
    LF equ 0xA ; Line Feed
    NULL equ 0x0 ; Final da String
    SYS_CALL equ 0x80 ; Codigo de chamada do sistema | Envia informacoes para o kernel
    ; eax
    SYS_EXIT equ 0x1 ; Codigo de chamada do sistema para sair do programa
    SYS_READ equ 0x3 ; Codigo de chamada do sistema para ler da tela
    SYS_WRITE equ 0x4 ; Codigo de chamada do sistema para escrever na tela
    ; ebx
    RET_EXIT equ 0x0 ; Codigo de retorno do programa | Sucesso
    STD_IN equ 0x0 ; Codigo de entrada padrao
    STD_OUT equ 0x1 ; Codigo de saida padrao

section .data
    ; 'Constantes'
    msg db "Entre com seu nome: ", LF, NULL
    tan equ $- msg

section .bss
    ; 'Variaveis'
    ; resb - Reserva bytes na memoria para a variavel
    nome resb 1 ; Reserva 1 bytes para a variavel nome

section .text

global _start

_start:

    mov EAX, SYS_WRITE ; Chamada do sistema para escrever na tela
    ; o EBX define aonde vai sair teclado, no caso a tela
    mov EBX, STD_OUT ; Codigo de saida padrao
    mov ECX, msg ; Endereco da mensagem a ser escrita
    mov EDX, tan ; Tamanho da mensagem a ser escrita
    int SYS_CALL ; Chamada do sistema   

    mov EAX, SYS_READ ; Chamada do sistema para ler da tela
    mov EBX, STD_IN ; Codigo de entrada padrao
    mov ECX, nome ; Endereco da variavel a ser lida
    mov EDX, 0xA ; Tamanho da variavel a ser lida
    int SYS_CALL ; Chamada do sistema

    mov EAX, SYS_EXIT
    mov EBX, RET_EXIT ; Codigo de retorno do programa   
    int SYS_CALL ; Chamada do sistema