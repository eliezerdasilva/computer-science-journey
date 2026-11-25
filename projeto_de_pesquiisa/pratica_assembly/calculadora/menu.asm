%include 'bibliotecaE.asm'

section .data
    tit      db LF, '+--------------------+', LF, '| Conversor de Base |', LF, '+--------------------+', LF, NULL
    obVal1   db LF, 'Digite o valor 1: ', NULL
    obVal2   db LF, 'Digite o valor 2: ', NULL
    opc1     db LF, '1. Adicionar', NULL
    opc2     db LF, '2. Subtrair', NULL
    opc3     db LF, '3. Multiplicar', NULL
    opc4     db LF, '4. Dividir', NULL
    msgOpc   db LF, 'Escolha uma opcao: ', NULL
    msgErro  db LF, 'Opcao invalida!', LF, NULL
    p1       db LF, 'Processo de adicao', LF, NULL
    p2       db LF, 'Processo de subtracao', LF, NULL
    p3       db LF, 'Processo de multiplicacao', LF, NULL
    p4       db LF, 'Processo de divisao', LF, NULL
    msgRes   db LF, 'Resultado: ', NULL
    msgFim   db LF, 'Fim do programa!', LF, NULL

section .bss
    opc       resb 0x2
    num1      resb 0x10      ; buffer maior para entrada
    num2      resb 0x10
    valor1    resd 1         ; inteiros convertidos
    valor2    resd 1
    resultado resd 1
    BUFFER    resb 0xA       ; buffer para int_to_string
    TAM_BUFFER equ 0xA

section .text
global _start

_start:
    ; --- título ---
    mov ECX, tit
    call mst_saida

    ; --- lê valor 1 ---
    mov ECX, obVal1
    call mst_saida
    mov EAX, SYS_READ
    mov EBX, STD_IN
    mov ECX, num1
    mov EDX, 0x10 ; edx serve para informar o tamanho do buffer
    int SYS_CALL

    ; --- lê valor 2 ---
    mov ECX, obVal2
    call mst_saida
    mov EAX, SYS_READ
    mov EBX, STD_IN
    mov ECX, num2
    mov EDX, 0x10
    int SYS_CALL

    ; --- menu ---
    mov ECX, opc1
    call mst_saida
    mov ECX, opc2
    call mst_saida
    mov ECX, opc3
    call mst_saida
    mov ECX, opc4
    call mst_saida

    mov ECX, msgOpc
    call mst_saida
    mov EAX, SYS_READ
    mov EBX, STD_IN
    mov ECX, opc
    mov EDX, 0x2
    int SYS_CALL

    ; --- escolhe operação ---
    mov AL, [opc]  ; copia o primeiro byte da opção escolhida para AL
    sub AL, '0' ; subtrai '0' para converter de ASCII para inteiro que é 0x30
    cmp AL, 1
    je adicionar
    cmp AL, 2
    je subtrair
    cmp AL, 3
    je multiplicar
    cmp AL, 4
    je dividir
    mov ECX, msgErro
    call mst_saida
    jmp saida

; =========================================================
; OPERAÇÕES
; =========================================================
adicionar:
    mov ECX, p1 
    call mst_saida
    call converte_operandos
    mov EAX, [valor1]
    add EAX, [valor2]
    mov [resultado], EAX
    jmp mostra_resultado

subtrair:
    mov ECX, p2
    call mst_saida
    call converte_operandos
    mov EAX, [valor1]
    sub EAX, [valor2]
    mov [resultado], EAX
    jmp mostra_resultado

multiplicar:
    mov ECX, p3
    call mst_saida
    call converte_operandos
    mov EAX, [valor1]
    imul EAX, [valor2]
    mov [resultado], EAX
    jmp mostra_resultado

dividir:
    mov ECX, p4
    call mst_saida
    call converte_operandos
    xor EDX, EDX              ; obrigatório antes do div
    mov EAX, [valor1]
    div DWORD [valor2]
    mov [resultado], EAX      ; quociente
    jmp mostra_resultado

; =========================================================
; CONVERTE num1 e num2 para inteiros
; =========================================================
converte_operandos:
    lea ESI, [num1] ; pega possição do buffer num1
    call conta_digitos        ; o retorno em ECX = quantidade de dígitos
    call string_to_int
    mov [valor1], EAX

    lea ESI, [num2]
    call conta_digitos
    call string_to_int
    mov [valor2], EAX
    ret

; =========================================================
; conta_digitos: conta dígitos até '\n' ou NULL
; Entrada: ESI = endereço da string
; Saída:   ECX = quantidade de dígitos
; =========================================================
conta_digitos:
    mov ECX, 0
.loop:
    mov AL, [ESI + ECX] ; pega o byte da string mais o próximo dígito   
    cmp AL, LF          ;   compara com o caractere de nova linha (quebra de linha)    
    je .fim             ;  se for igual, termina o loop
    cmp AL, NULL        ;   compara com o caractere nulo
    je .fim             ;   se for igual, termina o loop
    inc ECX             ;   incrementa o contador de dígitos
    jmp .loop
.fim:
    ret

; =========================================================
; MOSTRA RESULTADO
; =========================================================
mostra_resultado:
    mov ECX, msgRes
    call mst_saida
    mov EAX, [resultado]
    call int_to_string
    call print_buffer
    jmp saida

; =========================================================
; print_buffer: imprime BUFFER (TAM_BUFFER bytes)
; =========================================================
print_buffer:
    mov EAX, SYS_WRITE
    mov EBX, STD_OUT
    mov ECX, BUFFER
    mov EDX, TAM_BUFFER
    int SYS_CALL
    ret

; =========================================================
; string_to_int (da lib, incluída aqui)
; Entrada: ESI = string, ECX = tamanho
; Saída:   EAX = número
; =========================================================
string_to_int:
    xor EBX, EBX ; zera EBX para acumular o resultado
.prox_digito:
    movzx EAX, BYTE [ESI] ; pega o próximo dígito da string que esta em ESI
    inc ESI               ; incrementa ESI para apontar para o próximo dígito
    sub AL, '0'           ; converte de ASCII para inteiro
    imul EBX, 0xA         ; multiplica o valor acumulado por 10
    add EBX, EAX
    loop .prox_digito     ; isso acontence até ECX = 0, ou seja, até processar todos os dígitos
    mov EAX, EBX
    ret

; =========================================================
; int_to_string (da lib, incluída aqui)
; Entrada: EAX = número
; Saída:   BUFFER preenchido
; =========================================================
int_to_string:
    lea ESI, [BUFFER]
    add ESI, 0x9
    mov BYTE [ESI], 0xA
    mov EBX, 0xA
.prox_digito:
    xor EDX, EDX
    div EBX
    add DL, '0'
    dec ESI
    mov [ESI], DL
    test EAX, EAX
    jnz .prox_digito
    ret

; =========================================================
; SAÍDA
; =========================================================
saida:
    mov ECX, msgFim
    call mst_saida
    mov EAX, SYS_EXIT
    mov EBX, RET_EXIT
    int SYS_CALL