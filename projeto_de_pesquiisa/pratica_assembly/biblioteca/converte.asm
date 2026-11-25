%include 'bibliotecaE.asm'

section .data

    v1 dw '105', LF , NULL

section .text

global _start

_start:
    call converte_valor
    call mostrar_valor

    mov eax, SYS_EXIT
    xor ebx, ebx
    int SYS_CALL

converte_valor:
    lea esi, [v1]
    mov ecx, 3
    call string_to_int
    ret

mostrar_valor:
    call int_to_string
    call saidaResultado
    ret
; String para inteiro
; Entrada ESI valor de entrada ecx tamanho

string_to_int:
    xor ebx,ebx
.prox_digito:
    movzx eax, byte [esi]
    inc esi
    sub al, '0'
    imul ebx, 0xA
    add ebx, eax
    loop .prox_digito ; ecx é decrementado automaticamente, se ecx != 0, pula para .prox_digito
    mov eax, ebx
    ret

; Inteiro para string
; Entrada interio em EAX
; Saída Buffer TAM_BUFFER

int_to_string:
    lea esi, [BUFFER]
    add  esi, 0x9
    mov BYTE [esi], 0xA
    mov ebx, 0xA
.prox_digito:
    xor edx, edx
    div ebx
    add dl, '0'
    dec esi
    mov [esi], dl
    test eax, eax
    jnz .prox_digito
    ret
