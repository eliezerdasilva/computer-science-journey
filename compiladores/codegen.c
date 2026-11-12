/* codegen.c */
#include "codegen.h"
#include <gd.h>
#include <gdfonts.h>
#include <gif_lib.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_FRAMES 256

typedef struct { char *nome; double valor; } Variavel;
static Variavel vars[128];
static int nvars = 0;
static double var_get(const char *n) {
    for (int i = 0; i < nvars; i++) if (strcmp(vars[i].nome, n) == 0) return vars[i].valor;
    return 0;
}
static void var_set(const char *n, double v) {
    for (int i = 0; i < nvars; i++) if (strcmp(vars[i].nome, n) == 0) { vars[i].valor = v; return; }
    if (nvars < 128) { vars[nvars].nome = strdup(n); vars[nvars].valor = v; nvars++; }
}

/* Estado do canvas */
static gdImagePtr canvas = NULL;
static int largura = 0, altura = 0;
static int fps = 10;
static char *arquivo_saida = NULL;
static int cor_bg = 0;
static int **frames_rgb = NULL;   /* frames acumulados como RGB888 */
static int nframes = 0;

static int hex_para_int(const char *hex) {
    int r, g, b;
    sscanf(hex, "#%02x%02x%02x", &r, &g, &b);
    return (r << 16) | (g << 8) | b;
}
static int cor_para_gd(int rgb) {
    int r = (rgb >> 16) & 0xff, g = (rgb >> 8) & 0xff, b = rgb & 0xff;
    return gdImageColorAllocate(canvas, r, g, b);
}

static double eval(AstNode *n) {
    if (!n) return 0;
    switch (n->tipo) {
        case AST_NUM: return n->u.num;
        case AST_IDENT: return var_get(n->u.ident);
        case AST_BINOP: {
            double a = eval(n->u.binop.esq), b = eval(n->u.binop.dir);
            switch (n->u.binop.op) {
                case OP_ADD: return a + b;
                case OP_SUB: return a - b;
                case OP_MUL: return a * b;
                case OP_DIV: return (b != 0) ? a / b : 0;
                case OP_MOD: return (b != 0) ? fmod(a, b) : 0;
                case OP_EQ: return a == b;
                case OP_NE: return a != b;
                case OP_LT: return a < b;
                case OP_GT: return a > b;
                case OP_LE: return a <= b;
                case OP_GE: return a >= b;
                case OP_AND: return a && b;
                case OP_OR: return a || b;
                default: return 0;
            }
        }
        case AST_UNOP:
            if (n->u.unop.op == OP_NOT) return !eval(n->u.unop.operando);
            return -eval(n->u.unop.operando);
        default: return 0;
    }
}

static void captura_frame(void) {
    if (!canvas) return;
    int w = gdImageSX(canvas), h = gdImageSY(canvas);
    int *buf = malloc(w * h * sizeof(int));
    if (!buf) return;
    for (int y = 0; y < h; y++)
        for (int x = 0; x < w; x++) {
            int c = gdImageGetPixel(canvas, x, y);
            int r = gdImageRed(canvas, c);
            int g = gdImageGreen(canvas, c);
            int b = gdImageBlue(canvas, c);
            buf[y*w + x] = (r << 16) | (g << 8) | b;
        }
    if (nframes < MAX_FRAMES) {
        if (!frames_rgb) frames_rgb = malloc(MAX_FRAMES * sizeof(int*));
        frames_rgb[nframes++] = buf;   /* atribuição direta, sem cast */
    } else {
        free(buf);
    }
}

static int salva_png(const char *arq) {
    FILE *f = fopen(arq, "wb");
    if (!f) return 0;
    gdImagePng(canvas, f);
    fclose(f);
    return 1;
}

/* Escrita de GIF animado usando giflib */
static int salva_gif(const char *arq) {
    int error = 0;
    GifFileType *gif = EGifOpenFileName(arq, false, &error);
    if (!gif) return 0;
    int w = largura, h = altura;
    ColorMapObject *cmap = GifMakeMapObject(256, NULL);
    if (!cmap) { EGifCloseFile(gif, &error); return 0; }
    for (int i = 0; i < 256; i++) { cmap->Colors[i].Red = i; cmap->Colors[i].Green = i; cmap->Colors[i].Blue = i; }
    EGifPutScreenDesc(gif, w, h, 8, 0, cmap);
    EGifPutImageDesc(gif, 0, 0, w, h, false, NULL);
    /* Para simplificar, salvamos apenas o primeiro frame como GIF estático */
    if (nframes > 0) {
        GifByteType *linha = malloc(w);
        for (int y = 0; y < h; y++) {
            for (int x = 0; x < w; x++) {
                int rgb = frames_rgb[0][y*w + x];
                int r = (rgb >> 16) & 0xff, g = (rgb >> 8) & 0xff, b = rgb & 0xff;
                linha[x] = (GifPixelType)((r + g + b) / 3);
            }
            EGifPutLine(gif, linha, w);
        }
        free(linha);
    }
    EGifCloseFile(gif, &error);
    GifFreeMapObject(cmap);
    return 1;
}

static void executa_no(AstNode *n) {
    if (!n) return;
    switch (n->tipo) {
        case AST_PROGRAMA:
            for (int i = 0; i < n->u.programa.n; i++) executa_no(n->u.programa.itens[i]);
            break;
        case AST_BLOCO:
            for (int i = 0; i < n->u.bloco.n; i++) executa_no(n->u.bloco.itens[i]);
            break;
        case AST_TELA: {
            largura = (int)eval(n->u.tela.w);
            altura = (int)eval(n->u.tela.h);
            cor_bg = hex_para_int(n->u.tela.cor->u.cor);
            if (canvas) gdImageDestroy(canvas);
            canvas = gdImageCreateTrueColor(largura, altura);
            int bg = gdImageColorAllocate(canvas, (cor_bg>>16)&0xff, (cor_bg>>8)&0xff, cor_bg&0xff);
            gdImageFilledRectangle(canvas, 0, 0, largura-1, altura-1, bg);
            break;
        }
        case AST_PIXEL: {
            int x = (int)eval(n->u.pixel.x), y = (int)eval(n->u.pixel.y);
            int c = cor_para_gd(hex_para_int(n->u.pixel.cor->u.cor));
            gdImageSetPixel(canvas, x, y, c);
            break;
        }
        case AST_LINHA: {
            int x1 = (int)eval(n->u.linha.x1), y1 = (int)eval(n->u.linha.y1);
            int x2 = (int)eval(n->u.linha.x2), y2 = (int)eval(n->u.linha.y2);
            int c = cor_para_gd(hex_para_int(n->u.linha.cor->u.cor));
            gdImageLine(canvas, x1, y1, x2, y2, c);
            break;
        }
        case AST_RETANGULO: {
            int x = (int)eval(n->u.retangulo.x), y = (int)eval(n->u.retangulo.y);
            int w = (int)eval(n->u.retangulo.w), h = (int)eval(n->u.retangulo.h);
            int c = cor_para_gd(hex_para_int(n->u.retangulo.cor->u.cor));
            gdImageFilledRectangle(canvas, x, y, x+w, y+h, c);
            break;
        }
        case AST_CIRCULO: {
            int cx = (int)eval(n->u.circulo.cx), cy = (int)eval(n->u.circulo.cy);
            int r = (int)eval(n->u.circulo.r);
            int c = cor_para_gd(hex_para_int(n->u.circulo.cor->u.cor));
            gdImageFilledEllipse(canvas, cx, cy, r*2, r*2, c);
            break;
        }
        case AST_TEXTO: {
            int x = (int)eval(n->u.texto.x), y = (int)eval(n->u.texto.y);
            int c = cor_para_gd(hex_para_int(n->u.texto.cor->u.cor));
            gdImageString(canvas, gdFontSmall, x, y, (unsigned char*)n->u.texto.texto, c);
            break;
        }
        case AST_COR_FUNDO: {
            cor_bg = hex_para_int(n->u.cor_fundo.cor->u.cor);
            int c = gdImageColorAllocate(canvas, (cor_bg>>16)&0xff, (cor_bg>>8)&0xff, cor_bg&0xff);
            gdImageFilledRectangle(canvas, 0, 0, largura-1, altura-1, c);
            break;
        }
        case AST_ANIMA:
            fps = n->u.anima.fps;
            break;
        case AST_VAR:
            var_set(n->u.var.nome, eval(n->u.var.expr));
            break;
        case AST_ATRIBUICAO:
            var_set(n->u.atrib.nome, eval(n->u.atrib.expr));
            break;
        case AST_SE:
            if (eval(n->u.se.cond) != 0) executa_no(n->u.se.entao);
            else if (n->u.se.senao) executa_no(n->u.se.senao);
            break;
        case AST_REPETE: {
            int vezes = (int)eval(n->u.repete.vezes);
            for (int i = 0; i < vezes; i++) executa_no(n->u.repete.corpo);
            break;
        }
        case AST_QUADRO:
            executa_no(n->u.quadro.corpo);
            captura_frame();
            break;
        case AST_MOVE: {
            double x = eval(n->u.move.x), y = eval(n->u.move.y);
            /* interpolação simples: atualiza variável alvo */
            var_set(n->u.move.alvo, x);
            (void)y;
            break;
        }
        case AST_SALVA:
            arquivo_saida = strdup(n->u.salva.arquivo);
            break;
        default: break;
    }
}

int executar_programa(AstNode *raiz) {
    executa_no(raiz);
    if (!canvas) { fprintf(stderr, "Nenhum canvas criado (falta TELA).\n"); return 0; }
    if (!arquivo_saida) arquivo_saida = strdup("saida.png");
    int ok = 0;
    if (strstr(arquivo_saida, ".gif") && nframes > 0) ok = salva_gif(arquivo_saida);
    else ok = salva_png(arquivo_saida);
    if (ok) printf("Saída gerada: %s\n", arquivo_saida);
    else fprintf(stderr, "Falha ao salvar %s\n", arquivo_saida);
    return ok;
}