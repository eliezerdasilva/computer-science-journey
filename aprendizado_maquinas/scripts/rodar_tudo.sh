#!/bin/bash
# Roda todos os demos em sequência. Útil antes de apresentar.
set -e
source .venv/bin/activate
echo ">>> Mínimos Quadrados"
python src/minimos_quadrados/minimos_quadrados.py
echo ">>> SOM"
python src/som/som.py
echo ">>> Perceptron"
python src/perceptron/perceptron.py
echo ">>> Adaline/LMS"
python src/adaline_LMS/adaline_lms.py
echo ">>> MLP"
python src/multi_layer/mlp.py
echo ">>> Comparativo Final"
echo "✅ Todos os demos rodaram sem erro."