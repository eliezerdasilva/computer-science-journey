# API C/Assembly

Todas as funções retornam `0` em sucesso ou um valor negativo em falha (quando a syscall subjacente retorna erro). Os ponteiros recebidos devem apontar para estruturas alocadas pelo chamador.

| Função | Saída | Origem |
|---|---|---|
| `sm_read_cpu(SmCpuInfo *)` | Modelo, processadores lógicos, percentual agregado e por CPU lógica | `/proc/cpuinfo`, `/proc/stat` |
| `sm_read_memory(SmMemoryInfo *)` | RAM e SWAP em KiB | `/proc/meminfo` |
| `sm_read_uptime(SmUptimeInfo *)` | Segundos de atividade | `/proc/uptime` |
| `sm_read_network(SmNetworkInfo *)` | RX/TX acumulado e delta por amostra | `/proc/net/dev` |
| `sm_read_processes(SmLists *)` | Até 128 processos | `getdents64`, `/proc/[pid]/stat` |
| `sm_read_storage(SmLists *)` | Partição raiz | `statfs("/")` |
| `sm_read_sensors(SmLists *)` | Thermal zone 0, se disponível | `/sys/class/thermal/thermal_zone0/temp` |
| `sm_send_signal(pid, signal)` | Envia sinal Linux ao PID | syscall `kill` |

`sm_send_signal` está exposta na API, mas não é chamada pela interface gráfica. A aplicação atual é somente leitura quanto a processos.

## Layouts compartilhados

O arquivo `tests/layout_check.c` contém `_Static_assert` para validar os offsets e tamanhos das estruturas usadas diretamente pelos módulos Assembly. Execute `make test-layout` depois de alterar `sysmonitor.h`.
