"""
SOM de deputados com TRÊS visualizações complementares:

1. MAPA DO SOM (grade) — a visão "de cima", onde cada célula é um neurônio.
2. DEPUTADOS COMO PONTOS sobre o mapa (com jitter) — visão individual,
   preservando a topologia do SOM.
3. PROJEÇÃO PCA — visão individual no espaço original, colorida pelos
   clusters descobertos pelo SOM.

Cada visualização responde a uma pergunta diferente:
- Mapa: "como o SOM organizou as regiões?"
- Pontos no mapa: "onde cada deputado caiu, e quem está perto de quem?"
- PCA: "como os deputados se distribuem no espaço real de voto?"
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# ============================================================
# UTILITÁRIOS
# ============================================================
def normalizar_zscore(X):
    media = X.mean(axis=0)
    desvio = X.std(axis=0) + 1e-8
    return (X - media) / desvio


# ============================================================
# DATASET (mantido igual ao anterior)
# ============================================================
def construir_dataset_real():
    perfil_partido = {
        'PT':          [ 1,  1,  1,  1,  1],
        'PL':          [ 1,  1,  1,  1, -1],
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
        'PSOL':        [ 1,  1, -1, -1, -1],
        'Novo':        [-1, -1,  1,  1, -1],
        'Missão':      [-1, -1,  1,  1, -1],
    }

    dissidentes_escala = {
        'PL': ['Bibo Nunes','Caroline De Toni','Daniel Freitas','Daniela Reinerhr',
               'Julia Zanatta','Mauricio Marcon','Nicoletti','Paulo Marinho Jr.',
               'Ricardo Guidi','Rosangela Moro','Zé Trovão'],
        'Novo': ['Adriana Ventura','Gilson Marques','Marcel van Hattem','Ricardo Salles'],
        'União': ['Fabio Schiochet','Fausto Pinato'],
        'MDB': ['Carlos Chiodini','Pezenti'],
        'PSD': ['Lucas Redecker'],
        'PP': ['Sergio Turra'],
    }

    ausentes = [
        'Adolfo Viana','Afonso Motta','Alexandre Leite','Arnaldo Jardim',
        'Cobalchini','Dilceu Sperafico','Geovania de Sá','Guilherme Derrite',
        'João Carlos Bacelar','José Priante','Luiz Philippe de Orleans e Bragança',
        'Newton Cardoso Jr','Padovani','Pedro Lupion','Roberto Monteiro Pai',
        'Sergio Souza','Tião Medeiros','Yandra Moura'
    ]

    bancadas = {
        'PT': 65, 'PL': 97, 'União': 50, 'PP': 47, 'MDB': 38,
        'PSD': 48, 'Republicanos': 43, 'Podemos': 27, 'PSDB': 18,
        'PSB': 17, 'PDT': 9, 'Solidariedade': 6, 'Avante': 5,
        'PRD': 2, 'Cidadania': 2, 'PCdoB': 11, 'PV': 6,
        'Rede': 4, 'PSOL': 12, 'Novo': 5, 'Missão': 1,
    }

    X_list, partidos_list, nomes_list = [], [], []
    for partido, n in bancadas.items():
        perfil = perfil_partido.get(partido, [1,1,1,1,-1])
        for i in range(n):
            nome = f"{partido}_{i+1:02d}"
            votos = np.array(perfil, dtype=float).copy()
            # Dissidência na Escala 6x1 só faz sentido para partidos que votaram Sim
            if partido in dissidentes_escala and nome in dissidentes_escala[partido]:
                if votos[0] == 1:
                    votos[0] = -1
            if nome in ausentes:
                votos[0] = 0
            X_list.append(votos)
            partidos_list.append(partido)
            nomes_list.append(nome)
    return np.array(X_list), np.array(partidos_list), np.array(nomes_list)


# ============================================================
# SOM
# ============================================================
class SOM:
    def __init__(self, grid_rows=8, grid_cols=8, n_features=5,
                 lr=0.5, sigma=None, n_iter=3000, seed=42):
        self.rows, self.cols = grid_rows, grid_cols
        self.lr0 = lr
        self.sigma0 = sigma if sigma else max(grid_rows, grid_cols)/2
        self.n_iter, self.seed = n_iter, seed
        r, c = np.meshgrid(np.arange(grid_rows), np.arange(grid_cols), indexing='ij')
        self.coords = np.stack([r.ravel(), c.ravel()], axis=1).astype(float)
        rng = np.random.RandomState(seed)
        self.W = rng.rand(grid_rows*grid_cols, n_features)

    def _bmu(self, x):
        return np.argmin(np.sum((self.W - x)**2, axis=1))

    def treinar(self, X):
        rng = np.random.RandomState(self.seed)
        n = X.shape[0]
        tau = self.n_iter/np.log(self.sigma0) if self.sigma0 > 1 else 1
        for t in range(self.n_iter):
            x = X[rng.randint(n)]
            lr = self.lr0*np.exp(-t/self.n_iter)
            sigma = self.sigma0*np.exp(-t/tau)
            bmu = self._bmu(x)
            dg = np.sum((self.coords - self.coords[bmu])**2, axis=1)
            h = np.exp(-dg/(2*sigma**2))
            self.W += lr * h[:, None] * (x - self.W)

    def mapear(self, X):
        return np.array([self._bmu(x) for x in X])


# ============================================================
# VISUALIZAÇÃO 1 — MAPA DO SOM (grade agregada)
# ============================================================
def plot_mapa_som(som, X, partidos):
    bmus = som.mapear(X)
    partidos_unicos = sorted(set(partidos))
    cor_map = {
        'PT':'#E30613','PL':'#003399','União':'#00A0DF','PP':'#FFA500',
        'MDB':'#008000','PSD':'#FFD700','Republicanos':'#8B0000',
        'Podemos':'#9370DB','PSDB':'#4169E1','PSB':'#FF0000','PDT':'#FF1493',
        'Solidariedade':'#20B2AA','Avante':'#DAA520','PRD':'#808080',
        'Cidadania':'#FF69B4','PCdoB':'#DC143C','PV':'#228B22',
        'Rede':'#32CD32','PSOL':'#800080','Novo':'#FF8C00','Missão':'#A0522D',
    }
    contagem = np.zeros((som.rows, som.cols, len(partidos_unicos)), dtype=int)
    idx = {p:i for i,p in enumerate(partidos_unicos)}
    for bmu, p in zip(bmus, partidos):
        r, c = int(som.coords[bmu][0]), int(som.coords[bmu][1])
        contagem[r, c, idx[p]] += 1
    major = np.argmax(contagem, axis=2)
    total = contagem.sum(axis=2)

    fig, ax = plt.subplots(figsize=(9, 8))
    for r in range(som.rows):
        for c in range(som.cols):
            if total[r,c] == 0:
                ax.add_patch(mpatches.Rectangle((c, som.rows-1-r), 1, 1,
                             facecolor='#F5F5F5', edgecolor='gray'))
                continue
            p = partidos_unicos[major[r,c]]
            cor = cor_map.get(p, '#CCCCCC')
            ax.add_patch(mpatches.Rectangle((c, som.rows-1-r), 1, 1,
                         facecolor=cor, edgecolor='black', linewidth=1.5, alpha=0.85))
            cor_txt = 'white' if p in ['PL','PT','PSOL','Republicanos','Novo'] else 'black'
            ax.text(c+0.5, som.rows-1-r+0.65, p, ha='center', va='center',
                    fontsize=7, fontweight='bold', color=cor_txt)
            ax.text(c+0.5, som.rows-1-r+0.3, f"n={total[r,c]}",
                    ha='center', va='center', fontsize=6, color=cor_txt)
    ax.set_xlim(0, som.cols); ax.set_ylim(0, som.rows)
    ax.set_xticks(np.arange(som.cols)+0.5); ax.set_yticks(np.arange(som.rows)+0.5)
    ax.set_xticklabels(range(som.cols)); ax.set_yticklabels(range(som.rows-1,-1,-1))
    ax.set_xlabel('Coluna'); ax.set_ylabel('Linha')
    ax.set_title('VISÃO 1 — Mapa do SOM (cada célula = 1 neurônio)', fontweight='bold')
    ax.set_aspect('equal')
    handles = [mpatches.Patch(color=cor_map.get(p,'#CCC'), label=p) for p in partidos_unicos]
    ax.legend(handles=handles, loc='upper left', bbox_to_anchor=(1.01,1),
              fontsize=7, title='Partido')
    plt.tight_layout(); plt.show()


# ============================================================
# VISUALIZAÇÃO 2 — DEPUTADOS COMO PONTOS sobre o mapa
# ============================================================
def plot_pontos_no_mapa(som, X, partidos, jitter=0.15, seed=0):
    """
    Cada deputado é um PONTO no mapa 2D do SOM.
    Vários deputados no mesmo neurônio recebem pequeno deslocamento (jitter)
    para ficarem visíveis individualmente.
    
    A posição do ponto = (coluna, linha) do neurônio vencedor + jitter.
    A distância entre pontos no gráfico reflete distância no mapa do SOM,
    que por sua vez reflete similaridade de voto.
    """
    rng = np.random.RandomState(seed)
    bmus = som.mapear(X)

    # Posição base = coordenada do neurônio; + jitter para separar
    pos_x = som.coords[bmus, 1] + rng.uniform(-jitter, jitter, len(bmus))
    pos_y = som.coords[bmus, 0] + rng.uniform(-jitter, jitter, len(bmus))
    # Inverte o eixo Y para combinar com o mapa (linha 0 no topo)

    partidos_unicos = sorted(set(partidos))
    cor_map = {
        'PT':'#E30613','PL':'#003399','União':'#00A0DF','PP':'#FFA500',
        'MDB':'#008000','PSD':'#FFD700','Republicanos':'#8B0000',
        'Podemos':'#9370DB','PSDB':'#4169E1','PSB':'#FF0000','PDT':'#FF1493',
        'Solidariedade':'#20B2AA','Avante':'#DAA520','PRD':'#808080',
        'Cidadania':'#FF69B4','PCdoB':'#DC143C','PV':'#228B22',
        'Rede':'#32CD32','PSOL':'#800080','Novo':'#FF8C00','Missão':'#A0522D',
    }

    fig, ax = plt.subplots(figsize=(11, 10))
    # Plota grade de fundo (linhas dos neurônios) para referência
    for i in range(som.rows + 1):
        ax.axhline(i - 0.5, color='#DDDDDD', linewidth=0.5, zorder=0)
    for j in range(som.cols + 1):
        ax.axvline(j - 0.5, color='#DDDDDD', linewidth=0.5, zorder=0)

    # Um scatter por partido, para gerar legenda
    for p in partidos_unicos:
        mask = partidos == p
        ax.scatter(pos_x[mask], som.rows - 1 - pos_y[mask],
                   c=cor_map.get(p, '#CCCCCC'), label=p,
                   s=45, alpha=0.85, edgecolors='black', linewidth=0.4, zorder=3)

    ax.set_xlim(-0.7, som.cols - 0.3)
    ax.set_ylim(-0.7, som.rows - 0.3)
    ax.set_xticks(range(som.cols)); ax.set_yticks(range(som.rows))
    ax.set_xticklabels(range(som.cols))
    ax.set_yticklabels(range(som.rows-1, -1, -1))
    ax.set_xlabel('Coluna do mapa'); ax.set_ylabel('Linha do mapa')
    ax.set_title('VISÃO 2 — Cada deputado é um ponto (posição = neurônio vencedor)',
                 fontweight='bold')
    ax.set_aspect('equal')
    ax.legend(loc='upper left', bbox_to_anchor=(1.01,1), fontsize=8,
              title='Partido', markerscale=1.2)
    plt.tight_layout(); plt.show()


# ============================================================
# VISUALIZAÇÃO 3 — DEPUTADOS no espaço original via PCA
# ============================================================
def plot_pca(X, partidos):
    """
    Projeta deputados em 2D via PCA (as duas componentes principais).
    Cada ponto = 1 deputado no espaço de voto original.
    As cores são os partidos, mas o agrupamento mostra quem vota parecido
    INDEPENDENTE de partido.
    
    PCA é só uma técnica de projeção — o agrupamento real é o dos dados,
    não do SOM. Serve para comparar com as outras visualizações.
    """
    # PCA manual: subtrai a média, faz SVD, projeta nas 2 primeiras componentes
    Xc = X - X.mean(axis=0)
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    proj = Xc @ Vt[:2].T  # (n, 2)

    partidos_unicos = sorted(set(partidos))
    cor_map = {
        'PT':'#E30613','PL':'#003399','União':'#00A0DF','PP':'#FFA500',
        'MDB':'#008000','PSD':'#FFD700','Republicanos':'#8B0000',
        'Podemos':'#9370DB','PSDB':'#4169E1','PSB':'#FF0000','PDT':'#FF1493',
        'Solidariedade':'#20B2AA','Avante':'#DAA520','PRD':'#808080',
        'Cidadania':'#FF69B4','PCdoB':'#DC143C','PV':'#228B22',
        'Rede':'#32CD32','PSOL':'#800080','Novo':'#FF8C00','Missão':'#A0522D',
    }

    fig, ax = plt.subplots(figsize=(11, 8))
    for p in partidos_unicos:
        mask = partidos == p
        ax.scatter(proj[mask, 0], proj[mask, 1],
                   c=cor_map.get(p, '#CCC'), label=p,
                   s=50, alpha=0.8, edgecolors='black', linewidth=0.4)
    variancia = (S**2) / np.sum(S**2) * 100
    ax.set_xlabel(f'Componente 1 ({variancia[0]:.1f}% da variância)')
    ax.set_ylabel(f'Componente 2 ({variancia[1]:.1f}% da variância)')
    ax.set_title('VISÃO 3 — Deputados no espaço original (PCA)\n'
                 'Cada ponto = 1 deputado. Proximidade = voto parecido.',
                 fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left', bbox_to_anchor=(1.01,1), fontsize=8,
              title='Partido', markerscale=1.2)
    plt.tight_layout(); plt.show()


# ============================================================
# DEMO
# ============================================================
def demo():
    print("=== SOM de Deputados — 3 visualizações ===\n")
    X, partidos, nomes = construir_dataset_real()
    print(f"Deputados: {X.shape[0]}, Votações: {X.shape[1]}\n")
    X_norm = normalizar_zscore(X)

    som = SOM(grid_rows=8, grid_cols=8, n_features=5, n_iter=3000, seed=42)
    print("Treinando SOM 8×8 (3000 iterações)...")
    som.treinar(X_norm)
    print("Pronto.\n")

    print("Gerando VISÃO 1: mapa do SOM (grade agregada)...")
    plot_mapa_som(som, X_norm, partidos)

    print("Gerando VISÃO 2: cada deputado como ponto sobre o mapa...")
    plot_pontos_no_mapa(som, X_norm, partidos, jitter=0.15)

    print("Gerando VISÃO 3: deputados no espaço original (PCA)...")
    plot_pca(X_norm, partidos)

    print("\nQual usar na apresentação?")
    print("- Visão 1 mostra a organização topológica (conceito do SOM).")
    print("- Visão 2 mostra cada deputado individualmente, mantendo a topologia.")
    print("- Visão 3 mostra os dados reais, permitindo ver quem se agrupa")
    print("  sem a intermediação do SOM.")


if __name__ == "__main__":
    demo()