# Arquitetura do SysMonitor 2.0

## Separação de responsabilidades

```text
┌──────────────────────────────────────────────┐
│                 GTK 4 / C                    │
│ Janela, widgets, atualização visual, eventos  │
└──────────────────────┬───────────────────────┘
                       │ System V AMD64 ABI
┌──────────────────────▼───────────────────────┐
│               API sysmonitor.h               │
│       estruturas de dados compartilhadas     │
└──────────────────────┬───────────────────────┘
                       │
┌──────────────────────▼───────────────────────┐
│              Assembly NASM x86-64            │
│ CPU | RAM/SWAP | processos | disco | rede    │
│ sensores | uptime | parsing | conversões     │
└──────────────────────┬───────────────────────┘
                       │ syscalls Linux
┌──────────────────────▼───────────────────────┐
│                  Kernel Linux                │
│ /proc, /sys, getdents64, statfs, kill         │
└──────────────────────────────────────────────┘
```

O C não abre pseudoarquivos, não faz parsing e não calcula métricas. Ele chama as funções exportadas pelo Assembly e apresenta os campos recebidos. Os callbacks GTK apenas coordenam atualização e interação.

## ABI e syscalls

As funções chamadas pelo C seguem a System V AMD64 ABI: argumentos em RDI, RSI, RDX, RCX, R8 e R9; retorno inteiro em RAX; RBX, RBP e R12–R15 preservados. Antes de cada `call`, a pilha deve estar alinhada em 16 bytes. As syscalls Linux usam RAX para o número e RDI, RSI, RDX, R10, R8 e R9 para argumentos; RCX e R11 são destruídos.

## Módulos Assembly

| Arquivo | Responsabilidade |
|---|---|
| `core/syscalls.asm` | Wrappers para `read`, `open`, `close`, `getdents64`, `statfs` e `kill`. |
| `core/parser.asm` | Leitura limitada de arquivos, conversão decimal e cópia de strings. |
| `modules/cpu.asm` | Modelo, processadores lógicos e utilização agregada por deltas de `/proc/stat`. |
| `modules/memory.asm` | RAM e SWAP via `/proc/meminfo`. |
| `modules/uptime.asm` | Tempo de atividade via `/proc/uptime`. |
| `modules/network.asm` | Contadores agregados de `/proc/net/dev`. |
| `modules/process.asm` | Enumeração de `/proc` com `getdents64`; leitura de PID, nome, estado e RSS. |
| `modules/storage.asm` | Capacidade da raiz via syscall `statfs`. |
| `modules/sensors.asm` | Leitura de `thermal_zone0` em `/sys/class/thermal`. |

## Contrato C/Assembly

`src/include/sysmonitor.h` define estruturas fixas. A estrutura `SmLists` possui um campo reservado de alinhamento após os três contadores; por isso os offsets dos arrays devem permanecer sincronizados com os comentários nos módulos Assembly. Alterar campos ou tamanhos exige revisar os offsets usados em NASM.

## Limitações técnicas atuais

O detalhamento da CPU segue CPUs lógicas (`cpu0`, `cpu1` etc.), não núcleos físicos. Armazenamento está limitado à raiz `/`; sensores, ao primeiro thermal zone; rede, a contadores agregados. O módulo de processos é somente leitura. `sm_send_signal` encapsula a syscall `kill`, mas a interface não oferece botão para encerramento.
