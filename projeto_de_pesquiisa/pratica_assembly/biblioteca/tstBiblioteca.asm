%include  'bibliotecaE.asm'

section .text
global _start

_start:
    ; lea seria um mov, porem ele carrega o endereco de memoria da variavel e nao o valor da variavel e pode ser usado para fazer calculos com o endereco de memoria da variavel
    lea esi, [BUFFER]; Load Effective Address - Carrega o endereco de memoria da variavel | esi = endereco de memoria da variavel
    add esi, 0x9 ; Adiciona 0x9 ao endereco de memoria da variavel      
    mov BYTE [esi], 0xA ; Coloca o valor 0x0 no endereco de memoria da variavel

    ; esi = endereco da memoria da variavel 

    dec esi
    mov dl, 0x11 ; A 
    add dl, '0' ; Converte o valor de A para o seu equivalente em ASCII
    mov [esi], dl ; Coloca o valor de A no endereco de memoria da variavel

    dec esi
    mov dl, 0x12 ; B
    add dl, '0' ; Converte o valor de A para o seu equivalente em ASCII
    mov [esi], dl ; Coloca o valor de A no endereco de memoria da variavel

    call saidaResultado ; Chama a funcao saidaResultado para escrever na tela o valor da variavel
    
    mov eax, SYS_EXIT ; Chamada do sistema para sair do programa
    mov ebx, RET_EXIT ; Codigo de retorno do programa | Sucesso
    int SYS_CALL ; Interrupcao do sistema para sair do programa