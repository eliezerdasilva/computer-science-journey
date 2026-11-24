/* semantic.c */
#include "semantic.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_VARS 128
typedef struct { char *nome; int linha; } Var;
static Var vars[MAX_VARS];
static int nvars = 0;
static int erro_semantico = 0;

static int var_existe(const char *n) {
    for (int i = 0; i < nvars; i++)
        if (strcmp(vars[i].nome, n) == 0) return 1;
    return 0;
}

static void declara_var(const char *n, int linha) {
    if (var_existe(n)) {
        erro_semantico = 1;
        fprintf(stderr, "Erro semântico (linha %d): variável '%s' já declarada\n", linha, n);
        return;
    }
    if (nvars >= MAX_VARS) {
        erro_semantico = 1;
        fprintf(stderr, "Erro semântico (linha %d): limite de variáveis atingido\n", linha);
        return;
    }
    vars[nvars].nome = strdup(n);
    vars[nvars].linha = linha;
    nvars++;
}

static void erro(const char *msg, int linha) {
    fprintf(stderr, "Erro semântico (linha %d): %s\n", linha, msg);
    erro_semantico = 1;
}

static void libera_vars(void) {
    for (int i = 0; i < nvars; i++) free(vars[i].nome);
    nvars = 0;
}

/* Forward declaration */
static void verifica_expr(AstNode *n);

static void verifica_expr(AstNode *n) {
    if (!n) return;
    switch (n->tipo) {
        case AST_IDENT:
            if (!var_existe(n->u.ident))
                erro("variável não declarada", n->linha);
            break;
        case AST_BINOP:
            verifica_expr(n->u.binop.esq);
            verifica_expr(n->u.binop.dir);
            /* divisão por zero constante */
            if (n->u.binop.op == OP_DIV &&
                n->u.binop.dir &&
                n->u.binop.dir->tipo == AST_NUM &&
                n->u.binop.dir->u.num == 0.0)
                erro("divisão por zero", n->linha);
            if (n->u.binop.op == OP_MOD &&
                n->u.binop.dir &&
                n->u.binop.dir->tipo == AST_NUM &&
                n->u.binop.dir->u.num == 0.0)
                erro("módulo por zero", n->linha);
            break;
        case AST_UNOP:
            verifica_expr(n->u.unop.operando);
            break;
        default:
            break;
    }
}

/* Helper para verificar pares (expr, cor) das primitivas de desenho */
static void verifica_no(AstNode *n) {
    if (!n) return;
    switch (n->tipo) {
        case AST_PROGRAMA:
            for (int i = 0; i < n->u.programa.n; i++)
                verifica_no(n->u.programa.itens[i]);
            break;
        case AST_BLOCO:
            for (int i = 0; i < n->u.bloco.n; i++)
                verifica_no(n->u.bloco.itens[i]);
            break;
        case AST_VAR:
            verifica_expr(n->u.var.expr);
            declara_var(n->u.var.nome, n->linha);
            break;
        case AST_ATRIBUICAO:
            if (!var_existe(n->u.atrib.nome))
                erro("atribuição a variável não declarada", n->linha);
            verifica_expr(n->u.atrib.expr);
            break;

        /* --- CORREÇÃO ITEM 4: verificar expressões internas --- */
        case AST_TELA:
            verifica_expr(n->u.tela.w);
            verifica_expr(n->u.tela.h);
            break;
        case AST_PIXEL:
            verifica_expr(n->u.pixel.x);
            verifica_expr(n->u.pixel.y);
            break;
        case AST_LINHA:
            verifica_expr(n->u.linha.x1);
            verifica_expr(n->u.linha.y1);
            verifica_expr(n->u.linha.x2);
            verifica_expr(n->u.linha.y2);
            break;
        case AST_RETANGULO:
            verifica_expr(n->u.retangulo.x);
            verifica_expr(n->u.retangulo.y);
            verifica_expr(n->u.retangulo.w);
            verifica_expr(n->u.retangulo.h);
            break;
        case AST_CIRCULO:
            verifica_expr(n->u.circulo.cx);
            verifica_expr(n->u.circulo.cy);
            verifica_expr(n->u.circulo.r);
            break;
        case AST_TEXTO:
            verifica_expr(n->u.texto.x);
            verifica_expr(n->u.texto.y);
            break;
        case AST_COR_FUNDO:
        case AST_SALVA:
            break;  /* sem expressões */

        case AST_SE:
            verifica_expr(n->u.se.cond);
            verifica_no(n->u.se.entao);
            verifica_no(n->u.se.senao);
            break;
        case AST_REPETE:
            verifica_expr(n->u.repete.vezes);
            /* repete com constante negativa é erro */
            if (n->u.repete.vezes &&
                n->u.repete.vezes->tipo == AST_NUM &&
                n->u.repete.vezes->u.num < 0)
                erro("REPETE com número negativo de vezes", n->linha);
            verifica_no(n->u.repete.corpo);
            break;
        case AST_QUADRO:
            verifica_no(n->u.quadro.corpo);
            break;
        case AST_ANIMA:
            if (n->u.anima.fps <= 0)
                erro("FPS deve ser positivo", n->linha);
            break;
        case AST_MOVE:
            if (!var_existe(n->u.move.alvo))
                erro("MOVE para variável não declarada", n->linha);
            verifica_expr(n->u.move.x);
            verifica_expr(n->u.move.y);
            verifica_expr(n->u.move.segundos);
            if (n->u.move.segundos &&
                n->u.move.segundos->tipo == AST_NUM &&
                n->u.move.segundos->u.num <= 0)
                erro("MOVE com duração <= 0 segundos", n->linha);
            break;
        default:
            break;
    }
}

int analisa_semantica(AstNode *raiz) {
    libera_vars();           /* CORREÇÃO ITEM 5: não vaza memória */
    erro_semantico = 0;
    verifica_no(raiz);
    libera_vars();           /* libera também ao final */
    return !erro_semantico;
}