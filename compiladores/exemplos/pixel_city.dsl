// ============================================================
//  PIXEL CITY AO ENTARDECER  —  1200 x 1200
//  Demonstra TODAS as primitivas da DSL:
//    TELA, PIXEL, LINHA, RETANGULO, CIRCULO, TEXTO,
//    COR_FUNDO, VAR, ATRIBUICAO, SE, SENAO, REPETE,
//    ANIMA, MOVE, QUADRO, SALVA
// ============================================================

// ---------- Configuração da tela ----------
TELA 1200, 1200, #1A1A2E;
COR_FUNDO #1A1A2E;

// ---------- Céu em gradiente (faixas horizontais) ----------
// De roxo-escuro no topo a laranja no horizonte
VAR y = 0;
VAR r = 26;
VAR g = 26;
VAR b = 46;
REPETE 60 VEZES
    LINHA 0, y, 1199, y, #000000;
    y = y + 20;
FIM

// ---------- Sol no horizonte ----------
VAR sol_x = 600;
VAR sol_y = 720;
VAR sol_r = 90;

// Halo externo (3 círculos concêntricos)
CIRCULO sol_x, sol_y, sol_r + 40, #FFD54F;
CIRCULO sol_x, sol_y, sol_r + 20, #FFB74D;
CIRCULO sol_x, sol_y, sol_r,      #FF8A65;

// Raios do sol (usando REPETE + LINHA)
VAR ang = 0;
VAR i = 0;
REPETE 12 VEZES
    // Aproximação de raio: usa deslocamento fixo
    LINHA sol_x, sol_y,
          sol_x + 200, sol_y - 200 + (i * 35),
          #FFB74D;
    i = i + 1;
FIM

// ---------- Montanhas ao fundo ----------
// Montanha 1
LINHA 0, 800, 150, 620, #2D1B4E;
LINHA 150, 620, 320, 800, #2D1B4E;
LINHA 0, 800, 320, 800, #2D1B4E;

// Montanha 2
LINHA 280, 820, 480, 580, #3D2B5E;
LINHA 480, 580, 700, 820, #3D2B5E;
LINHA 280, 820, 700, 820, #3D2B5E;

// Montanha 3
LINHA 650, 810, 850, 560, #2D1B4E;
LINHA 850, 560, 1080, 810, #2D1B4E;
LINHA 650, 810, 1080, 810, #2D1B4E;

// Montanha 4
LINHA 1000, 830, 1200, 640, #3D2B5E;
LINHA 1200, 640, 1200, 830, #3D2B5E;

// ---------- Chão ----------
RETANGULO 0, 820, 1200, 380, #1E3A2F;
RETANGULO 0, 860, 1200, 340, #16302A;

// ---------- Estrelas no céu ----------
// Estrelas fixas (PIXEL)
PIXEL 120, 80,  #FFFFFF;
PIXEL 250, 40,  #FFFFFF;
PIXEL 380, 120, #FFFFFF;
PIXEL 520, 60,  #FFFFFF;
PIXEL 680, 30,  #FFFFFF;
PIXEL 780, 100, #FFFFFF;
PIXEL 900, 50,  #FFFFFF;
PIXEL 1050, 90, #FFFFFF;
PIXEL 1150, 40, #FFFFFF;
PIXEL 80,  200, #FFFFFF;
PIXEL 300, 220, #FFFFFF;
PIXEL 450, 180, #FFFFFF;
PIXEL 620, 250, #FFFFFF;
PIXEL 820, 200, #FFFFFF;
PIXEL 980, 230, #FFFFFF;
PIXEL 1120, 180, #FFFFFF;

// Estrelas em loop (padrão)
VAR sx = 50;
VAR sy = 300;
REPETE 20 VEZES
    PIXEL sx, sy, #E0E0FF;
    PIXEL sx + 5, sy + 3, #FFFFFF;
    PIXEL sx - 3, sy + 5, #C0C0FF;
    sx = sx + 60;
    sy = sy + 15;
FIM

// ---------- Prédios (primeira fileira — mais distantes) ----------
// Prédio 1
RETANGULO 40, 620, 100, 200, #2E2E4E;
RETANGULO 40, 620, 100, 10,  #4E4E6E;
// Janelas do prédio 1
VAR wx = 55;
VAR wy = 640;
REPETE 4 VEZES
    REPETE 3 VEZES
        RETANGULO wx, wy, 12, 18, #FFD54F;
        wx = wx + 25;
    FIM
    wx = 55;
    wy = wy + 35;
FIM

// Prédio 2
RETANGULO 160, 580, 120, 240, #3E2E5E;
RETANGULO 160, 580, 120, 10,  #5E4E7E;
// Janelas do prédio 2
VAR wx2 = 175;
VAR wy2 = 600;
REPETE 5 VEZES
    REPETE 4 VEZES
        RETANGULO wx2, wy2, 14, 20, #FFE082;
        wx2 = wx2 + 26;
    FIM
    wx2 = 175;
    wy2 = wy2 + 42;
FIM

// Prédio 3 — mais alto
RETANGULO 300, 500, 110, 320, #2E2E5E;
RETANGULO 300, 500, 110, 10,  #4E4E7E;
// Janelas
VAR wx3 = 315;
VAR wy3 = 520;
REPETE 6 VEZES
    REPETE 3 VEZES
        RETANGULO wx3, wy3, 16, 22, #FFCC80;
        wx3 = wx3 + 28;
    FIM
    wx3 = 315;
    wy3 = wy3 + 48;
FIM

// Prédio 4
RETANGULO 430, 650, 90, 170, #3E2E4E;
RETANGULO 430, 650, 90, 8,   #5E4E6E;
VAR wx4 = 445;
VAR wy4 = 670;
REPETE 3 VEZES
    REPETE 3 VEZES
        RETANGULO wx4, wy4, 12, 16, #FFD54F;
        wx4 = wx4 + 22;
    FIM
    wx4 = 445;
    wy4 = wy4 + 40;
FIM

// Prédio 5
RETANGULO 540, 590, 100, 230, #2E3E5E;
RETANGULO 540, 590, 100, 8,   #4E5E7E;
VAR wx5 = 555;
VAR wy5 = 610;
REPETE 5 VEZES
    REPETE 3 VEZES
        RETANGULO wx5, wy5, 14, 20, #FFE082;
        wx5 = wx5 + 24;
    FIM
    wx5 = 555;
    wy5 = wy5 + 42;
FIM

// Prédio 6 — destaque
RETANGULO 660, 470, 130, 350, #3E2E6E;
RETANGULO 660, 470, 130, 12,  #5E4E8E;
VAR wx6 = 675;
VAR wy6 = 490;
REPETE 7 VEZES
    REPETE 4 VEZES
        RETANGULO wx6, wy6, 16, 22, #FFCC80;
        wx6 = wx6 + 28;
    FIM
    wx6 = 675;
    wy6 = wy6 + 46;
FIM

// Prédio 7
RETANGULO 810, 620, 100, 200, #2E2E4E;
RETANGULO 810, 620, 100, 10,  #4E4E6E;
VAR wx7 = 825;
VAR wy7 = 640;
REPETE 4 VEZES
    REPETE 3 VEZES
        RETANGULO wx7, wy7, 14, 18, #FFD54F;
        wx7 = wx7 + 26;
    FIM
    wx7 = 825;
    wy7 = wy7 + 38;
FIM

// Prédio 8 — torre
RETANGULO 930, 450, 120, 370, #2E3E5E;
RETANGULO 930, 450, 120, 10,  #4E5E7E;
RETANGULO 955, 420, 70, 30,   #3E4E6E;   // topo
VAR wx8 = 945;
VAR wy8 = 470;
REPETE 8 VEZES
    REPETE 3 VEZES
        RETANGULO wx8, wy8, 14, 20, #FFE082;
        wx8 = wx8 + 30;
    FIM
    wx8 = 945;
    wy8 = wy8 + 44;
FIM

// Prédio 9
RETANGULO 1070, 600, 90, 220, #3E2E5E;
RETANGULO 1070, 600, 90, 10,  #5E4E7E;
VAR wx9 = 1085;
VAR wy9 = 620;
REPETE 5 VEZES
    REPETE 3 VEZES
        RETANGULO wx9, wy9, 12, 18, #FFD54F;
        wx9 = wx9 + 22;
    FIM
    wx9 = 1085;
    wy9 = wy9 + 40;
FIM

// ---------- Segunda fileira de prédios (frente, mais escuros) ----------
RETANGULO 0, 780, 140, 80,   #1E1E3E;
RETANGULO 220, 760, 130, 100, #1E1E3E;
RETANGULO 420, 790, 160, 70,  #1E1E3E;
RETANGULO 640, 770, 140, 90,  #1E1E3E;
RETANGULO 850, 780, 150, 80,  #1E1E3E;
RETANGULO 1050, 760, 150, 100, #1E1E3E;

// Janelas da segunda fileira (pequenas, acesas)
VAR fx = 20;
REPETE 5 VEZES
    RETANGULO fx, 800, 10, 12, #FFD54F;
    RETANGULO fx + 25, 800, 10, 12, #FFE082;
    RETANGULO fx + 50, 800, 10, 12, #FFD54F;
    fx = fx + 90;
FIM

VAR fx2 = 240;
REPETE 5 VEZES
    RETANGULO fx2, 790, 10, 12, #FFE082;
    RETANGULO fx2 + 25, 790, 10, 12, #FFD54F;
    RETANGULO fx2 + 50, 790, 10, 12, #FFE082;
    fx2 = fx2 + 80;
FIM

// ---------- Árvores no chão ----------
// Árvore 1
RETANGULO 150, 940, 12, 60, #3E2A1E;
CIRCULO 156, 920, 45, #2E7D32;
CIRCULO 130, 930, 35, #388E3C;
CIRCULO 180, 930, 35, #388E3C;
CIRCULO 156, 905, 30, #43A047;

// Árvore 2
RETANGULO 380, 950, 12, 50, #3E2A1E;
CIRCULO 386, 930, 40, #2E7D32;
CIRCULO 360, 940, 32, #388E3C;
CIRCULO 410, 940, 32, #388E3C;
CIRCULO 386, 915, 28, #43A047;

// Árvore 3
RETANGULO 780, 945, 12, 55, #3E2A1E;
CIRCULO 786, 925, 42, #2E7D32;
CIRCULO 760, 935, 34, #388E3C;
CIRCULO 812, 935, 34, #388E3C;
CIRCULO 786, 910, 30, #43A047;

// Árvore 4
RETANGULO 1050, 950, 12, 50, #3E2A1E;
CIRCULO 1056, 930, 40, #2E7D32;
CIRCULO 1030, 940, 32, #388E3C;
CIRCULO 1082, 940, 32, #388E3C;
CIRCULO 1056, 915, 28, #43A047;

// ---------- Postes de luz ----------
// Poste 1
RETANGULO 250, 850, 6, 120, #1A1A1A;
RETANGULO 240, 850, 26, 8,  #1A1A1A;
CIRCULO 253, 845, 12, #FFEB3B;

// Poste 2
RETANGULO 550, 850, 6, 120, #1A1A1A;
RETANGULO 540, 850, 26, 8,  #1A1A1A;
CIRCULO 553, 845, 12, #FFEB3B;

// Poste 3
RETANGULO 850, 850, 6, 120, #1A1A1A;
RETANGULO 840, 850, 26, 8,  #1A1A1A;
CIRCULO 853, 845, 12, #FFEB3B;

// Poste 4
RETANGULO 1150, 850, 6, 120, #1A1A1A;
RETANGULO 1140, 850, 26, 8, #1A1A1A;
CIRCULO 1153, 845, 12, #FFEB3B;

// ---------- Estrada / calçada ----------
RETANGULO 0, 1000, 1200, 200, #1A1A1A;
// Faixas da estrada
VAR estrada_x = 0;
REPETE 20 VEZES
    RETANGULO estrada_x, 1095, 40, 10, #FFEB3B;
    estrada_x = estrada_x + 60;
FIM

// ---------- Lua no canto superior ----------
CIRCULO 1000, 150, 50, #E8E8D0;
CIRCULO 1025, 140, 45, #1A1A2E;   // "mordida" para simular crescente

// ---------- Estrelas cadentes (LINHA + PIXEL) ----------
LINHA 300, 150, 340, 200, #FFFFFF;
PIXEL 340, 200, #FFFFFF;
PIXEL 345, 205, #E0E0FF;

LINHA 700, 100, 730, 140, #FFFFFF;
PIXEL 730, 140, #FFFFFF;
PIXEL 735, 145, #E0E0FF;

// ---------- Pássaros (V com LINHA) ----------
LINHA 400, 300, 420, 290, #000000;
LINHA 420, 290, 440, 300, #000000;

LINHA 500, 350, 515, 342, #000000;
LINHA 515, 342, 530, 350, #000000;

LINHA 620, 280, 635, 272, #000000;
LINHA 635, 272, 650, 280, #000000;

// ---------- Texto (assinatura) ----------
TEXTO "PIXEL CITY" EM 500, 1150, #FFD54F;
TEXTO "2024" EM 580, 1175, #FFE082;

// ---------- Animação: definir FPS ----------
ANIMA FPS 30;

// ---------- Quadro de animação (futuro GIF) ----------
QUADRO
    // Neste quadro, pisca uma janela específica
    RETANGULO 700, 500, 16, 22, #FFFFFF;
    RETANGULO 700, 500, 16, 22, #FFCC80;
FIM

// ---------- MOVE: mover o sol (exemplo de animação) ----------
// (Na versão atual, MOVE só atualiza X — limitação documentada)
VAR sol_pos = 600;
MOVE sol_pos PARA (620, 720) EM 2 SEGUNDOS;

// ---------- Salvar ----------
SALVA "pixel_city.png";