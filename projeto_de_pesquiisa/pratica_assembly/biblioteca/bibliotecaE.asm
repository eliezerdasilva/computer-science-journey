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

    TAM_BUFFER equ 0xA 

segment .bss
    BUFFER resb 0xA

segment .text

saidaResultado:
    mov EAX , SYS_WRITE ; Chamada do sistema para escrever na tela
    mov EBX , STD_OUT ; Codigo de saida padrao
    mov ECX , BUFFER ; Endereco da variavel a ser escrita
    mov EDX , TAM_BUFFER ; Tamanho da variavel a ser escrita
    int SYS_CALL ; Interrupcao do sistema para escrever na tela
    ret