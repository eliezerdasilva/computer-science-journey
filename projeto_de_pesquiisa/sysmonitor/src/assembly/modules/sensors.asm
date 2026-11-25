extern sm_read_file, sm_parse_u64
global sm_read_sensors
section .rodata
sensor_path: db '/sys/class/thermal/thermal_zone0/temp',0
sensor_label: db 'thermal_zone0',0
section .bss
sensor_buf: resb 64
section .text
; SmSensor starts after 12 + 128*80 bytes; stride 104 (label[96], int64 temp).
sm_read_sensors:
    push rbx
    mov rbx,rdi
    lea rdi,[rel sensor_path]
    lea rsi,[rel sensor_buf]
    mov edx,64
    call sm_read_file
    test rax,rax
    js .none
    lea rdi,[rel sensor_buf]
    call sm_parse_u64
    mov r8,rax
    ; populate first sensor
    lea rdx,[rbx+16+10240]
    lea rsi,[rel sensor_label]
    mov ecx,13
.copy: mov al,[rsi]
    mov [rdx],al
    inc rsi
    inc rdx
    test al,al
    jz .temp
    dec ecx
    jnz .copy
.temp: mov [rbx+16+10240+96],r8
    mov dword [rbx+4],1
    xor eax,eax
    jmp .done
.none: mov dword [rbx+4],0
    xor eax,eax
.done: pop rbx
    ret
