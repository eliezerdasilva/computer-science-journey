#include "ast.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

AstNode *ast_novo(AstTipo tipo, int linha) {
    AstNode *n = calloc(1, sizeof(AstNode));
    n->tipo = tipo;
    n->linha = linha;
    return n;
}
AstNode *ast_binop(OpTipo op, AstNode *e, AstNode *d, int l) {
    AstNode *n = ast_novo(AST_BINOP, l);
    n->u.binop.op = op; n->u.binop.esq = e; n->u.binop.dir = d;
    return n;
}
AstNode *ast_unop(OpTipo op, AstNode *e, int l) {
    AstNode *n = ast_novo(AST_UNOP, l);
    n->u.unop.op = op; n->u.unop.operando = e;
    return n;
}
AstNode *ast_num(double v, int l) {
    AstNode *n = ast_novo(AST_NUM, l); n->u.num = v; return n;
}
AstNode *ast_string(const char *s, int l) {
    AstNode *n = ast_novo(AST_STRING, l); n->u.str = strdup(s); return n;
}
AstNode *ast_cor(const char *c, int l) {
    AstNode *n = ast_novo(AST_COR, l); n->u.cor = strdup(c); return n;
}
AstNode *ast_ident(const char *id, int l) {
    AstNode *n = ast_novo(AST_IDENT, l); n->u.ident = strdup(id); return n;
}

static const char *nome_tipo(AstTipo t) {
    switch (t) {
        case AST_PROGRAMA: return "PROGRAMA";
        case AST_TELA: return "TELA";
        case AST_PIXEL: return "PIXEL";
        case AST_LINHA: return "LINHA";
        case AST_RETANGULO: return "RETANGULO";
        case AST_CIRCULO: return "CIRCULO";
        case AST_TEXTO: return "TEXTO";
        case AST_COR_FUNDO: return "COR_FUNDO";
        case AST_ANIMA: return "ANIMA";
        case AST_SALVA: return "SALVA";
        case AST_VAR: return "VAR";
        case AST_ATRIBUICAO: return "ATRIBUICAO";
        case AST_SE: return "SE";
        case AST_REPETE: return "REPETE";
        case AST_MOVE: return "MOVE";
        case AST_QUADRO: return "QUADRO";
        case AST_BLOCO: return "BLOCO";
        case AST_BINOP: return "BINOP";
        case AST_UNOP: return "UNOP";
        case AST_NUM: return "NUM";
        case AST_STRING: return "STRING";
        case AST_IDENT: return "IDENT";
        case AST_COR: return "COR";
    }
    return "?";
}

void ast_imprime(AstNode *n, int nivel) {
    if (!n) return;
    for (int i = 0; i < nivel; i++) printf("  ");
    printf("%s", nome_tipo(n->tipo));
    if (n->tipo == AST_NUM) printf(" (%.2f)", n->u.num);
    if (n->tipo == AST_IDENT) printf(" (%s)", n->u.ident);
    if (n->tipo == AST_COR) printf(" (%s)", n->u.cor);
    if (n->tipo == AST_STRING) printf(" (\"%s\")", n->u.str);
    if (n->tipo == AST_BINOP) printf(" (op=%d)", n->u.binop.op);
    printf("\n");
    switch (n->tipo) {
        case AST_PROGRAMA: case AST_BLOCO: {
            int cnt = (n->tipo==AST_PROGRAMA)?n->u.programa.n:n->u.bloco.n;
            AstNode **it = (n->tipo==AST_PROGRAMA)?n->u.programa.itens:n->u.bloco.itens;
            for (int i = 0; i < cnt; i++) ast_imprime(it[i], nivel+1);
            break;
        }
        case AST_TELA:
            ast_imprime(n->u.tela.w, nivel+1);
            ast_imprime(n->u.tela.h, nivel+1);
            ast_imprime(n->u.tela.cor, nivel+1);
            break;
        case AST_PIXEL:
            ast_imprime(n->u.pixel.x, nivel+1);
            ast_imprime(n->u.pixel.y, nivel+1);
            ast_imprime(n->u.pixel.cor, nivel+1);
            break;
        case AST_LINHA:
            ast_imprime(n->u.linha.x1, nivel+1);
            ast_imprime(n->u.linha.y1, nivel+1);
            ast_imprime(n->u.linha.x2, nivel+1);
            ast_imprime(n->u.linha.y2, nivel+1);
            ast_imprime(n->u.linha.cor, nivel+1);
            break;
        case AST_RETANGULO:
            ast_imprime(n->u.retangulo.x, nivel+1);
            ast_imprime(n->u.retangulo.y, nivel+1);
            ast_imprime(n->u.retangulo.w, nivel+1);
            ast_imprime(n->u.retangulo.h, nivel+1);
            ast_imprime(n->u.retangulo.cor, nivel+1);
            break;
        case AST_CIRCULO:
            ast_imprime(n->u.circulo.cx, nivel+1);
            ast_imprime(n->u.circulo.cy, nivel+1);
            ast_imprime(n->u.circulo.r, nivel+1);
            ast_imprime(n->u.circulo.cor, nivel+1);
            break;
        case AST_TEXTO:
            ast_imprime(n->u.texto.x, nivel+1);
            ast_imprime(n->u.texto.y, nivel+1);
            ast_imprime(n->u.texto.cor, nivel+1);
            break;
        case AST_COR_FUNDO: ast_imprime(n->u.cor_fundo.cor, nivel+1); break;
        case AST_VAR: case AST_ATRIBUICAO: {
            AstNode *e = (n->tipo==AST_VAR)?n->u.var.expr:n->u.atrib.expr;
            const char *nm = (n->tipo==AST_VAR)?n->u.var.nome:n->u.atrib.nome;
            for (int i = 0; i <= nivel; i++) printf("  ");
            printf("nome=%s\n", nm);
            ast_imprime(e, nivel+1);
            break;
        }
        case AST_SE:
            ast_imprime(n->u.se.cond, nivel+1);
            ast_imprime(n->u.se.entao, nivel+1);
            if (n->u.se.senao) ast_imprime(n->u.se.senao, nivel+1);
            break;
        case AST_REPETE:
            ast_imprime(n->u.repete.vezes, nivel+1);
            ast_imprime(n->u.repete.corpo, nivel+1);
            break;
        case AST_MOVE:
            ast_imprime(n->u.move.x, nivel+1);
            ast_imprime(n->u.move.y, nivel+1);
            ast_imprime(n->u.move.segundos, nivel+1);
            break;
        case AST_QUADRO: ast_imprime(n->u.quadro.corpo, nivel+1); break;
        case AST_BINOP:
            ast_imprime(n->u.binop.esq, nivel+1);
            ast_imprime(n->u.binop.dir, nivel+1);
            break;
        case AST_UNOP: ast_imprime(n->u.unop.operando, nivel+1); break;
        default: break;
    }
}

void ast_libera(AstNode *n) {
    if (!n) return;
    /* liberação simplificada: apenas free, para projeto didático */
    free(n);
}