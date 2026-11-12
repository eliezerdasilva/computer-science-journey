#ifndef AST_H
#define AST_H

typedef enum {
    AST_PROGRAMA,
    AST_TELA, AST_PIXEL, AST_LINHA, AST_RETANGULO, AST_CIRCULO,
    AST_TEXTO, AST_COR_FUNDO, AST_ANIMA, AST_SALVA,
    AST_VAR, AST_ATRIBUICAO, AST_SE, AST_REPETE, AST_MOVE,
    AST_QUADRO, AST_BLOCO,
    AST_BINOP, AST_UNOP, AST_NUM, AST_STRING, AST_IDENT, AST_COR
} AstTipo;

typedef enum { OP_ADD, OP_SUB, OP_MUL, OP_DIV, OP_MOD,
               OP_EQ, OP_NE, OP_LT, OP_GT, OP_LE, OP_GE,
               OP_AND, OP_OR, OP_NOT } OpTipo;

typedef struct AstNode {
    AstTipo tipo;
    int linha;
    union {
        struct { struct AstNode *itens[256]; int n; } programa;
        struct { struct AstNode *w, *h, *cor; } tela;
        struct { struct AstNode *x, *y, *cor; } pixel;
        struct { struct AstNode *x1, *y1, *x2, *y2, *cor; } linha;
        struct { struct AstNode *x, *y, *w, *h, *cor; } retangulo;
        struct { struct AstNode *cx, *cy, *r, *cor; } circulo;
        struct { char *texto; struct AstNode *x, *y, *cor; } texto;
        struct { struct AstNode *cor; } cor_fundo;
        struct { int fps; } anima;
        struct { char *arquivo; } salva;
        struct { char *nome; struct AstNode *expr; } var;
        struct { char *nome; struct AstNode *expr; } atrib;
        struct { struct AstNode *cond, *entao, *senao; } se;
        struct { struct AstNode *vezes, *corpo; } repete;
        struct { char *alvo; struct AstNode *x, *y, *segundos; } move;
        struct { struct AstNode *corpo; } quadro;
        struct { struct AstNode *itens[256]; int n; } bloco;
        struct { struct AstNode *esq, *dir; OpTipo op; } binop;
        struct { struct AstNode *operando; OpTipo op; } unop;
        double num;
        char *str;
        char *cor;
        char *ident;
    } u;
} AstNode;

AstNode *ast_novo(AstTipo tipo, int linha);
AstNode *ast_binop(OpTipo op, AstNode *e, AstNode *d, int linha);
AstNode *ast_unop(OpTipo op, AstNode *e, int linha);
AstNode *ast_num(double v, int linha);
AstNode *ast_string(const char *s, int linha);
AstNode *ast_cor(const char *c, int linha);
AstNode *ast_ident(const char *n, int linha);
void ast_libera(AstNode *n);
void ast_imprime(AstNode *n, int nivel);

#endif