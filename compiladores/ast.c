/* ast.c */
#include "ast.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Cria um nó bruto; capacidade só é usada por AST_PROGRAMA/AST_BLOCO */
AstNode *ast_novo(AstTipo tipo, int capacidade) {
    AstNode *n = calloc(1, sizeof(AstNode));
    if (!n) { perror("calloc"); exit(1); }
    n->tipo = tipo;
    n->linha = 0;
    if (tipo == AST_PROGRAMA) {
        n->u.programa.cap = capacidade > 0 ? capacidade : 4;
        n->u.programa.n = 0;
        n->u.programa.itens = malloc(sizeof(AstNode*) * n->u.programa.cap);
    } else if (tipo == AST_BLOCO) {
        n->u.bloco.cap = capacidade > 0 ? capacidade : 4;
        n->u.bloco.n = 0;
        n->u.bloco.itens = malloc(sizeof(AstNode*) * n->u.bloco.cap);
    }
    return n;
}

AstNode *ast_num(double v, int linha) {
    AstNode *n = ast_novo(AST_NUM, 0);
    n->linha = linha;
    n->u.num = v;
    return n;
}

AstNode *ast_ident(char *nome, int linha) {
    AstNode *n = ast_novo(AST_IDENT, 0);
    n->linha = linha;
    n->u.ident = nome;
    return n;
}

AstNode *ast_binop(OpTipo op, AstNode *e, AstNode *d, int linha) {
    AstNode *n = ast_novo(AST_BINOP, 0);
    n->linha = linha;
    n->u.binop.op = op;
    n->u.binop.esq = e;
    n->u.binop.dir = d;
    return n;
}

AstNode *ast_unop(OpTipo op, AstNode *e, int linha) {
    AstNode *n = ast_novo(AST_UNOP, 0);
    n->linha = linha;
    n->u.unop.op = op;
    n->u.unop.operando = e;
    return n;
}

AstNode *ast_cor(char *hex, int linha) {
    /* hex no formato "#RRGGBB" */
    AstNode *n = ast_novo(AST_NUM, 0);
    n->linha = linha;
    unsigned int r = 0, g = 0, b = 0;
    if (hex && hex[0] == '#' && strlen(hex) >= 7) {
        sscanf(hex + 1, "%2x%2x%2x", &r, &g, &b);
    }
    n->u.num = (double)((r << 16) | (g << 8) | b);
    free(hex);
    return n;
}

void ast_bloco_push(AstNode *bloco, AstNode *filho) {
    if (bloco->u.bloco.n >= bloco->u.bloco.cap) {
        bloco->u.bloco.cap = bloco->u.bloco.cap ? bloco->u.bloco.cap * 2 : 4;
        bloco->u.bloco.itens = realloc(bloco->u.bloco.itens,
                                       sizeof(AstNode*) * bloco->u.bloco.cap);
    }
    bloco->u.bloco.itens[bloco->u.bloco.n++] = filho;
}

/* Impressão recursiva (para --ast) */
static const char *tipo_nome(AstTipo t) {
    switch (t) {
        case AST_PROGRAMA: return "PROGRAMA";
        case AST_BLOCO: return "BLOCO";
        case AST_VAR: return "VAR";
        case AST_ATRIBUICAO: return "ATRIBUICAO";
        case AST_TELA: return "TELA";
        case AST_PIXEL: return "PIXEL";
        case AST_LINHA: return "LINHA";
        case AST_RETANGULO: return "RETANGULO";
        case AST_CIRCULO: return "CIRCULO";
        case AST_TEXTO: return "TEXTO";
        case AST_COR_FUNDO: return "COR_FUNDO";
        case AST_SALVA: return "SALVA";
        case AST_SE: return "SE";
        case AST_REPETE: return "REPETE";
        case AST_QUADRO: return "QUADRO";
        case AST_ANIMA: return "ANIMA";
        case AST_MOVE: return "MOVE";
        case AST_NUM: return "NUM";
        case AST_IDENT: return "IDENT";
        case AST_BINOP: return "BINOP";
        case AST_UNOP: return "UNOP";
        default: return "?";
    }
}

void ast_imprime(AstNode *n, int nivel) {
    if (!n) return;
    for (int i = 0; i < nivel; i++) printf("  ");
    printf("%s (linha %d)\n", tipo_nome(n->tipo), n->linha);
    switch (n->tipo) {
        case AST_PROGRAMA:
            for (int i = 0; i < n->u.programa.n; i++) ast_imprime(n->u.programa.itens[i], nivel + 1);
            break;
        case AST_BLOCO:
            for (int i = 0; i < n->u.bloco.n; i++) ast_imprime(n->u.bloco.itens[i], nivel + 1);
            break;
        case AST_VAR:
            for (int i = 0; i < nivel + 1; i++) printf("  ");
            printf("nome: %s\n", n->u.var.nome);
            ast_imprime(n->u.var.expr, nivel + 1);
            break;
        case AST_ATRIBUICAO:
            for (int i = 0; i < nivel + 1; i++) printf("  ");
            printf("nome: %s\n", n->u.atrib.nome);
            ast_imprime(n->u.atrib.expr, nivel + 1);
            break;
        case AST_BINOP:
            ast_imprime(n->u.binop.esq, nivel + 1);
            ast_imprime(n->u.binop.dir, nivel + 1);
            break;
        case AST_UNOP:
            ast_imprime(n->u.unop.operando, nivel + 1);
            break;
        case AST_SE:
            ast_imprime(n->u.se.cond, nivel + 1);
            ast_imprime(n->u.se.entao, nivel + 1);
            ast_imprime(n->u.se.senao, nivel + 1);
            break;
        case AST_REPETE:
            ast_imprime(n->u.repete.vezes, nivel + 1);
            ast_imprime(n->u.repete.corpo, nivel + 1);
            break;
        case AST_QUADRO:
            ast_imprime(n->u.quadro.corpo, nivel + 1);
            break;
        case AST_MOVE:
            ast_imprime(n->u.move.x, nivel + 1);
            ast_imprime(n->u.move.y, nivel + 1);
            ast_imprime(n->u.move.segundos, nivel + 1);
            break;
        case AST_TELA:
            ast_imprime(n->u.tela.w, nivel + 1);
            ast_imprime(n->u.tela.h, nivel + 1);
            break;
        case AST_PIXEL:
            ast_imprime(n->u.pixel.x, nivel + 1);
            ast_imprime(n->u.pixel.y, nivel + 1);
            break;
        case AST_LINHA:
            ast_imprime(n->u.linha.x1, nivel + 1);
            ast_imprime(n->u.linha.y1, nivel + 1);
            ast_imprime(n->u.linha.x2, nivel + 1);
            ast_imprime(n->u.linha.y2, nivel + 1);
            break;
        case AST_RETANGULO:
            ast_imprime(n->u.retangulo.x, nivel + 1);
            ast_imprime(n->u.retangulo.y, nivel + 1);
            ast_imprime(n->u.retangulo.w, nivel + 1);
            ast_imprime(n->u.retangulo.h, nivel + 1);
            break;
        case AST_CIRCULO:
            ast_imprime(n->u.circulo.cx, nivel + 1);
            ast_imprime(n->u.circulo.cy, nivel + 1);
            ast_imprime(n->u.circulo.r, nivel + 1);
            break;
        case AST_TEXTO:
            ast_imprime(n->u.texto.x, nivel + 1);
            ast_imprime(n->u.texto.y, nivel + 1);
            break;
        case AST_NUM:
            for (int i = 0; i < nivel + 1; i++) printf("  ");
            printf("valor: %g\n", n->u.num);
            break;
        case AST_IDENT:
            for (int i = 0; i < nivel + 1; i++) printf("  ");
            printf("nome: %s\n", n->u.ident);
            break;
        default: break;
    }
}

void ast_libera(AstNode *n) {
    if (!n) return;
    switch (n->tipo) {
        case AST_PROGRAMA:
            for (int i = 0; i < n->u.programa.n; i++) ast_libera(n->u.programa.itens[i]);
            free(n->u.programa.itens);
            break;
        case AST_BLOCO:
            for (int i = 0; i < n->u.bloco.n; i++) ast_libera(n->u.bloco.itens[i]);
            free(n->u.bloco.itens);
            break;
        case AST_VAR:        free(n->u.var.nome);   ast_libera(n->u.var.expr);   break;
        case AST_ATRIBUICAO: free(n->u.atrib.nome); ast_libera(n->u.atrib.expr); break;
        case AST_IDENT:      free(n->u.ident);      break;
        case AST_BINOP:      ast_libera(n->u.binop.esq); ast_libera(n->u.binop.dir); break;
        case AST_UNOP:       ast_libera(n->u.unop.operando); break;
        case AST_TELA:       ast_libera(n->u.tela.w); ast_libera(n->u.tela.h); break;
        case AST_PIXEL:      ast_libera(n->u.pixel.x); ast_libera(n->u.pixel.y); break;
        case AST_LINHA:
            ast_libera(n->u.linha.x1); ast_libera(n->u.linha.y1);
            ast_libera(n->u.linha.x2); ast_libera(n->u.linha.y2); break;
        case AST_RETANGULO:
            ast_libera(n->u.retangulo.x); ast_libera(n->u.retangulo.y);
            ast_libera(n->u.retangulo.w); ast_libera(n->u.retangulo.h); break;
        case AST_CIRCULO:
            ast_libera(n->u.circulo.cx); ast_libera(n->u.circulo.cy);
            ast_libera(n->u.circulo.r); break;
        case AST_TEXTO:
            free(n->u.texto.texto);
            ast_libera(n->u.texto.x); ast_libera(n->u.texto.y); break;
        case AST_SALVA:      free(n->u.salva.arquivo); break;
        case AST_SE:
            ast_libera(n->u.se.cond); ast_libera(n->u.se.entao);
            ast_libera(n->u.se.senao); break;
        case AST_REPETE:
            ast_libera(n->u.repete.vezes); ast_libera(n->u.repete.corpo); break;
        case AST_QUADRO:     ast_libera(n->u.quadro.corpo); break;
        case AST_MOVE:
            free(n->u.move.alvo);
            ast_libera(n->u.move.x); ast_libera(n->u.move.y);
            ast_libera(n->u.move.segundos); break;
        default: break;
    }
    free(n);
}