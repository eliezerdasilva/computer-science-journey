# Especificação — SysMonitor 2.0

## Objetivo

Monitor gráfico para Linux x86-64, com interface em C/GTK 4 e núcleo de coleta e processamento em Assembly NASM.

## Requisitos funcionais

| ID | Requisito | Estado nesta versão |
|---|---|---|
| RF01 | Exibir modelo e processadores lógicos | Implementado |
| RF02 | Calcular utilização agregada da CPU | Implementado por amostras sucessivas |
| RF03 | Exibir uso individual por CPU lógica | Implementado |
| RF04 | Exibir RAM total, disponível e usada | Implementado |
| RF05 | Exibir SWAP total e livre | Implementado |
| RF06 | Listar processos com PID, nome, estado e RSS | Implementado |
| RF07 | Encerrar processo pela interface | Não habilitado; API syscall preparada |
| RF08 | Exibir capacidade da partição raiz | Implementado |
| RF09 | Exibir tráfego RX/TX agregado | Implementado; delta por atualização |
| RF10 | Exibir temperatura do primeiro thermal zone | Implementado quando disponível |
| RF11 | Exibir uptime | Implementado |
| RF12 | Atualizar automaticamente e manualmente | Implementado |
| RF13 | Apresentar falhas/indisponibilidade sem encerrar a interface | Parcial; algumas métricas mantêm último valor se a leitura falhar |

## Requisitos não funcionais

- Linux x86-64 e NASM ELF64.
- Interface GTK 4.
- Coleta, parsing e cálculos em Assembly.
- Integração C/Assembly pela System V AMD64 ABI.
- Acesso somente leitura aos dados do sistema, exceto syscall `kill` que não é acionada pela interface.
- Buffers de tamanho fixo e limites para arrays de processos/sensores.

## Fontes de dados

- `/proc/cpuinfo`, `/proc/stat`
- `/proc/meminfo`, `/proc/uptime`
- `/proc/net/dev`, `/proc/[pid]/stat`
- `/sys/class/thermal/thermal_zone0/temp`
- syscall `statfs("/")`

## Fórmulas

Memória usada = MemTotal − MemAvailable.

Uso agregado de CPU = (delta_total − delta_idle) × 100 / delta_total.

Armazenamento usado = total_bytes − available_bytes.

Os deltas de rede são diferenças entre duas leituras sucessivas; como a atualização visual é periódica, o resultado é uma aproximação por intervalo e não uma taxa com relógio monotônico calibrado.
