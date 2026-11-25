; ============================================================
; PROGRAMA: lê array[1] (valor 22), converte para string e imprime
; ============================================================

%include 'bibliotecaE.asm'          ; inclui constantes e rotinas da biblioteca
                                    ; (LF, NULL, SYS_CALL, SYS_EXIT, SYS_WRITE,
                                    ;  STD_OUT, RET_EXIT, mst_saida, tamStr)

; ------------------------------------------------------------
; SEÇÃO DE DADOS INICIALIZADOS
; ------------------------------------------------------------
section .data
    array dd 10, 22, 13, 14, 55     ; define 5 dwords (4 bytes cada):
                                    ;   array+0  = 10
                                    ;   array+4  = 22
                                    ;   array+8  = 13
                                    ;   array+12 = 14
                                    ;   array+16 = 55

; ------------------------------------------------------------
; SEÇÃO DE DADOS NÃO INICIALIZADOS
; ------------------------------------------------------------
section .bss
    BUFFER resb 0xA                 ; reserva 10 bytes para o buffer de saída
    TAM_BUFFER equ 0xA              ; constante: tamanho do buffer = 10

; ------------------------------------------------------------
; SEÇÃO DE CÓDIGO
; ------------------------------------------------------------
section .text
global _start                       ; torna _start visível ao linker (ponto de entrada)

; ============================================================
; PONTO DE ENTRADA
; ============================================================
_start:
    mov ECX, 1                      ; ECX = índice 1 (queremos array[1])
    mov EAX, [array + ECX*4]        ; EAX = valor em array + (1*4) = array+4 = 22
                                    ; (escala *4 porque cada elemento tem 4 bytes)

    call int_to_string              ; converte EAX (22) para string no BUFFER
                                    ; ao retornar, ESI aponta para o 1º dígito no buffer

    mov ECX, ESI                    ; ECX = endereço do início do número (para write)
    lea EDX, [BUFFER + 0xA]         ; EDX = endereço do fim do buffer (BUFFER + 10)
    sub EDX, ESI                    ; EDX = tamanho = fim - início (nº de bytes a imprimir)

    mov EAX, SYS_WRITE              ; EAX = 4 (syscall write)
    mov EBX, STD_OUT                ; EBX = 1 (fd = stdout)
    int SYS_CALL                    ; chama o kernel: escreve EDX bytes de ECX na tela

    mov EAX, SYS_EXIT               ; EAX = 1 (syscall exit)
    mov EBX, RET_EXIT               ; EBX = 0 (código de retorno = sucesso)
    int SYS_CALL                    ; encerra o processo

; ============================================================
; ROTINA: int_to_string
; Converte o inteiro em EAX para string decimal no BUFFER
; Entrada: EAX = número
; Saída:   BUFFER preenchido (número + LF), ESI = início do número
; ============================================================
int_to_string:
    lea ESI, [BUFFER]               ; ESI = endereço inicial do buffer
    add ESI, 0x9                    ; ESI = offset 9 (último byte do buffer de 10)

    mov BYTE [ESI], 0xA             ; grava LF (0x0A) no offset 9 (quebra de linha)

    mov EBX, 0xA                    ; EBX = 10 (divisor para extrair dígitos)

    test EAX, EAX                   ; EAX == 0? (testa sem alterar EAX)
    jnz .prox_digito                ; se EAX != 0, vai para o loop normal

    dec ESI                         ; caso EAX == 0: volta uma posição
    mov BYTE [ESI], '0'             ; grava '0' (representação de zero)
    ret                             ; retorna (nada mais a fazer)

.prox_digito:
    xor EDX, EDX                    ; EDX = 0 (obrigatório antes de div: EDX:EAX)
    div EBX                         ; divide EDX:EAX por 10:
                                    ;   EAX = quociente
                                    ;   EDX = resto (dígito extraído)

    add DL, '0'                     ; converte o resto (0-9) para ASCII ('0'-'9')
    dec ESI                         ; volta uma posição no buffer (grava de trás pra frente)
    mov [ESI], DL                   ; grava o caractere no buffer

    test EAX, EAX                   ; EAX (quociente) == 0?
    jnz .prox_digito                ; se ainda há dígitos, repete

    ret                             ; fim: ESI aponta para o 1º dígito do número