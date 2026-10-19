
#!/bin/bash

set -e

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate

pip install -r ../requirements.txt

echo ">>> Mínimos Quadrados"
python ../src/minimos_quadrados/minimos_quadrados.py

echo ">>> SOM"
python ../src/som/som.py

echo ">>> Perceptron"
python ../src/perceptron/perceptron.py

echo ">>> Adaline/LMS"
python ../src/adaline_LMS/adaline_lms.py

echo ">>> MLP"
python ../src/multi_layer/mlp.py

echo ">>> Comparativo Final"
echo "Todos os demos rodaram sem erros."
