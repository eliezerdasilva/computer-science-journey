%code requires {
#include "ast.h"
}

%{
#include "ast.h"
#include "semantic.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylex(void);
extern int linha_atual;
void yyerror(const char *s);

AstNode *raiz = NULL;
int tem_erro = 0;
%}

%union {
    double num;
    char *str;
    AstNode *node;
}

%token TELA PIXEL LINHA RETANGULO CIRCULO TEXTO COR_FUNDO ANIMA SALVA
%token VAR SE SENAO FIM REPETE VEZES MOVE PARA EM SEGUNDOS QUADRO FPS
%token E OU NAO
%token ATRIB EQ NE LT GT LE GE
%token <str> IDENT STRING COR
%token <num> NUM

%type <node> programa lista_cmds cmd desenho controle animacao
%type <node> expressao expr_logica expr_rel expr_arit expr_termo expr_fator

%left OU
%left E
%nonassoc NAO
%nonassoc EQ NE LT GT LE GE
%left '+' '-'
%left '*' '/' '%'

%%
programa:
    lista_cmds              { raiz = ast_novo(AST_PROGRAMA, 1); raiz->u.programa.n = $1->u.bloco.n;
                              memcpy(raiz->u.programa.itens, $1->u.bloco.itens, sizeof(AstNode*)*$1->u.bloco.n); $$ = raiz; }
  ;

lista_cmds:
    /* vazio */             { $$ = ast_novo(AST_BLOCO, 0); }
  | lista_cmds cmd          { AstNode *b = $1; b->u.bloco.itens[b->u.bloco.n++] = $2; $$ = b; }
  ;

cmd:
    desenho ';'             { $$ = $1; }
  | controle                { $$ = $1; }
  | animacao                { $$ = $1; }
  | VAR IDENT ATRIB expressao ';'   { AstNode *n = ast_novo(AST_VAR, linha_atual);
                                       n->u.var.nome = $2; n->u.var.expr = $4; $$ = n; }
  | IDENT ATRIB expressao ';'       { AstNode *n = ast_novo(AST_ATRIBUICAO, linha_atual);
                                       n->u.atrib.nome = $1; n->u.atrib.expr = $3; $$ = n; }
  ;

desenho:
    TELA expressao ',' expressao ',' COR
        { AstNode *n = ast_novo(AST_TELA, linha_atual);
          n->u.tela.w = $2; n->u.tela.h = $4; n->u.tela.cor = ast_cor($6, linha_atual); $$ = n; }
  | PIXEL expressao ',' expressao ',' COR
        { AstNode *n = ast_novo(AST_PIXEL, linha_atual);
          n->u.pixel.x = $2; n->u.pixel.y = $4; n->u.pixel.cor = ast_cor($6, linha_atual); $$ = n; }
  | LINHA expressao ',' expressao ',' expressao ',' expressao ',' COR
        { AstNode *n = ast_novo(AST_LINHA, linha_atual);
          n->u.linha.x1=$2; n->u.linha.y1=$4; n->u.linha.x2=$6; n->u.linha.y2=$8;
          n->u.linha.cor = ast_cor($10, linha_atual); $$ = n; }
  | RETANGULO expressao ',' expressao ',' expressao ',' expressao ',' COR
        { AstNode *n = ast_novo(AST_RETANGULO, linha_atual);
          n->u.retangulo.x=$2; n->u.retangulo.y=$4; n->u.retangulo.w=$6; n->u.retangulo.h=$8;
          n->u.retangulo.cor = ast_cor($10, linha_atual); $$ = n; }
  | CIRCULO expressao ',' expressao ',' expressao ',' COR
        { AstNode *n = ast_novo(AST_CIRCULO, linha_atual);
          n->u.circulo.cx=$2; n->u.circulo.cy=$4; n->u.circulo.r=$6;
          n->u.circulo.cor = ast_cor($8, linha_atual); $$ = n; }
  | TEXTO STRING EM expressao ',' expressao ',' COR
        { AstNode *n = ast_novo(AST_TEXTO, linha_atual);
          n->u.texto.texto = $2; n->u.texto.x = $4; n->u.texto.y = $6;
          n->u.texto.cor = ast_cor($8, linha_atual); $$ = n; }
  | COR_FUNDO COR
        { AstNode *n = ast_novo(AST_COR_FUNDO, linha_atual);
          n->u.cor_fundo.cor = ast_cor($2, linha_atual); $$ = n; }
  | SALVA STRING
    { AstNode *n = ast_novo(AST_SALVA, linha_atual);
      n->u.salva.arquivo = $2; $$ = n; }
  ;

controle:
    SE expressao lista_cmds FIM
        { AstNode *n = ast_novo(AST_SE, linha_atual);
          n->u.se.cond = $2; n->u.se.entao = $3; n->u.se.senao = NULL; $$ = n; }
  | SE expressao lista_cmds SENAO lista_cmds FIM
        { AstNode *n = ast_novo(AST_SE, linha_atual);
          n->u.se.cond = $2; n->u.se.entao = $3; n->u.se.senao = $5; $$ = n; }
  | REPETE expressao VEZES lista_cmds FIM
        { AstNode *n = ast_novo(AST_REPETE, linha_atual);
          n->u.repete.vezes = $2; n->u.repete.corpo = $4; $$ = n; }
  ;

animacao:
    ANIMA FPS NUM ';'
        { AstNode *n = ast_novo(AST_ANIMA, linha_atual); n->u.anima.fps = (int)$3; $$ = n; }
  | MOVE IDENT PARA '(' expressao ',' expressao ')' EM expressao SEGUNDOS ';'
        { AstNode *n = ast_novo(AST_MOVE, linha_atual);
          n->u.move.alvo = $2; n->u.move.x = $5; n->u.move.y = $7;
          n->u.move.segundos = $10; $$ = n; }
  | QUADRO lista_cmds FIM
        { AstNode *n = ast_novo(AST_QUADRO, linha_atual);
          n->u.quadro.corpo = $2; $$ = n; }
  ;

expressao: expr_logica { $$ = $1; } ;

expr_logica:
    expr_logica OU expr_logica   { $$ = ast_binop(OP_OR, $1, $3, linha_atual); }
  | expr_logica E expr_logica    { $$ = ast_binop(OP_AND, $1, $3, linha_atual); }
  | NAO expr_logica              { $$ = ast_unop(OP_NOT, $2, linha_atual); }
  | expr_rel                     { $$ = $1; }
  ;

expr_rel:
    expr_rel EQ expr_rel   { $$ = ast_binop(OP_EQ, $1, $3, linha_atual); }
  | expr_rel NE expr_rel   { $$ = ast_binop(OP_NE, $1, $3, linha_atual); }
  | expr_rel LT expr_rel   { $$ = ast_binop(OP_LT, $1, $3, linha_atual); }
  | expr_rel GT expr_rel   { $$ = ast_binop(OP_GT, $1, $3, linha_atual); }
  | expr_rel LE expr_rel   { $$ = ast_binop(OP_LE, $1, $3, linha_atual); }
  | expr_rel GE expr_rel   { $$ = ast_binop(OP_GE, $1, $3, linha_atual); }
  | expr_arit              { $$ = $1; }
  ;

expr_arit:
    expr_arit '+' expr_termo   { $$ = ast_binop(OP_ADD, $1, $3, linha_atual); }
  | expr_arit '-' expr_termo   { $$ = ast_binop(OP_SUB, $1, $3, linha_atual); }
  | expr_termo                 { $$ = $1; }
  ;

expr_termo:
    expr_termo '*' expr_fator  { $$ = ast_binop(OP_MUL, $1, $3, linha_atual); }
  | expr_termo '/' expr_fator  { $$ = ast_binop(OP_DIV, $1, $3, linha_atual); }
  | expr_termo '%' expr_fator  { $$ = ast_binop(OP_MOD, $1, $3, linha_atual); }
  | expr_fator                 { $$ = $1; }
  ;

expr_fator:
    NUM                        { $$ = ast_num($1, linha_atual); }
  | IDENT                      { $$ = ast_ident($1, linha_atual); }
  | '(' expressao ')'          { $$ = $2; }
  | '-' expr_fator %prec NAO   { $$ = ast_unop(OP_NOT, $2, linha_atual); }  /* unário */
  ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro sintático (linha %d): %s\n", linha_atual, s);
    tem_erro = 1;
}