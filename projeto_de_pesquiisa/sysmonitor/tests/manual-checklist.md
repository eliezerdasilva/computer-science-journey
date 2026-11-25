# Checklist manual — SysMonitor 2.0

- [ ] Verificar dependências com `make check-deps`.
- [ ] Compilar com `make`.
- [ ] Abrir a janela GTK 4.
- [ ] Conferir CPU e processadores lógicos com `/proc/cpuinfo`.
- [ ] Conferir RAM e SWAP com `/proc/meminfo`.
- [ ] Conferir uptime com `/proc/uptime`.
- [ ] Conferir tráfego agregado com `/proc/net/dev`.
- [ ] Conferir lista de processos com `/proc`.
- [ ] Conferir partição raiz com `stat -f /` ou `df -B1 /`.
- [ ] Conferir temperatura se `/sys/class/thermal/thermal_zone0/temp` existir.
- [ ] Testar atualização automática e manual.
- [ ] Testar em conta sem privilégios administrativos.
- [ ] Confirmar que a ausência de sensor não encerra a aplicação.
