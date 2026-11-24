/* codegen.c — gera C, compila e executa (one-step) */
#include "codegen.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ============ Helper: int RGB → "#RRGGBB" ============ */
static const char *cor_para_str(int rgb) {
    static char bufs[4][8];
    static int idx = 0;
    char *b = bufs[idx];
    idx = (idx + 1) % 4;
    snprintf(b, 8, "#%06X", rgb & 0xFFFFFF);
    return b;
}

/* ============ Estado do codegen ============ */
static FILE *out;
static int nvars = 0;
static char *vars[128];
static int fps = 10;
static char *arquivo_saida = NULL;

static int var_idx(const char *n) {
    for (int i = 0; i < nvars; i++)
        if (strcmp(vars[i], n) == 0) return i;
    vars[nvars] = strdup(n);
    return nvars++;
}

/* ============ Emissão de expressões ============ */
static void emite_expr(AstNode *n) {
    if (!n) { fprintf(out, "0"); return; }
    switch (n->tipo) {
        case AST_NUM:
            fprintf(out, "%.4f", n->u.num); break;
        case AST_IDENT:
            fprintf(out, "v[%d]", var_idx(n->u.ident)); break;
        case AST_BINOP: {
            OpTipo op = n->u.binop.op;
            fprintf(out, "(");
            emite_expr(n->u.binop.esq);
            switch (op) {
                case OP_ADD: fprintf(out, " + "); break;
                case OP_SUB: fprintf(out, " - "); break;
                case OP_MUL: fprintf(out, " * "); break;
                case OP_DIV: fprintf(out, " / "); break;
                case OP_MOD: fprintf(out, " %% "); break;
                case OP_EQ:  fprintf(out, " == "); break;
                case OP_NE:  fprintf(out, " != "); break;
                case OP_LT:  fprintf(out, " < ");  break;
                case OP_GT:  fprintf(out, " > ");  break;
                case OP_LE:  fprintf(out, " <= "); break;
                case OP_GE:  fprintf(out, " >= "); break;
                case OP_AND: fprintf(out, " && "); break;
                case OP_OR:  fprintf(out, " || "); break;
                default:     fprintf(out, " /*op?*/ "); break;
            }
            emite_expr(n->u.binop.dir);
            fprintf(out, ")");
            break;
        }
        case AST_UNOP:
            if (n->u.unop.op == OP_NEG) fprintf(out, "(-");
            else                        fprintf(out, "(!");
            emite_expr(n->u.unop.operando);
            fprintf(out, ")");
            break;
        default:
            fprintf(out, "0"); break;
    }
}

/* ============ Emissão de comandos ============ */
static void emite_cmd(AstNode *n);

static void emite_bloco(AstNode *b) {
    if (!b) return;
    int cnt = (b->tipo == AST_PROGRAMA) ? b->u.programa.n : b->u.bloco.n;
    AstNode **it = (b->tipo == AST_PROGRAMA) ? b->u.programa.itens : b->u.bloco.itens;
    for (int i = 0; i < cnt; i++) emite_cmd(it[i]);
}

static void emite_cmd(AstNode *n) {
    if (!n) return;
    switch (n->tipo) {
        case AST_TELA:
            fprintf(out, "  largura = (int)("); emite_expr(n->u.tela.w); fprintf(out, ");\n");
            fprintf(out, "  altura  = (int)("); emite_expr(n->u.tela.h); fprintf(out, ");\n");
            fprintf(out, "  if (canvas) gdImageDestroy(canvas);\n");
            fprintf(out, "  canvas = gdImageCreateTrueColor(largura, altura);\n");
            fprintf(out, "  { int bg = cor_gd(\"%s\");\n", cor_para_str(n->u.tela.cor));
            fprintf(out, "    gdImageFilledRectangle(canvas, 0,0, largura-1, altura-1, bg); }\n");
            break;
        case AST_COR_FUNDO:
            fprintf(out, "  { int bg = cor_gd(\"%s\");\n", cor_para_str(n->u.cor_fundo.cor));
            fprintf(out, "    gdImageFilledRectangle(canvas, 0,0, largura-1, altura-1, bg); }\n");
            break;
        case AST_PIXEL:
            fprintf(out, "  gdImageSetPixel(canvas, (int)(");
            emite_expr(n->u.pixel.x); fprintf(out, "), (int)(");
            emite_expr(n->u.pixel.y);
            fprintf(out, "), cor_gd(\"%s\"));\n", cor_para_str(n->u.pixel.cor));
            break;
        case AST_LINHA:
            fprintf(out, "  gdImageLine(canvas, (int)(");
            emite_expr(n->u.linha.x1); fprintf(out, "), (int)(");
            emite_expr(n->u.linha.y1); fprintf(out, "), (int)(");
            emite_expr(n->u.linha.x2); fprintf(out, "), (int)(");
            emite_expr(n->u.linha.y2);
            fprintf(out, "), cor_gd(\"%s\"));\n", cor_para_str(n->u.linha.cor));
            break;
        case AST_RETANGULO:
            fprintf(out, "  { int _x = (int)("); emite_expr(n->u.retangulo.x);
            fprintf(out, "), _y = (int)("); emite_expr(n->u.retangulo.y);
            fprintf(out, "), _w = (int)("); emite_expr(n->u.retangulo.w);
            fprintf(out, "), _h = (int)("); emite_expr(n->u.retangulo.h);
            fprintf(out, ");\n    gdImageFilledRectangle(canvas, _x,_y, _x+_w-1, _y+_h-1, cor_gd(\"%s\")); }\n",
                    cor_para_str(n->u.retangulo.cor));
            break;
        case AST_CIRCULO:
            fprintf(out, "  { int _cx = (int)("); emite_expr(n->u.circulo.cx);
            fprintf(out, "), _cy = (int)("); emite_expr(n->u.circulo.cy);
            fprintf(out, "), _r = (int)("); emite_expr(n->u.circulo.r);
            fprintf(out, ");\n    gdImageFilledEllipse(canvas, _cx,_cy, 2*_r, 2*_r, cor_gd(\"%s\")); }\n",
                    cor_para_str(n->u.circulo.cor));
            break;
        case AST_TEXTO:
            fprintf(out, "  gdImageString(canvas, gdFontSmall, (int)(");
            emite_expr(n->u.texto.x); fprintf(out, "), (int)(");
            emite_expr(n->u.texto.y);
            fprintf(out, "), (unsigned char*)\"%s\", cor_gd(\"%s\"));\n",
                    n->u.texto.texto, cor_para_str(n->u.texto.cor));
            break;
        case AST_VAR:
            fprintf(out, "  v[%d] = (double)(", var_idx(n->u.var.nome));
            emite_expr(n->u.var.expr);
            fprintf(out, ");\n");
            break;
        case AST_ATRIBUICAO:
            fprintf(out, "  v[%d] = (double)(", var_idx(n->u.atrib.nome));
            emite_expr(n->u.atrib.expr);
            fprintf(out, ");\n");
            break;
        case AST_SE:
            fprintf(out, "  if ("); emite_expr(n->u.se.cond); fprintf(out, ") {\n");
            emite_bloco(n->u.se.entao);
            fprintf(out, "  }");
            if (n->u.se.senao) {
                fprintf(out, " else {\n");
                emite_bloco(n->u.se.senao);
                fprintf(out, "  }");
            }
            fprintf(out, "\n");
            break;
        case AST_REPETE: {
            static int rep_counter = 0;
            int rid = rep_counter++;
            fprintf(out, "  for (int __r%d = 0; __r%d < (int)(", rid, rid);
            emite_expr(n->u.repete.vezes);
            fprintf(out, "); __r%d++) {\n", rid);
            emite_bloco(n->u.repete.corpo);
            fprintf(out, "  }\n");
            break;
        }
        case AST_QUADRO:
            emite_bloco(n->u.quadro.corpo);
            break;
        case AST_ANIMA:
            fps = n->u.anima.fps;
            break;
        case AST_MOVE:
            fprintf(out, "  v[%d] = (double)(", var_idx(n->u.move.alvo));
            emite_expr(n->u.move.x);
            fprintf(out, ");\n");
            break;
        case AST_SALVA:
            free(arquivo_saida);
            arquivo_saida = strdup(n->u.salva.arquivo);
            break;
        default: break;
    }
}

/* ============ Pipeline one-step ============ */
int executar_programa(AstNode *raiz) {
    const char *caminho_c   = "saida_gerada.c";
    const char *caminho_bin = "saida_gerada";

    /* ETAPA 1 — cria e abre saida_gerada.c */
    out = fopen(caminho_c, "w");
    if (!out) { perror("fopen saida_gerada.c"); return 0; }

    /* ETAPA 2 — cabeçalho do C gerado */
    fprintf(out, "#include <gd.h>\n#include <gdfonts.h>\n"
                 "#include <stdio.h>\n#include <stdlib.h>\n"
                 "#include <string.h>\n#include <math.h>\n\n");
    fprintf(out, "static gdImagePtr canvas = NULL;\n");
    fprintf(out, "static int largura = 0, altura = 0;\n");
    fprintf(out, "static double v[256];\n\n");
    fprintf(out,
        "static int cor_gd(const char *h) {\n"
        "    int r=0,g=0,b=0; sscanf(h+1, \"%%02x%%02x%%02x\", &r,&g,&b);\n"
        "    return gdImageColorAllocate(canvas, r, g, b);\n"
        "}\n\n");
    fprintf(out, "int main(void) {\n");

    /* ETAPA 3 — traduz a AST para C */
    emite_bloco(raiz);

    /* ETAPA 4 — fecha o main() e o arquivo */
    const char *saida = arquivo_saida ? arquivo_saida : "saida.png";
    fprintf(out, "  if (!canvas) { fprintf(stderr, \"Nenhum canvas.\\n\"); return 1; }\n");
    fprintf(out, "  { FILE *f = fopen(\"%s\", \"wb\");\n", saida);
    fprintf(out, "    if (!f) { perror(\"fopen\"); return 1; }\n");
    fprintf(out, "    gdImagePng(canvas, f); fclose(f); }\n");
    fprintf(out, "  gdImageDestroy(canvas);\n");
    fprintf(out, "  printf(\"Imagem salva em %s\\n\");\n", saida);
    fprintf(out, "  return 0;\n}\n");
    fclose(out);

    /* ETAPA 5 — compila saida_gerada.c → saida_gerada */
    char cmd[1024];
    snprintf(cmd, sizeof(cmd),
             "gcc -O2 -o %s %s -lgd -lm", caminho_bin, caminho_c);
    int rc = system(cmd);
    if (rc != 0) {
        fprintf(stderr, "Falha ao compilar %s (rc=%d).\n", caminho_c, rc);
        return 0;
    }

    /* ETAPA 6 — executa saida_gerada → gera PNG */
    snprintf(cmd, sizeof(cmd), "./%s", caminho_bin);
    rc = system(cmd);
    if (rc != 0) {
        fprintf(stderr, "Falha ao executar %s (rc=%d).\n", caminho_bin, rc);
        return 0;
    }

    /* PRESERVA saida_gerada.c e saida_gerada para inspeção/execução manual.
       Não chamamos remove(). */

    /* Limpeza de estado interno */
    for (int i = 0; i < nvars; i++) free(vars[i]);
    nvars = 0;
    free(arquivo_saida);
    arquivo_saida = NULL;

    return 1;
}