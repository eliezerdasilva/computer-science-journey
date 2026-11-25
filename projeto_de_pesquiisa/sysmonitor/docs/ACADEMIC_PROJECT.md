# SysMonitor — Projeto acadêmico

## Tema

Monitoramento de recursos de um sistema Linux por meio de Assembly x86-64, integrado a uma interface gráfica desenvolvida em C com GTK 4.

## Problema e motivação

O projeto explora como informações expostas pelo kernel Linux podem ser acessadas em baixo nível, interpretadas sem bibliotecas de alto nível e apresentadas em uma aplicação gráfica. O foco está na interface entre aplicações e kernel, ABI, syscalls, representação de dados e modularização.

## Objetivo geral

Desenvolver um monitor de sistema no qual a camada de apresentação seja separada do núcleo de coleta e processamento, mantendo este núcleo em Assembly NASM.

## Objetivos específicos

- Aplicar a System V AMD64 ABI na integração entre C e Assembly.
- Implementar wrappers de syscalls Linux x86-64.
- Ler e interpretar interfaces de `/proc` e `/sys`.
- Calcular métricas de CPU, memória e tráfego de rede.
- Enumerar processos e consultar informações de estado e memória residente.
- Consultar capacidade de armazenamento e sensores térmicos.
- Construir uma interface GTK 4 com atualização periódica.
- Documentar limitações e validar resultados comparando-os com ferramentas e pseudoarquivos do Linux.

## Metodologia

1. Preservar a versão CLI e separar o núcleo reutilizável.
2. Definir estruturas compartilhadas em `sysmonitor.h`.
3. Implementar funções NASM exportadas para coleta de cada subsistema.
4. Implementar a interface GTK 4 como consumidora da API, sem parsing de dados do kernel em C.
5. Comparar as métricas com fontes equivalentes do sistema e executar testes de robustez.

## Resultados e limitações

A versão 2.0 implementa CPU agregada e por CPU lógica, RAM/SWAP, processos, partição raiz, tráfego agregado, thermal zone 0 e uptime. A enumeração completa de pontos de montagem e a descoberta de todos os sensores permanecem como evoluções. A interface não encerra processos; a syscall está encapsulada, mas não é acionada pela GUI.

## Possíveis extensões

- Percentual de utilização individual por núcleo.
- Descoberta de múltiplos sensores em `hwmon` e `thermal`.
- Lista de todos os sistemas de arquivos montados.
- Gráficos históricos e taxa de rede calibrada por relógio monotônico.
- Ação de encerramento de processo com confirmação explícita e tratamento de permissões.
- Testes automatizados dos parsers com dados simulados.
