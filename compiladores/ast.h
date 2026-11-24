/* ast.h */
#ifndef AST_H
#define AST_H

/* ============================================================
 * 1. ENUM DE OPERADORES (deve vir ANTES do struct AstNode)
 * ============================================================ */
typedef enum {
    OP_ADD, OP_SUB, OP_MUL, OP_DIV, OP_MOD,
    OP_EQ, OP_NE, OP_LT, OP_GT, OP_LE, OP_GE,
    OP_AND, OP_OR, OP_NOT,
    OP_NEG                      /* menos unário */
} OpTipo;

/* ============================================================
 * 2. ENUM DE TIPOS DE NÓ
 * ============================================================ */
typedef enum {
    AST_PROGRAMA, AST_BLOCO, AST_VAR, AST_ATRIBUICAO,
    AST_TELA, AST_PIXEL, AST_LINHA, AST_RETANGULO,
    AST_CIRCULO, AST_TEXTO, AST_COR_FUNDO, AST_SALVA,
    AST_SE, AST_REPETE, AST_QUADRO, AST_ANIMA, AST_MOVE,
    AST_NUM, AST_IDENT, AST_BINOP, AST_UNOP
} AstTipo;

/* ============================================================
 * 3. STRUCT DO NÓ
 * ============================================================ */
typedef struct AstNode {
    AstTipo tipo;
    int linha;
    union {
        double num;
        char  *ident;
        struct { struct AstNode *esq, *dir; OpTipo op; } binop;
        struct { struct AstNode *operando; OpTipo op; } unop;
        struct { struct AstNode **itens; int n; int cap; } programa;
        struct { struct AstNode **itens; int n; int cap; } bloco;
        struct { char *nome; struct AstNode *expr; } var;
        struct { char *nome; struct AstNode *expr; } atrib;
        struct { struct AstNode *w, *h; int cor; } tela;
        struct { struct AstNode *x, *y; int cor; } pixel;
        struct { struct AstNode *x1, *y1, *x2, *y2; int cor; } linha;
        struct { struct AstNode *x, *y, *w, *h; int cor; } retangulo;
        struct { struct AstNode *cx, *cy, *r; int cor; } circulo;
        struct { char *texto; struct AstNode *x, *y; int cor; } texto;
        struct { int cor; } cor_fundo;
        struct { char *arquivo; } salva;
        struct { struct AstNode *cond, *entao, *senao; } se;
        struct { struct AstNode *vezes, *corpo; } repete;
        struct { struct AstNode *corpo; } quadro;
        struct { int fps; } anima;
        struct { char *alvo; struct AstNode *x, *y, *segundos; } move;
    } u;
} AstNode;

/* ============================================================
 * 4. PROTÓTIPOS
 * ============================================================ */
AstNode *ast_novo(AstTipo tipo, int capacidade);
AstNode *ast_num(double v, int linha);
AstNode *ast_ident(char *nome, int linha);
AstNode *ast_binop(OpTipo op, AstNode *e, AstNode *d, int linha);
AstNode *ast_unop(OpTipo op, AstNode *e, int linha);
AstNode *ast_cor(char *hex, int linha);
void     ast_bloco_push(AstNode *bloco, AstNode *filho);
void     ast_imprime(AstNode *n, int nivel);
void     ast_libera(AstNode *n);

#endif /* AST_H */