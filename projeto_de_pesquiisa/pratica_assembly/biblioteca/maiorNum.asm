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
    x dd 5 ; db 1 byte dw 2 bytes, dd 4 bytes, dq 8 bytes dt 10 bytes
    y dd 10
    msg1 db "X maior que Y", LF, NULL
    tan1 equ $- msg1
    msg2 db "Y maior que X", LF, NULL
    tan2 equ $- msg2

section .text

global _start

_start: 
    ; word 2 bytes, dword 4 bytes, qword 8 bytes
    mov EAX, DWORD [x] ; Carrega o valor de x em EAX
    mov EBX, DWORD [y] ; Carrega o valor de y
    ; Comparacao
    cmp EAX, EBX ; Compara o valor de x com o valor de y
    ; je = jg > jge >= jl < jle <= jne !=
    JGE maior ; Se x >= y, pula para a label maior
    ; Se x < y, escreve a mensagem msg2
    mov ECX, msg2 ; Endereco da mensagem a ser escrita
    mov EDX, tan2 ; Tamanho da mensagem a ser escrita
    jmp final ; Pula para o fim do programa

maior: 
    mov ECX, msg1 ; Endereco da mensagem a ser escrita
    mov EDX, tan1 ; Tamanho da mensagem a ser escrita       

final: 
    mov EAX, SYS_WRITE ; Chamada do sistema para escrever na tela
    mov EBX, STD_OUT ; Codigo de saida padrao
    int SYS_CALL ; Chamada do sistema   

    mov EAX, SYS_EXIT
    mov EBX, RET_EXIT ; Codigo de retorno do programa   
    int SYS_CALL ; Chamada do sistema   