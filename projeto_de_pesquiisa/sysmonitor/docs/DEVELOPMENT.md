# Desenvolvimento

## Ambiente

Debian 13 / Linux x86-64, GCC, NASM, Make, pkg-config e GTK 4 (`libgtk-4-dev`).

## Dependências

```bash
sudo apt update
sudo apt install build-essential nasm pkg-config libgtk-4-dev
```

## Build seguro

Antes de compilar, revise o `Makefile`. Nesta versão ele executa apenas `mkdir`, NASM, GCC, `pkg-config`, linkedição e, nos alvos `run`/`clean`, execução do binário ou remoção de `build/`.

```bash
make check-deps
make
./build/sysmonitor
```

## Depuração

```bash
gdb ./build/sysmonitor
```

Para investigar ABI, confira alinhamento da pilha e preservação de RBX/RBP/R12–R15. Para dados do kernel, compare a saída com os pseudoarquivos correspondentes em `/proc` e `/sys`.
