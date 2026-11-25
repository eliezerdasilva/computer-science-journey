# SysMonitor 2.0

Monitor gráfico de recursos para Linux x86-64. A interface é escrita em C com GTK 4; a coleta, leitura de pseudoarquivos, parsing e cálculos são implementados em Assembly NASM.

## Funcionalidades implementadas nesta versão

- CPU: modelo, quantidade de processadores lógicos, utilização agregada e percentual individual por CPU lógica calculados por deltas de `/proc/stat` entre atualizações.
- RAM e SWAP: total, disponível/livre e memória utilizada via `/proc/meminfo`.
- Processos: enumeração de `/proc`, PID, nome, estado e RSS em KiB. A interface é somente leitura nesta versão; a syscall `kill` está encapsulada para uma futura ação explícita de gerenciamento.
- Armazenamento: capacidade total, usada e disponível da partição raiz via syscall `statfs`.
- Rede: bytes recebidos/transmitidos agregados via `/proc/net/dev`; o delta exibido é por amostra de atualização (aproximadamente 1 s), não uma taxa calibrada em tempo real.
- Temperatura: leitura de `/sys/class/thermal/thermal_zone0/temp`, quando o kernel disponibiliza esse sensor.
- Uptime: dias, horas, minutos e segundos via `/proc/uptime`.
- Atualização periódica e botão de atualização manual.

## Arquitetura

- `src/c/`: janela GTK 4, widgets, atualização e apresentação.
- `src/assembly/core/`: wrappers de syscalls e rotinas reutilizáveis de leitura/parsing.
- `src/assembly/modules/`: CPU, memória, uptime, rede, processos, armazenamento e sensores.
- `src/include/sysmonitor.h`: estruturas e funções da API C/Assembly.
- `legacy/cli-v1/`: fontes da versão de terminal original, preservadas para consulta.
- `docs/`: arquitetura, API, especificação, metodologia acadêmica e plano de testes.

## Dependências (Debian 13)

```bash
sudo apt update
sudo apt install build-essential nasm pkg-config libgtk-4-dev
```

## Compilação e execução

Na raiz do projeto:

```bash
make check-deps
make
./build/sysmonitor
```

O `Makefile` foi simplificado para compilar objetos NASM e C e linkar pelo GCC com as bibliotecas GTK 4 detectadas pelo `pkg-config`. `make clean` remove somente `build/`.

## Limitações conhecidas

- O detalhamento individual segue as linhas `cpuN` de `/proc/stat` (CPUs lógicas, não necessariamente núcleos físicos).
- O sensor térmico inicial consulta apenas `thermal_zone0`; nomes e disponibilidade variam conforme hardware e drivers.
- O armazenamento apresenta a partição raiz `/`, não uma lista completa de todos os pontos de montagem.
- O tráfego de rede é agregado entre interfaces e a diferença entre amostras é mostrada como delta por intervalo aproximado de atualização.
- O gerenciamento de processos é de monitoramento/listagem. Encerrar processos pela interface não foi habilitado para evitar uma ação destrutiva acidental.
- A compilação e execução devem ser validadas em uma máquina Debian/Linux x86-64 com NASM e GTK 4 instalados. O ambiente usado para preparar este pacote não possui NASM nem GTK 4, portanto não foi possível afirmar que o build foi validado aqui.
