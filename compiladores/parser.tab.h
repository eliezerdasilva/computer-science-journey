/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_PARSER_TAB_H_INCLUDED
# define YY_YY_PARSER_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif
/* "%code requires" blocks.  */
#line 1 "parser.y"

#include "ast.h"

#line 53 "parser.tab.h"

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    TELA = 258,                    /* TELA  */
    PIXEL = 259,                   /* PIXEL  */
    LINHA = 260,                   /* LINHA  */
    RETANGULO = 261,               /* RETANGULO  */
    CIRCULO = 262,                 /* CIRCULO  */
    TEXTO = 263,                   /* TEXTO  */
    COR_FUNDO = 264,               /* COR_FUNDO  */
    ANIMA = 265,                   /* ANIMA  */
    SALVA = 266,                   /* SALVA  */
    VAR = 267,                     /* VAR  */
    SE = 268,                      /* SE  */
    SENAO = 269,                   /* SENAO  */
    FIM = 270,                     /* FIM  */
    REPETE = 271,                  /* REPETE  */
    VEZES = 272,                   /* VEZES  */
    MOVE = 273,                    /* MOVE  */
    PARA = 274,                    /* PARA  */
    EM = 275,                      /* EM  */
    SEGUNDOS = 276,                /* SEGUNDOS  */
    QUADRO = 277,                  /* QUADRO  */
    FPS = 278,                     /* FPS  */
    E = 279,                       /* E  */
    OU = 280,                      /* OU  */
    NAO = 281,                     /* NAO  */
    ATRIB = 282,                   /* ATRIB  */
    EQ = 283,                      /* EQ  */
    NE = 284,                      /* NE  */
    LT = 285,                      /* LT  */
    GT = 286,                      /* GT  */
    LE = 287,                      /* LE  */
    GE = 288,                      /* GE  */
    IDENT = 289,                   /* IDENT  */
    STRING = 290,                  /* STRING  */
    COR = 291,                     /* COR  */
    NUM = 292                      /* NUM  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 20 "parser.y"

    double num;
    char *str;
    AstNode *node;

#line 113 "parser.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_PARSER_TAB_H_INCLUDED  */
