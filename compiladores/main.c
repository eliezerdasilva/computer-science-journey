#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ast.h"
#include "semantic.h"
#include "codegen.h"

extern FILE *yyin;
extern AstNode *raiz;
extern int tem_erro;
int yyparse(void);

int main(int argc, char **argv) {
    int opt_ast = 0, opt_no_run = 0;
    const char *arq = NULL;
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--ast") == 0) opt_ast = 1;
        else if (strcmp(argv[i], "--no-run") == 0) opt_no_run = 1;
        else arq = argv[i];
    }
    if (!arq) {
        fprintf(stderr, "Uso: %s [--ast] [--no-run] arquivo.dsl\n", argv[0]);
        return 1;
    }
    yyin = fopen(arq, "r");
    if (!yyin) { perror("fopen"); return 1; }

    if (yyparse() != 0 || tem_erro) {
        fprintf(stderr, "Falha na análise sintática.\n");
        return 1;
    }
    if (!raiz) { fprintf(stderr, "AST vazia.\n"); return 1; }
    if (opt_ast) ast_imprime(raiz, 0);

    if (!analisa_semantica(raiz)) {
        fprintf(stderr, "Falha na análise semântica.\n");
        return 1;
    }

    if (opt_no_run) { printf("Análise concluída (--no-run).\n"); return 0; }

    if (!executar_programa(raiz)) return 1;
    return 0;
}