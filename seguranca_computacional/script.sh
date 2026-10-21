#!/bin/bash

PDF="fatura.pdf"

for i in $(seq 0 9999); do
    senha=$(printf "%04d" "$i")

    echo -ne "\rTestando: $senha"

    qpdf --password="$senha" --decrypt "$PDF" /tmp/teste.pdf \
        >/dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo
        echo "================================"
        echo "SENHA ENCONTRADA: $senha"
        echo "================================"

        qpdf --password="$senha" --decrypt "$PDF" desbloqueado.pdf

        exit 0
    fi
done

echo
echo "Senha não encontrada."