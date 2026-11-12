TELA 80, 80, #111111;
ANIMA FPS 12;
VAR bola_x = 10;
VAR bola_y = 40;

REPETE 20 VEZES
    QUADRO
        COR_FUNDO #111111;
        CIRCULO bola_x, bola_y, 5, #FF0000;
        bola_x = bola_x + 3;
    FIM
FIM

SALVA "bounce.gif";