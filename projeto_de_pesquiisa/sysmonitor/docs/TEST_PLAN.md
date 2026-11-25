# Plano de testes

## Compilação

- [ ] `make check-deps` identifica GCC, NASM e GTK 4.
- [ ] `make` gera `build/sysmonitor` sem warnings inesperados.
- [ ] `file build/sysmonitor` identifica ELF x86-64.

## Execução e dados

- [ ] Janela abre e atualiza sem bloquear o loop GTK.
- [ ] CPU: comparar modelo/quantidade com `/proc/cpuinfo`.
- [ ] CPU: comparar percentual agregado e de cada CPU lógica com amostras de `/proc/stat`.
- [ ] RAM/SWAP: comparar valores com `/proc/meminfo`.
- [ ] Uptime: comparar com `/proc/uptime`.
- [ ] Rede: comparar bytes com `/proc/net/dev` (somatório das interfaces não loopback).
- [ ] Processos: comparar PIDs e estados com `/proc/[pid]/stat`; validar RSS.
- [ ] Armazenamento: comparar com `df -B1 /`.
- [ ] Temperatura: comparar com o arquivo thermal zone quando existir.
- [ ] Atualização manual e automática funcionam.
- [ ] Sistema sem thermal zone continua exibindo o restante das métricas.

## Limites e robustez

- [ ] Mais de 128 processos: lista limitada sem sobrescrever memória.
- [ ] Arquivos de sensores ausentes ou inacessíveis não encerram a aplicação.
- [ ] Executar sem privilégios de root.
- [ ] Verificar comportamento em máquina com `/proc` restrito.

> O ambiente de geração deste pacote não possui NASM nem GTK 4; os testes de compilação e execução precisam ser realizados no Debian de desenvolvimento.
