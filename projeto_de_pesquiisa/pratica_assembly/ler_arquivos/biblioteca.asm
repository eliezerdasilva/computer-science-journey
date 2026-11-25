segment .data
    LF equ 0xA ; Line Feed
    NULL equ 0x0 ; Final da String
    

    SYS_EXIT equ 0x1    ; Codigo de chamada do sistema para sair do programa
    RET_EXIT equ 0x0    ; Codigo de retorno do programa | Sucesso

    STD_IN equ 0x0      ; Codigo de entrada padrao
    STD_OUT equ 0x1     ; Codigo de saida padrao
    SYS_READ equ 0x3    ; Codigo de chamada do sistema para ler da tela
    SYS_WRITE equ 0x4   ; Codigo de chamada do sistema para escrever na tela    

    READ_FILE equ 0x3   ; Ler arquivo
    WRITE_FILE equ 0x4  ;
    OPEN_FILE equ 0x5   ;
    CLOSE_FILE equ 0x6  ;
    CREATED_FILE equ 0x8 ;

    OPEN_READ equ 0x0    ; Arquivo para leitura
    OPEN_WRITE equ 0x1   ; Arquivo para escrita
    OPEN_RW equ 0x2      ; Arquivo para Leitura/escrita
    OPEN_CREATE equ 0x40 ;Se o arquivo nao existe cria
    OPEN_APPEND equ 0x400; Arquivo para adicao de  informaćao

    


    SYS_CALL equ 0x80 ; Codigo de chamada do sistema | Envia informacoes para o kernel
