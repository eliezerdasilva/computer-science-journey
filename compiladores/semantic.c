/* semantic.c */
#include "semantic.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_VARS 128
typedef struct { char *nome; int declarada; } Var;
static Var vars[MAX_VARS];
static int nvars = 0;
static int erro_semantico = 0;

static int var_existe(const char *n) {
    for (int i = 0; i < nvars; i++)
        if (strcmp(vars[i].nome, n) == 0) return 1;
    return 0;
}
static void declara_var(const char *n) {
    if (nvars < MAX_VARS) { vars[nvars].nome = strdup(n); vars[nvars].declarada = 1; nvars++; }
}
static void erro(const char *msg, int linha) {
    fprintf(stderr, "Erro semântico (linha %d): %s\n", linha, msg);
    erro_semantico = 1;
}

static void verifica_expr(AstNode *n) {
    if (!n) return;
    if (n->tipo == AST_IDENT) {
        if (!var_existe(n->u.ident))
            erro("variável não declarada", n->linha);
    } else if (n->tipo == AST_BINOP) {
        verifica_expr(n->u.binop.esq);
        verifica_expr(n->u.binop.dir);
    } else if (n->tipo == AST_UNOP) {
        verifica_expr(n->u.unop.operando);
    }
}

static void verifica_no(AstNode *n) {
    if (!n) return;
    switch (n->tipo) {
        case AST_PROGRAMA:
            for (int i = 0; i < n->u.programa.n; i++) verifica_no(n->u.programa.itens[i]);
            break;
        case AST_BLOCO:
            for (int i = 0; i < n->u.bloco.n; i++) verifica_no(n->u.bloco.itens[i]);
            break;
        case AST_VAR:
            verifica_expr(n->u.var.expr);
            declara_var(n->u.var.nome);
            break;
        case AST_ATRIBUICAO:
            if (!var_existe(n->u.atrib.nome))
                erro("atribuição a variável não declarada", n->linha);
            verifica_expr(n->u.atrib.expr);
            break;
        case AST_TELA: case AST_PIXEL: case AST_LINHA: case AST_RETANGULO:
        case AST_CIRCULO: case AST_TEXTO:
            /* expressões internas */
            break;
        case AST_SE:
            verifica_expr(n->u.se.cond);
            verifica_no(n->u.se.entao);
            verifica_no(n->u.se.senao);
            break;
        case AST_REPETE:
            verifica_expr(n->u.repete.vezes);
            verifica_no(n->u.repete.corpo);
            break;
        case AST_QUADRO:
            verifica_no(n->u.quadro.corpo);
            break;
        case AST_ANIMA:
            if (n->u.anima.fps <= 0) erro("FPS deve ser positivo", n->linha);
            break;
        case AST_MOVE:
            if (!var_existe(n->u.move.alvo))
                erro("MOVE para variável não declarada", n->linha);
            verifica_expr(n->u.move.x);
            verifica_expr(n->u.move.y);
            verifica_expr(n->u.move.segundos);
            break;
        default: break;
    }
}

int analisa_semantica(AstNode *raiz) {
    nvars = 0; erro_semantico = 0;
    verifica_no(raiz);
    return !erro_semantico;
}