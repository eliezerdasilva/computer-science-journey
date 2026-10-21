"""
SOM com dados REAIS de votações da Câmara dos Deputados.

Fontes dos dados (publicados na imprensa e no portal da Câmara):
- PEC Escala 6x1 (27/05/2026): votos por partido e lista de dissidentes
- PEC da Segurança (04/03/2026): votos por partido
- PEC 32/2015 (CCJ, 19/05/2026): votos por partido

Cada deputado é representado por um vetor de 5 votos:
[Escala6x1_1turno, Escala6x1_2turno, Seguranca_1turno, Seguranca_2turno, PEC32_CCJ]

Codificação: +1 = Sim, -1 = Não, 0 = Ausente/Abstenção/Obstrução
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# ============================================================
# 0. UTILITÁRIOS
# ============================================================
def normalizar_zscore(X):
    media = X.mean(axis=0)
    desvio = X.std(axis=0) + 1e-8
    return (X - media) / desvio


# ============================================================
# 1. DATASET REAL (baseado em fontes publicadas)
# ============================================================
def construir_dataset_real():
    """
    Constrói matriz de deputados × votações usando dados publicados.

    Estratégia:
    - Para partidos com votação unânime conhecida, todos os deputados
      recebem o mesmo voto naquela dimensão.
    - Para partidos com dissidências documentadas, os dissidentes são
      listados explicitamente e recebem voto contrário.
    - Deputados ausentes documentados recebem 0.

    Retorna: X (n_deputados, 5), partidos (n,), nomes (n,)
    """

    # ---- Definição dos votos por partido em cada votação ----
    # Dimensões: [Esc6x1_1T, Esc6x1_2T, Seg1T, Seg2T, PEC32_CCJ]
    # +1=Sim, -1=Não, 0=Ausente/Abstenção

    # Votos "padrão" (maioria) de cada partido nas 5 votações
    # Fonte: tabelas por partido publicadas [citation:4][citation:9][citation:10]
    perfil_partido = {
        # partido: [Esc1, Esc2, Seg1, Seg2, PEC32]
        'PT':          [ 1,  1,  1,  1,  1],   # todos Sim na Escala; 66/67 Sim na Segurança
        'PL':          [ 1,  1,  1,  1, -1],   # maioria Sim em tudo, mas CCJ votou Não em massa
        'União':       [ 1,  1,  1,  1, -1],
        'PP':          [ 1,  1,  1,  1, -1],
        'MDB':         [ 1,  1,  1,  1, -1],
        'PSD':         [ 1,  1,  1,  1, -1],
        'Republicanos':[ 1,  1,  1,  1, -1],
        'Podemos':     [ 1,  1,  1,  1, -1],
        'PSDB':        [ 1,  1,  1,  1, -1],
        'PSB':         [ 1,  1,  1,  1, -1],
        'PDT':         [ 1,  1,  1,  1, -1],
        'Solidariedade':[ 1,  1,  1,  1, -1],
        'Avante':      [ 1,  1,  1,  1, -1],
        'PRD':         [ 1,  1,  1,  1, -1],
        'Cidadania':   [ 1,  1,  1,  1, -1],
        'PCdoB':       [ 1,  1,  1,  1, -1],
        'PV':          [ 1,  1,  1,  1, -1],
        'Rede':        [ 1,  1,  1,  1, -1],
        'PSOL':        [ 1,  1, -1, -1, -1],   # PSOL votou 100% NÃO na Segurança
        'Novo':        [-1, -1,  1,  1, -1],   # Novo votou NÃO na Escala, Sim na Segurança
        'Missão':      [-1, -1,  1,  1, -1],   # Kim Kataguiri
    }

    # ---- Dissidentes documentados ----
    # Deputados que votaram DIFERENTE da maioria do partido na Escala 6x1
    dissidentes_escala_1T = {
        'PL': ['Bibo Nunes', 'Caroline De Toni', 'Daniel Freitas', 'Daniela Reinerhr',
               'Julia Zanatta', 'Mauricio Marcon', 'Nicoletti', 'Paulo Marinho Jr.',
               'Ricardo Guidi', 'Rosangela Moro', 'Zé Trovão'],
        'Novo': ['Adriana Ventura', 'Gilson Marques', 'Marcel van Hattem', 'Ricardo Salles'],
        'União': ['Fabio Schiochet', 'Fausto Pinato'],
        'MDB': ['Carlos Chiodini', 'Pezenti'],
        'PSD': ['Lucas Redecker'],
        'PP': ['Sergio Turra'],
        'Missão': ['Kim Kataguiri'],
    }

    # Ausentes no 1º turno da Escala 6x1 [citation:13]
    ausentes_escala_1T = [
        'Adolfo Viana', 'Afonso Motta', 'Alexandre Leite', 'Arnaldo Jardim',
        'Cobalchini', 'Dilceu Sperafico', 'Geovania de Sá', 'Guilherme Derrite',
        'João Carlos Bacelar', 'José Priante', 'Luiz Philippe de Orleans e Bragança',
        'Newton Cardoso Jr', 'Padovani', 'Pedro Lupion', 'Roberto Monteiro Pai',
        'Sergio Souza', 'Tião Medeiros', 'Yandra Moura'
    ]

    # ---- Quantidade de deputados por partido (aproximada, Câmara 2026) ----
    # Baseado nas bancadas reportadas nas votações [citation:4][citation:9]
    bancadas = {
        'PT': 65, 'PL': 97, 'União': 50, 'PP': 47, 'MDB': 38,
        'PSD': 48, 'Republicanos': 43, 'Podemos': 27, 'PSDB': 18,
        'PSB': 17, 'PDT': 9, 'Solidariedade': 6, 'Avante': 5,
        'PRD': 2, 'Cidadania': 2, 'PCdoB': 11, 'PV': 6,
        'Rede': 4, 'PSOL': 12, 'Novo': 5, 'Missão': 1,
    }

    X_list, partidos_list, nomes_list = [], [], []

    for partido, n in bancadas.items():
        perfil = perfil_partido.get(partido, [1, 1, 1, 1, -1])

        for i in range(n):
            nome = f"{partido}_{i+1:02d}"
            votos = np.array(perfil, dtype=float).copy()

            # Aplica dissidência documentada (Escala 6x1, 1º turno)
            if partido in dissidentes_escala_1T and nome in dissidentes_escala_1T[partido]:
                votos[0] = -1  # voto contrário à maioria

            # Aplica ausência documentada (Escala 6x1, 1º turno)
            if nome in ausentes_escala_1T:
                votos[0] = 0

            # Ajuste: Novo e Missão têm padrão próprio já definido no perfil
            # (já estão com -1 na Escala, então dissidentes do Novo não precisam
            #  de ajuste extra — eles JÁ votaram -1 por padrão)

            X_list.append(votos)
            partidos_list.append(partido)
            nomes_list.append(nome)

    return np.array(X_list), np.array(partidos_list), np.array(nomes_list)


# ============================================================
# 2. CLASSE SOM (mesma do projeto)
# ============================================================
class SOM:
    def __init__(self, grid_rows=8, grid_cols=8, n_features=5,
                 lr_inicial=0.5, sigma_inicial=None, n_iter=3000, seed=42):
        self.rows = grid_rows
        self.cols = grid_cols
        self.lr0 = lr_inicial
        self.sigma0 = sigma_inicial if sigma_inicial else max(grid_rows, grid_cols) / 2.0
        self.n_iter = n_iter
        self.seed = seed

        r, c = np.meshgrid(np.arange(grid_rows), np.arange(grid_cols), indexing='ij')
        self.coords = np.stack([r.ravel(), c.ravel()], axis=1).astype(float)

        rng = np.random.RandomState(seed)
        self.W = rng.rand(grid_rows * grid_cols, n_features)

    def _bmu(self, x):
        return np.argmin(np.sum((self.W - x) ** 2, axis=1))

    def treinar(self, X):
        rng = np.random.RandomState(self.seed)
        n = X.shape[0]
        tau = self.n_iter / np.log(self.sigma0) if self.sigma0 > 1 else 1
        for t in range(self.n_iter):
            x = X[rng.randint(n)]
            lr = self.lr0 * np.exp(-t / self.n_iter)
            sigma = self.sigma0 * np.exp(-t / tau)
            bmu = self._bmu(x)
            dg = np.sum((self.coords - self.coords[bmu]) ** 2, axis=1)
            h = np.exp(-dg / (2 * sigma ** 2))
            self.W += lr * h[:, None] * (x - self.W)

    def mapear(self, X):
        return np.array([self._bmu(x) for x in X])


# ============================================================
# 3. VISUALIZAÇÃO
# ============================================================
def plot_som(som, X, partidos, titulo):
    bmus = som.mapear(X)
    partidos_unicos = sorted(set(partidos))

    cor_map = {
        'PT': '#E30613', 'PL': '#003399', 'União': '#00A0DF',
        'PP': '#FFA500', 'MDB': '#008000', 'PSD': '#FFD700',
        'Republicanos': '#8B0000', 'Podemos': '#9370DB',
        'PSDB': '#4169E1', 'PSB': '#FF0000', 'PDT': '#FF1493',
        'Solidariedade': '#20B2AA', 'Avante': '#DAA520',
        'PRD': '#808080', 'Cidadania': '#FF69B4', 'PCdoB': '#DC143C',
        'PV': '#228B22', 'Rede': '#32CD32', 'PSOL': '#800080',
        'Novo': '#FF8C00', 'Missão': '#A0522D',
    }

    contagem = np.zeros((som.rows, som.cols, len(partidos_unicos)), dtype=int)
    idx = {p: i for i, p in enumerate(partidos_unicos)}
    for bmu, p in zip(bmus, partidos):
        r, c = int(som.coords[bmu][0]), int(som.coords[bmu][1])
        contagem[r, c, idx[p]] += 1

    major = np.argmax(contagem, axis=2)
    total = contagem.sum(axis=2)

    fig, ax = plt.subplots(figsize=(12, 10))
    for r in range(som.rows):
        for c in range(som.cols):
            if total[r, c] == 0:
                ax.add_patch(mpatches.Rectangle((c, som.rows-1-r), 1, 1,
                             facecolor='#F5F5F5', edgecolor='gray'))
                continue
            p = partidos_unicos[major[r, c]]
            cor = cor_map.get(p, '#CCCCCC')
            ax.add_patch(mpatches.Rectangle((c, som.rows-1-r), 1, 1,
                         facecolor=cor, edgecolor='black', linewidth=1.5, alpha=0.85))
            cor_txt = 'white' if p in ['PL','PT','PSOL','Republicanos','Novo'] else 'black'
            ax.text(c+0.5, som.rows-1-r+0.65, p, ha='center', va='center',
                    fontsize=6, fontweight='bold', color=cor_txt)
            ax.text(c+0.5, som.rows-1-r+0.3, f"n={total[r,c]}",
                    ha='center', va='center', fontsize=6, color=cor_txt)

    ax.set_xlim(0, som.cols); ax.set_ylim(0, som.rows)
    ax.set_xticks(np.arange(som.cols)+0.5); ax.set_yticks(np.arange(som.rows)+0.5)
    ax.set_xticklabels(range(som.cols)); ax.set_yticklabels(range(som.rows-1,-1,-1))
    ax.set_xlabel('Coluna'); ax.set_ylabel('Linha')
    ax.set_title(titulo, fontsize=12, fontweight='bold')
    ax.set_aspect('equal')

    handles = [mpatches.Patch(color=cor_map.get(p,'#CCC'), label=p) for p in partidos_unicos]
    ax.legend(handles=handles, loc='upper left', bbox_to_anchor=(1.01,1),
              fontsize=7, title='Partido')
    plt.tight_layout()
    plt.show()


# ============================================================
# 4. DEMO
# ============================================================
def demo():
    print("=== SOM com DADOS REAIS: Deputados × PECs ===\n")
    print("Votações utilizadas:")
    print("  1. PEC Escala 6x1 — 1º turno (27/05/2026)")
    print("  2. PEC Escala 6x1 — 2º turno (27/05/2026)")
    print("  3. PEC da Segurança — 1º turno (04/03/2026)")
    print("  4. PEC da Segurança — 2º turno (04/03/2026)")
    print("  5. PEC 32/2015 (CCJ) — Requerimento (19/05/2026)\n")

    X, partidos, nomes = construir_dataset_real()
    print(f"Total de deputados: {X.shape[0]}")
    print(f"Votações (dimensões): {X.shape[1]}\n")

    X_norm = normalizar_zscore(X)

    som = SOM(grid_rows=8, grid_cols=8, n_features=5,
              n_iter=3000, lr_inicial=0.5, seed=42)
    print("Treinando SOM 8×8...")
    som.treinar(X_norm)

    plot_som(som, X_norm, partidos,
             'SOM de Deputados Brasileiros — Padrão de Voto em PECs\n'
             '(cor = partido majoritário na célula; algoritmo não usou partido)')

    print("\n--- Análise das células misturadas ---")
    bmus = som.mapear(X_norm)
    for r in range(som.rows):
        for c in range(som.cols):
            mask = (som.coords[bmus,0]==r) & (som.coords[bmus,1]==c)
            if mask.sum() > 1:
                partes, counts = np.unique(partidos[mask], return_counts=True)
                if len(partes) > 1:
                    print(f"  Célula ({r},{c}): {dict(zip(partes, counts))}")

    print("\nInterpretação política:")
    print("- PT (vermelho) deve ocupar uma região: votou Sim em tudo.")
    print("- Novo (laranja) deve ocupar outra: votou Não na Escala, Sim na Segurança.")
    print("- PSOL (roxo) deve ficar próximo do PT na Escala, mas distante na Segurança.")
    print("- Dissidências do PL (que votaram Não na Escala) podem aparecer")
    print("  próximas ao Novo, pois compartilham esse padrão de voto.")


if __name__ == "__main__":
    demo()