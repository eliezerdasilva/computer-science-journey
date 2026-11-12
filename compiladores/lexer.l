%{
#include "parser.tab.h"
#include "ast.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int linha_atual = 1;
extern int yyparse(void);
void yyerror(const char *s);
%}

%option noyywrap
%option nounput
%option noinput
%option yylineno

DIGITO   [0-9]
HEX      [0-9A-Fa-f]
COR      #{HEX}{6}
ID       [a-zA-Z_][a-zA-Z0-9_]*

%%
[ \t\r]+            ;
\n                  { linha_atual++; }
"//".*              ;

"TELA"              { return TELA; }
"PIXEL"             { return PIXEL; }
"LINHA"             { return LINHA; }
"RETANGULO"         { return RETANGULO; }
"CIRCULO"           { return CIRCULO; }
"TEXTO"             { return TEXTO; }
"COR_FUNDO"         { return COR_FUNDO; }
"ANIMA"             { return ANIMA; }
"SALVA"             { return SALVA; }
"VAR"               { return VAR; }
"SE"                { return SE; }
"SENAO"             { return SENAO; }
"FIM"               { return FIM; }
"REPETE"            { return REPETE; }
"VEZES"             { return VEZES; }
"MOVE"              { return MOVE; }
"PARA"              { return PARA; }
"EM"                { return EM; }
"SEGUNDOS"          { return SEGUNDOS; }
"SEGUNDO"           { return SEGUNDOS; }
"QUADRO"            { return QUADRO; }
"FPS"               { return FPS; }
"E"                 { return E; }
"OU"                { return OU; }
"NAO"               { return NAO; }

{COR}               { yylval.str = strdup(yytext); return COR; }
{DIGITO}+("."{DIGITO}+)?  { yylval.num = atof(yytext); return NUM; }
\"([^\"\\]|\\.)*\"  { yylval.str = strdup(yytext+1); yylval.str[strlen(yylval.str)-1]='\0'; return STRING; }
{ID}                { yylval.str = strdup(yytext); return IDENT; }

"=="                { return EQ; }
"!="                { return NE; }
"<="                { return LE; }
">="                { return GE; }
"<"                 { return LT; }
">"                 { return GT; }
"="                 { return ATRIB; }
"+"                 { return '+'; }
"-"                 { return '-'; }
"*"                 { return '*'; }
"/"                 { return '/'; }
"%"                 { return '%'; }
","                 { return ','; }
";"                 { return ';'; }
"("                 { return '('; }
")"                 { return ')'; }
"{"                 { return '{'; }
"}"                 { return '}'; }

.                   { fprintf(stderr, "Caractere inválido: '%s' (linha %d)\n", yytext, yylineno); }

%%