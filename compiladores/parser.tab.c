/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison implementation for Yacc-like parsers in C

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

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output, and Bison version.  */
#define YYBISON 30802

/* Bison version string.  */
#define YYBISON_VERSION "3.8.2"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1




/* First part of user prologue.  */
#line 5 "parser.y"

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

#line 86 "parser.tab.c"

# ifndef YY_CAST
#  ifdef __cplusplus
#   define YY_CAST(Type, Val) static_cast<Type> (Val)
#   define YY_REINTERPRET_CAST(Type, Val) reinterpret_cast<Type> (Val)
#  else
#   define YY_CAST(Type, Val) ((Type) (Val))
#   define YY_REINTERPRET_CAST(Type, Val) ((Type) (Val))
#  endif
# endif
# ifndef YY_NULLPTR
#  if defined __cplusplus
#   if 201103L <= __cplusplus
#    define YY_NULLPTR nullptr
#   else
#    define YY_NULLPTR 0
#   endif
#  else
#   define YY_NULLPTR ((void*)0)
#  endif
# endif

#include "parser.tab.h"
/* Symbol kind.  */
enum yysymbol_kind_t
{
  YYSYMBOL_YYEMPTY = -2,
  YYSYMBOL_YYEOF = 0,                      /* "end of file"  */
  YYSYMBOL_YYerror = 1,                    /* error  */
  YYSYMBOL_YYUNDEF = 2,                    /* "invalid token"  */
  YYSYMBOL_TELA = 3,                       /* TELA  */
  YYSYMBOL_PIXEL = 4,                      /* PIXEL  */
  YYSYMBOL_LINHA = 5,                      /* LINHA  */
  YYSYMBOL_RETANGULO = 6,                  /* RETANGULO  */
  YYSYMBOL_CIRCULO = 7,                    /* CIRCULO  */
  YYSYMBOL_TEXTO = 8,                      /* TEXTO  */
  YYSYMBOL_COR_FUNDO = 9,                  /* COR_FUNDO  */
  YYSYMBOL_ANIMA = 10,                     /* ANIMA  */
  YYSYMBOL_SALVA = 11,                     /* SALVA  */
  YYSYMBOL_VAR = 12,                       /* VAR  */
  YYSYMBOL_SE = 13,                        /* SE  */
  YYSYMBOL_SENAO = 14,                     /* SENAO  */
  YYSYMBOL_FIM = 15,                       /* FIM  */
  YYSYMBOL_REPETE = 16,                    /* REPETE  */
  YYSYMBOL_VEZES = 17,                     /* VEZES  */
  YYSYMBOL_MOVE = 18,                      /* MOVE  */
  YYSYMBOL_PARA = 19,                      /* PARA  */
  YYSYMBOL_EM = 20,                        /* EM  */
  YYSYMBOL_SEGUNDOS = 21,                  /* SEGUNDOS  */
  YYSYMBOL_QUADRO = 22,                    /* QUADRO  */
  YYSYMBOL_FPS = 23,                       /* FPS  */
  YYSYMBOL_E = 24,                         /* E  */
  YYSYMBOL_OU = 25,                        /* OU  */
  YYSYMBOL_NAO = 26,                       /* NAO  */
  YYSYMBOL_ATRIB = 27,                     /* ATRIB  */
  YYSYMBOL_EQ = 28,                        /* EQ  */
  YYSYMBOL_NE = 29,                        /* NE  */
  YYSYMBOL_LT = 30,                        /* LT  */
  YYSYMBOL_GT = 31,                        /* GT  */
  YYSYMBOL_LE = 32,                        /* LE  */
  YYSYMBOL_GE = 33,                        /* GE  */
  YYSYMBOL_IDENT = 34,                     /* IDENT  */
  YYSYMBOL_STRING = 35,                    /* STRING  */
  YYSYMBOL_COR = 36,                       /* COR  */
  YYSYMBOL_NUM = 37,                       /* NUM  */
  YYSYMBOL_38_ = 38,                       /* '+'  */
  YYSYMBOL_39_ = 39,                       /* '-'  */
  YYSYMBOL_40_ = 40,                       /* '*'  */
  YYSYMBOL_41_ = 41,                       /* '/'  */
  YYSYMBOL_42_ = 42,                       /* '%'  */
  YYSYMBOL_43_ = 43,                       /* ';'  */
  YYSYMBOL_44_ = 44,                       /* ','  */
  YYSYMBOL_45_ = 45,                       /* '('  */
  YYSYMBOL_46_ = 46,                       /* ')'  */
  YYSYMBOL_YYACCEPT = 47,                  /* $accept  */
  YYSYMBOL_programa = 48,                  /* programa  */
  YYSYMBOL_lista_cmds = 49,                /* lista_cmds  */
  YYSYMBOL_cmd = 50,                       /* cmd  */
  YYSYMBOL_desenho = 51,                   /* desenho  */
  YYSYMBOL_controle = 52,                  /* controle  */
  YYSYMBOL_animacao = 53,                  /* animacao  */
  YYSYMBOL_expressao = 54,                 /* expressao  */
  YYSYMBOL_expr_logica = 55,               /* expr_logica  */
  YYSYMBOL_expr_rel = 56,                  /* expr_rel  */
  YYSYMBOL_expr_arit = 57,                 /* expr_arit  */
  YYSYMBOL_expr_termo = 58,                /* expr_termo  */
  YYSYMBOL_expr_fator = 59                 /* expr_fator  */
};
typedef enum yysymbol_kind_t yysymbol_kind_t;




#ifdef short
# undef short
#endif

/* On compilers that do not define __PTRDIFF_MAX__ etc., make sure
   <limits.h> and (if available) <stdint.h> are included
   so that the code can choose integer types of a good width.  */

#ifndef __PTRDIFF_MAX__
# include <limits.h> /* INFRINGES ON USER NAME SPACE */
# if defined __STDC_VERSION__ && 199901 <= __STDC_VERSION__
#  include <stdint.h> /* INFRINGES ON USER NAME SPACE */
#  define YY_STDINT_H
# endif
#endif

/* Narrow types that promote to a signed type and that can represent a
   signed or unsigned integer of at least N bits.  In tables they can
   save space and decrease cache pressure.  Promoting to a signed type
   helps avoid bugs in integer arithmetic.  */

#ifdef __INT_LEAST8_MAX__
typedef __INT_LEAST8_TYPE__ yytype_int8;
#elif defined YY_STDINT_H
typedef int_least8_t yytype_int8;
#else
typedef signed char yytype_int8;
#endif

#ifdef __INT_LEAST16_MAX__
typedef __INT_LEAST16_TYPE__ yytype_int16;
#elif defined YY_STDINT_H
typedef int_least16_t yytype_int16;
#else
typedef short yytype_int16;
#endif

/* Work around bug in HP-UX 11.23, which defines these macros
   incorrectly for preprocessor constants.  This workaround can likely
   be removed in 2023, as HPE has promised support for HP-UX 11.23
   (aka HP-UX 11i v2) only through the end of 2022; see Table 2 of
   <https://h20195.www2.hpe.com/V2/getpdf.aspx/4AA4-7673ENW.pdf>.  */
#ifdef __hpux
# undef UINT_LEAST8_MAX
# undef UINT_LEAST16_MAX
# define UINT_LEAST8_MAX 255
# define UINT_LEAST16_MAX 65535
#endif

#if defined __UINT_LEAST8_MAX__ && __UINT_LEAST8_MAX__ <= __INT_MAX__
typedef __UINT_LEAST8_TYPE__ yytype_uint8;
#elif (!defined __UINT_LEAST8_MAX__ && defined YY_STDINT_H \
       && UINT_LEAST8_MAX <= INT_MAX)
typedef uint_least8_t yytype_uint8;
#elif !defined __UINT_LEAST8_MAX__ && UCHAR_MAX <= INT_MAX
typedef unsigned char yytype_uint8;
#else
typedef short yytype_uint8;
#endif

#if defined __UINT_LEAST16_MAX__ && __UINT_LEAST16_MAX__ <= __INT_MAX__
typedef __UINT_LEAST16_TYPE__ yytype_uint16;
#elif (!defined __UINT_LEAST16_MAX__ && defined YY_STDINT_H \
       && UINT_LEAST16_MAX <= INT_MAX)
typedef uint_least16_t yytype_uint16;
#elif !defined __UINT_LEAST16_MAX__ && USHRT_MAX <= INT_MAX
typedef unsigned short yytype_uint16;
#else
typedef int yytype_uint16;
#endif

#ifndef YYPTRDIFF_T
# if defined __PTRDIFF_TYPE__ && defined __PTRDIFF_MAX__
#  define YYPTRDIFF_T __PTRDIFF_TYPE__
#  define YYPTRDIFF_MAXIMUM __PTRDIFF_MAX__
# elif defined PTRDIFF_MAX
#  ifndef ptrdiff_t
#   include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  endif
#  define YYPTRDIFF_T ptrdiff_t
#  define YYPTRDIFF_MAXIMUM PTRDIFF_MAX
# else
#  define YYPTRDIFF_T long
#  define YYPTRDIFF_MAXIMUM LONG_MAX
# endif
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif defined __STDC_VERSION__ && 199901 <= __STDC_VERSION__
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned
# endif
#endif

#define YYSIZE_MAXIMUM                                  \
  YY_CAST (YYPTRDIFF_T,                                 \
           (YYPTRDIFF_MAXIMUM < YY_CAST (YYSIZE_T, -1)  \
            ? YYPTRDIFF_MAXIMUM                         \
            : YY_CAST (YYSIZE_T, -1)))

#define YYSIZEOF(X) YY_CAST (YYPTRDIFF_T, sizeof (X))


/* Stored state numbers (used for stacks). */
typedef yytype_uint8 yy_state_t;

/* State numbers in computations.  */
typedef int yy_state_fast_t;

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(Msgid) dgettext ("bison-runtime", Msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(Msgid) Msgid
# endif
#endif


#ifndef YY_ATTRIBUTE_PURE
# if defined __GNUC__ && 2 < __GNUC__ + (96 <= __GNUC_MINOR__)
#  define YY_ATTRIBUTE_PURE __attribute__ ((__pure__))
# else
#  define YY_ATTRIBUTE_PURE
# endif
#endif

#ifndef YY_ATTRIBUTE_UNUSED
# if defined __GNUC__ && 2 < __GNUC__ + (7 <= __GNUC_MINOR__)
#  define YY_ATTRIBUTE_UNUSED __attribute__ ((__unused__))
# else
#  define YY_ATTRIBUTE_UNUSED
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YY_USE(E) ((void) (E))
#else
# define YY_USE(E) /* empty */
#endif

/* Suppress an incorrect diagnostic about yylval being uninitialized.  */
#if defined __GNUC__ && ! defined __ICC && 406 <= __GNUC__ * 100 + __GNUC_MINOR__
# if __GNUC__ * 100 + __GNUC_MINOR__ < 407
#  define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN                           \
    _Pragma ("GCC diagnostic push")                                     \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")
# else
#  define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN                           \
    _Pragma ("GCC diagnostic push")                                     \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")              \
    _Pragma ("GCC diagnostic ignored \"-Wmaybe-uninitialized\"")
# endif
# define YY_IGNORE_MAYBE_UNINITIALIZED_END      \
    _Pragma ("GCC diagnostic pop")
#else
# define YY_INITIAL_VALUE(Value) Value
#endif
#ifndef YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_END
#endif
#ifndef YY_INITIAL_VALUE
# define YY_INITIAL_VALUE(Value) /* Nothing. */
#endif

#if defined __cplusplus && defined __GNUC__ && ! defined __ICC && 6 <= __GNUC__
# define YY_IGNORE_USELESS_CAST_BEGIN                          \
    _Pragma ("GCC diagnostic push")                            \
    _Pragma ("GCC diagnostic ignored \"-Wuseless-cast\"")
# define YY_IGNORE_USELESS_CAST_END            \
    _Pragma ("GCC diagnostic pop")
#endif
#ifndef YY_IGNORE_USELESS_CAST_BEGIN
# define YY_IGNORE_USELESS_CAST_BEGIN
# define YY_IGNORE_USELESS_CAST_END
#endif


#define YY_ASSERT(E) ((void) (0 && (E)))

#if !defined yyoverflow

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined EXIT_SUCCESS
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
      /* Use EXIT_SUCCESS as a witness for stdlib.h.  */
#     ifndef EXIT_SUCCESS
#      define EXIT_SUCCESS 0
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's 'empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (0)
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined EXIT_SUCCESS \
       && ! ((defined YYMALLOC || defined malloc) \
             && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef EXIT_SUCCESS
#    define EXIT_SUCCESS 0
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined EXIT_SUCCESS
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined EXIT_SUCCESS
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* !defined yyoverflow */

#if (! defined yyoverflow \
     && (! defined __cplusplus \
         || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yy_state_t yyss_alloc;
  YYSTYPE yyvs_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (YYSIZEOF (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (YYSIZEOF (yy_state_t) + YYSIZEOF (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

# define YYCOPY_NEEDED 1

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)                           \
    do                                                                  \
      {                                                                 \
        YYPTRDIFF_T yynewbytes;                                         \
        YYCOPY (&yyptr->Stack_alloc, Stack, yysize);                    \
        Stack = &yyptr->Stack_alloc;                                    \
        yynewbytes = yystacksize * YYSIZEOF (*Stack) + YYSTACK_GAP_MAXIMUM; \
        yyptr += yynewbytes / YYSIZEOF (*yyptr);                        \
      }                                                                 \
    while (0)

#endif

#if defined YYCOPY_NEEDED && YYCOPY_NEEDED
/* Copy COUNT objects from SRC to DST.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(Dst, Src, Count) \
      __builtin_memcpy (Dst, Src, YY_CAST (YYSIZE_T, (Count)) * sizeof (*(Src)))
#  else
#   define YYCOPY(Dst, Src, Count)              \
      do                                        \
        {                                       \
          YYPTRDIFF_T yyi;                      \
          for (yyi = 0; yyi < (Count); yyi++)   \
            (Dst)[yyi] = (Src)[yyi];            \
        }                                       \
      while (0)
#  endif
# endif
#endif /* !YYCOPY_NEEDED */

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  3
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   222

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  47
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  13
/* YYNRULES -- Number of rules.  */
#define YYNRULES  46
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  141

/* YYMAXUTOK -- Last valid token kind.  */
#define YYMAXUTOK   292


/* YYTRANSLATE(TOKEN-NUM) -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex, with out-of-bounds checking.  */
#define YYTRANSLATE(YYX)                                \
  (0 <= (YYX) && (YYX) <= YYMAXUTOK                     \
   ? YY_CAST (yysymbol_kind_t, yytranslate[YYX])        \
   : YYSYMBOL_YYUNDEF)

/* YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex.  */
static const yytype_int8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,    42,     2,     2,
      45,    46,    40,    38,    44,    39,     2,    41,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,    43,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37
};

#if YYDEBUG
/* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_uint8 yyrline[] =
{
       0,    45,    45,    50,    51,    55,    56,    57,    58,    60,
      65,    68,    71,    75,    79,    83,    87,    90,    96,    99,
     102,   108,   110,   114,   119,   122,   123,   124,   125,   129,
     130,   131,   132,   133,   134,   135,   139,   140,   141,   145,
     146,   147,   148,   152,   153,   154,   155
};
#endif

/** Accessing symbol of state STATE.  */
#define YY_ACCESSING_SYMBOL(State) YY_CAST (yysymbol_kind_t, yystos[State])

#if YYDEBUG || 0
/* The user-facing name of the symbol whose (internal) number is
   YYSYMBOL.  No bounds checking.  */
static const char *yysymbol_name (yysymbol_kind_t yysymbol) YY_ATTRIBUTE_UNUSED;

/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "\"end of file\"", "error", "\"invalid token\"", "TELA", "PIXEL",
  "LINHA", "RETANGULO", "CIRCULO", "TEXTO", "COR_FUNDO", "ANIMA", "SALVA",
  "VAR", "SE", "SENAO", "FIM", "REPETE", "VEZES", "MOVE", "PARA", "EM",
  "SEGUNDOS", "QUADRO", "FPS", "E", "OU", "NAO", "ATRIB", "EQ", "NE", "LT",
  "GT", "LE", "GE", "IDENT", "STRING", "COR", "NUM", "'+'", "'-'", "'*'",
  "'/'", "'%'", "';'", "','", "'('", "')'", "$accept", "programa",
  "lista_cmds", "cmd", "desenho", "controle", "animacao", "expressao",
  "expr_logica", "expr_rel", "expr_arit", "expr_termo", "expr_fator", YY_NULLPTR
};

static const char *
yysymbol_name (yysymbol_kind_t yysymbol)
{
  return yytname[yysymbol];
}
#endif

#define YYPACT_NINF (-24)

#define yypact_value_is_default(Yyn) \
  ((Yyn) == YYPACT_NINF)

#define YYTABLE_NINF (-1)

#define yytable_value_is_error(Yyn) \
  ((Yyn) == YYTABLE_NINF)

/* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
   STATE-NUM.  */
static const yytype_int16 yypact[] =
{
     -24,    14,   188,   -24,   -21,   -21,   -21,   -21,   -21,   -16,
       0,    17,     6,    12,   -21,   -21,    26,   -24,    39,   -24,
      40,   -24,   -24,   -21,   -24,   -24,   -22,   -21,    41,   -17,
      -3,   -18,    -9,   -24,    42,    43,    45,    46,    71,   -24,
      55,   -24,    68,   -24,    76,    77,   128,   -21,   -24,   -24,
     -24,    51,   -21,   -21,   -21,   -22,   -22,   -22,   -22,   -22,
     -22,   -22,   -22,   -22,   -22,   -22,   -21,   -21,   -21,   -21,
     -21,    56,   -21,    66,   -24,    61,   -24,    58,   -24,    63,
     -24,    84,    20,    20,    20,    20,    20,    20,    -9,    -9,
     -24,   -24,   -24,    65,    67,    69,    70,    72,   -24,    78,
     -24,   -24,   148,   -21,   -24,    74,    79,   -21,   -21,   -21,
     -21,   -24,   168,   -24,    80,   -24,   -24,    81,    82,    83,
      85,   -24,   -21,   -21,   -21,    86,    87,    96,   101,   103,
     -24,   -24,    92,   112,   113,   -21,   -24,   -24,    99,   122,
     -24
};

/* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
   Performed when YYTABLE does not specify something else to do.  Zero
   means the default is an error.  */
static const yytype_int8 yydefact[] =
{
       3,     0,     2,     1,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     3,     0,     4,
       0,     6,     7,     0,    44,    43,     0,     0,     0,    24,
      28,    35,    38,    42,     0,     0,     0,     0,     0,    16,
       0,    17,     0,     3,     0,     0,     0,     0,     5,    27,
      46,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     3,     0,    23,     0,    45,     0,
      26,    25,    29,    30,    31,    32,    33,    34,    36,    37,
      39,    40,    41,     0,     0,     0,     0,     0,    21,     0,
       3,    18,     0,     0,     9,     0,     0,     0,     0,     0,
       0,     8,     0,    20,     0,    10,    11,     0,     0,     0,
       0,    19,     0,     0,     0,     0,     0,     0,     0,     0,
      14,    15,     0,     0,     0,     0,    12,    13,     0,     0,
      22
};

/* YYPGOTO[NTERM-NUM].  */
static const yytype_int8 yypgoto[] =
{
     -24,   -24,    -6,   -24,   -24,   -24,   -24,    -5,   -19,    -1,
     -24,   -23,   -20
};

/* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int8 yydefgoto[] =
{
       0,     1,     2,    19,    20,    21,    22,    28,    29,    30,
      31,    32,    33
};

/* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
   positive, shift that token.  If negative, reduce the rule whose
   number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_int16 yytable[] =
{
      34,    35,    36,    37,    49,    23,    50,    53,    54,    43,
      44,    46,    24,    24,     3,    25,    25,    26,    26,    38,
      61,    62,    51,    27,    27,    55,    56,    57,    58,    59,
      60,    63,    64,    65,    80,    81,    39,    73,    88,    89,
      40,    41,    77,    90,    91,    92,    42,    79,    -1,    -1,
      -1,    -1,    -1,    -1,    82,    83,    84,    85,    86,    87,
      45,    93,    94,    95,    96,    97,    47,    99,   102,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
     100,   101,    15,    48,    16,    52,    66,    67,    17,    68,
      69,    70,    71,    74,   112,    72,    75,    78,   114,    98,
      18,   104,   117,   118,   119,   120,   103,   105,    53,   106,
     115,   107,   135,   108,   109,   116,   110,   127,   128,   129,
     139,   111,   130,   131,   122,   123,   124,   125,     0,   126,
     138,     4,     5,     6,     7,     8,     9,    10,    11,    12,
      13,    14,   132,    76,    15,   133,    16,   134,   136,   137,
      17,     4,     5,     6,     7,     8,     9,    10,    11,    12,
      13,    14,    18,   113,    15,   140,    16,     0,     0,     0,
      17,     4,     5,     6,     7,     8,     9,    10,    11,    12,
      13,    14,    18,   121,    15,     0,    16,     0,     0,     0,
      17,     4,     5,     6,     7,     8,     9,    10,    11,    12,
      13,    14,    18,     0,    15,     0,    16,     0,     0,     0,
      17,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,    18
};

static const yytype_int16 yycheck[] =
{
       5,     6,     7,     8,    23,    26,    26,    24,    25,    14,
      15,    17,    34,    34,     0,    37,    37,    39,    39,    35,
      38,    39,    27,    45,    45,    28,    29,    30,    31,    32,
      33,    40,    41,    42,    53,    54,    36,    43,    61,    62,
      23,    35,    47,    63,    64,    65,    34,    52,    28,    29,
      30,    31,    32,    33,    55,    56,    57,    58,    59,    60,
      34,    66,    67,    68,    69,    70,    27,    72,    74,     3,
       4,     5,     6,     7,     8,     9,    10,    11,    12,    13,
      14,    15,    16,    43,    18,    44,    44,    44,    22,    44,
      44,    20,    37,    17,   100,    27,    19,    46,   103,    43,
      34,    43,   107,   108,   109,   110,    45,    44,    24,    44,
      36,    44,    20,    44,    44,    36,    44,   122,   123,   124,
      21,    43,    36,    36,    44,    44,    44,    44,    -1,    44,
     135,     3,     4,     5,     6,     7,     8,     9,    10,    11,
      12,    13,    46,    15,    16,    44,    18,    44,    36,    36,
      22,     3,     4,     5,     6,     7,     8,     9,    10,    11,
      12,    13,    34,    15,    16,    43,    18,    -1,    -1,    -1,
      22,     3,     4,     5,     6,     7,     8,     9,    10,    11,
      12,    13,    34,    15,    16,    -1,    18,    -1,    -1,    -1,
      22,     3,     4,     5,     6,     7,     8,     9,    10,    11,
      12,    13,    34,    -1,    16,    -1,    18,    -1,    -1,    -1,
      22,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    34
};

/* YYSTOS[STATE-NUM] -- The symbol kind of the accessing symbol of
   state STATE-NUM.  */
static const yytype_int8 yystos[] =
{
       0,    48,    49,     0,     3,     4,     5,     6,     7,     8,
       9,    10,    11,    12,    13,    16,    18,    22,    34,    50,
      51,    52,    53,    26,    34,    37,    39,    45,    54,    55,
      56,    57,    58,    59,    54,    54,    54,    54,    35,    36,
      23,    35,    34,    54,    54,    34,    49,    27,    43,    55,
      59,    54,    44,    24,    25,    28,    29,    30,    31,    32,
      33,    38,    39,    40,    41,    42,    44,    44,    44,    44,
      20,    37,    27,    49,    17,    19,    15,    54,    46,    54,
      55,    55,    56,    56,    56,    56,    56,    56,    58,    58,
      59,    59,    59,    54,    54,    54,    54,    54,    43,    54,
      14,    15,    49,    45,    43,    44,    44,    44,    44,    44,
      44,    43,    49,    15,    54,    36,    36,    54,    54,    54,
      54,    15,    44,    44,    44,    44,    44,    54,    54,    54,
      36,    36,    46,    44,    44,    20,    36,    36,    54,    21,
      43
};

/* YYR1[RULE-NUM] -- Symbol kind of the left-hand side of rule RULE-NUM.  */
static const yytype_int8 yyr1[] =
{
       0,    47,    48,    49,    49,    50,    50,    50,    50,    50,
      51,    51,    51,    51,    51,    51,    51,    51,    52,    52,
      52,    53,    53,    53,    54,    55,    55,    55,    55,    56,
      56,    56,    56,    56,    56,    56,    57,    57,    57,    58,
      58,    58,    58,    59,    59,    59,    59
};

/* YYR2[RULE-NUM] -- Number of symbols on the right-hand side of rule RULE-NUM.  */
static const yytype_int8 yyr2[] =
{
       0,     2,     1,     0,     2,     2,     1,     1,     5,     4,
       6,     6,    10,    10,     8,     8,     2,     2,     4,     6,
       5,     4,    12,     3,     1,     3,     3,     2,     1,     3,
       3,     3,     3,     3,     3,     1,     3,     3,     1,     3,
       3,     3,     1,     1,     1,     3,     2
};


enum { YYENOMEM = -2 };

#define yyerrok         (yyerrstatus = 0)
#define yyclearin       (yychar = YYEMPTY)

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYNOMEM         goto yyexhaustedlab


#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)                                    \
  do                                                              \
    if (yychar == YYEMPTY)                                        \
      {                                                           \
        yychar = (Token);                                         \
        yylval = (Value);                                         \
        YYPOPSTACK (yylen);                                       \
        yystate = *yyssp;                                         \
        goto yybackup;                                            \
      }                                                           \
    else                                                          \
      {                                                           \
        yyerror (YY_("syntax error: cannot back up")); \
        YYERROR;                                                  \
      }                                                           \
  while (0)

/* Backward compatibility with an undocumented macro.
   Use YYerror or YYUNDEF. */
#define YYERRCODE YYUNDEF


/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)                        \
do {                                            \
  if (yydebug)                                  \
    YYFPRINTF Args;                             \
} while (0)




# define YY_SYMBOL_PRINT(Title, Kind, Value, Location)                    \
do {                                                                      \
  if (yydebug)                                                            \
    {                                                                     \
      YYFPRINTF (stderr, "%s ", Title);                                   \
      yy_symbol_print (stderr,                                            \
                  Kind, Value); \
      YYFPRINTF (stderr, "\n");                                           \
    }                                                                     \
} while (0)


/*-----------------------------------.
| Print this symbol's value on YYO.  |
`-----------------------------------*/

static void
yy_symbol_value_print (FILE *yyo,
                       yysymbol_kind_t yykind, YYSTYPE const * const yyvaluep)
{
  FILE *yyoutput = yyo;
  YY_USE (yyoutput);
  if (!yyvaluep)
    return;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YY_USE (yykind);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}


/*---------------------------.
| Print this symbol on YYO.  |
`---------------------------*/

static void
yy_symbol_print (FILE *yyo,
                 yysymbol_kind_t yykind, YYSTYPE const * const yyvaluep)
{
  YYFPRINTF (yyo, "%s %s (",
             yykind < YYNTOKENS ? "token" : "nterm", yysymbol_name (yykind));

  yy_symbol_value_print (yyo, yykind, yyvaluep);
  YYFPRINTF (yyo, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

static void
yy_stack_print (yy_state_t *yybottom, yy_state_t *yytop)
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)                            \
do {                                                            \
  if (yydebug)                                                  \
    yy_stack_print ((Bottom), (Top));                           \
} while (0)


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

static void
yy_reduce_print (yy_state_t *yyssp, YYSTYPE *yyvsp,
                 int yyrule)
{
  int yylno = yyrline[yyrule];
  int yynrhs = yyr2[yyrule];
  int yyi;
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %d):\n",
             yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr,
                       YY_ACCESSING_SYMBOL (+yyssp[yyi + 1 - yynrhs]),
                       &yyvsp[(yyi + 1) - (yynrhs)]);
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)          \
do {                                    \
  if (yydebug)                          \
    yy_reduce_print (yyssp, yyvsp, Rule); \
} while (0)

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args) ((void) 0)
# define YY_SYMBOL_PRINT(Title, Kind, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif






/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

static void
yydestruct (const char *yymsg,
            yysymbol_kind_t yykind, YYSTYPE *yyvaluep)
{
  YY_USE (yyvaluep);
  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yykind, yyvaluep, yylocationp);

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YY_USE (yykind);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}


/* Lookahead token kind.  */
int yychar;

/* The semantic value of the lookahead symbol.  */
YYSTYPE yylval;
/* Number of syntax errors so far.  */
int yynerrs;




/*----------.
| yyparse.  |
`----------*/

int
yyparse (void)
{
    yy_state_fast_t yystate = 0;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus = 0;

    /* Refer to the stacks through separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* Their size.  */
    YYPTRDIFF_T yystacksize = YYINITDEPTH;

    /* The state stack: array, bottom, top.  */
    yy_state_t yyssa[YYINITDEPTH];
    yy_state_t *yyss = yyssa;
    yy_state_t *yyssp = yyss;

    /* The semantic value stack: array, bottom, top.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs = yyvsa;
    YYSTYPE *yyvsp = yyvs;

  int yyn;
  /* The return value of yyparse.  */
  int yyresult;
  /* Lookahead symbol kind.  */
  yysymbol_kind_t yytoken = YYSYMBOL_YYEMPTY;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;



#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yychar = YYEMPTY; /* Cause a token to be read.  */

  goto yysetstate;


/*------------------------------------------------------------.
| yynewstate -- push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;


/*--------------------------------------------------------------------.
| yysetstate -- set current state (the top of the stack) to yystate.  |
`--------------------------------------------------------------------*/
yysetstate:
  YYDPRINTF ((stderr, "Entering state %d\n", yystate));
  YY_ASSERT (0 <= yystate && yystate < YYNSTATES);
  YY_IGNORE_USELESS_CAST_BEGIN
  *yyssp = YY_CAST (yy_state_t, yystate);
  YY_IGNORE_USELESS_CAST_END
  YY_STACK_PRINT (yyss, yyssp);

  if (yyss + yystacksize - 1 <= yyssp)
#if !defined yyoverflow && !defined YYSTACK_RELOCATE
    YYNOMEM;
#else
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYPTRDIFF_T yysize = yyssp - yyss + 1;

# if defined yyoverflow
      {
        /* Give user a chance to reallocate the stack.  Use copies of
           these so that the &'s don't force the real ones into
           memory.  */
        yy_state_t *yyss1 = yyss;
        YYSTYPE *yyvs1 = yyvs;

        /* Each stack pointer address is followed by the size of the
           data in use in that stack, in bytes.  This used to be a
           conditional around just the two extra args, but that might
           be undefined if yyoverflow is a macro.  */
        yyoverflow (YY_("memory exhausted"),
                    &yyss1, yysize * YYSIZEOF (*yyssp),
                    &yyvs1, yysize * YYSIZEOF (*yyvsp),
                    &yystacksize);
        yyss = yyss1;
        yyvs = yyvs1;
      }
# else /* defined YYSTACK_RELOCATE */
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
        YYNOMEM;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
        yystacksize = YYMAXDEPTH;

      {
        yy_state_t *yyss1 = yyss;
        union yyalloc *yyptr =
          YY_CAST (union yyalloc *,
                   YYSTACK_ALLOC (YY_CAST (YYSIZE_T, YYSTACK_BYTES (yystacksize))));
        if (! yyptr)
          YYNOMEM;
        YYSTACK_RELOCATE (yyss_alloc, yyss);
        YYSTACK_RELOCATE (yyvs_alloc, yyvs);
#  undef YYSTACK_RELOCATE
        if (yyss1 != yyssa)
          YYSTACK_FREE (yyss1);
      }
# endif

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;

      YY_IGNORE_USELESS_CAST_BEGIN
      YYDPRINTF ((stderr, "Stack size increased to %ld\n",
                  YY_CAST (long, yystacksize)));
      YY_IGNORE_USELESS_CAST_END

      if (yyss + yystacksize - 1 <= yyssp)
        YYABORT;
    }
#endif /* !defined yyoverflow && !defined YYSTACK_RELOCATE */


  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;


/*-----------.
| yybackup.  |
`-----------*/
yybackup:
  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yypact_value_is_default (yyn))
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either empty, or end-of-input, or a valid lookahead.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token\n"));
      yychar = yylex ();
    }

  if (yychar <= YYEOF)
    {
      yychar = YYEOF;
      yytoken = YYSYMBOL_YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else if (yychar == YYerror)
    {
      /* The scanner already issued an error message, process directly
         to error recovery.  But do not keep the error token as
         lookahead, it is too special and may lead us to an endless
         loop in error recovery. */
      yychar = YYUNDEF;
      yytoken = YYSYMBOL_YYerror;
      goto yyerrlab1;
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yytable_value_is_error (yyn))
        goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);
  yystate = yyn;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END

  /* Discard the shifted token.  */
  yychar = YYEMPTY;
  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     '$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
  case 2: /* programa: lista_cmds  */
#line 45 "parser.y"
                            { raiz = ast_novo(AST_PROGRAMA, 1); raiz->u.programa.n = (yyvsp[0].node)->u.bloco.n;
                              memcpy(raiz->u.programa.itens, (yyvsp[0].node)->u.bloco.itens, sizeof(AstNode*)*(yyvsp[0].node)->u.bloco.n); (yyval.node) = raiz; }
#line 1229 "parser.tab.c"
    break;

  case 3: /* lista_cmds: %empty  */
#line 50 "parser.y"
                            { (yyval.node) = ast_novo(AST_BLOCO, 0); }
#line 1235 "parser.tab.c"
    break;

  case 4: /* lista_cmds: lista_cmds cmd  */
#line 51 "parser.y"
                            { AstNode *b = (yyvsp[-1].node); b->u.bloco.itens[b->u.bloco.n++] = (yyvsp[0].node); (yyval.node) = b; }
#line 1241 "parser.tab.c"
    break;

  case 5: /* cmd: desenho ';'  */
#line 55 "parser.y"
                            { (yyval.node) = (yyvsp[-1].node); }
#line 1247 "parser.tab.c"
    break;

  case 6: /* cmd: controle  */
#line 56 "parser.y"
                            { (yyval.node) = (yyvsp[0].node); }
#line 1253 "parser.tab.c"
    break;

  case 7: /* cmd: animacao  */
#line 57 "parser.y"
                            { (yyval.node) = (yyvsp[0].node); }
#line 1259 "parser.tab.c"
    break;

  case 8: /* cmd: VAR IDENT ATRIB expressao ';'  */
#line 58 "parser.y"
                                    { AstNode *n = ast_novo(AST_VAR, linha_atual);
                                       n->u.var.nome = (yyvsp[-3].str); n->u.var.expr = (yyvsp[-1].node); (yyval.node) = n; }
#line 1266 "parser.tab.c"
    break;

  case 9: /* cmd: IDENT ATRIB expressao ';'  */
#line 60 "parser.y"
                                    { AstNode *n = ast_novo(AST_ATRIBUICAO, linha_atual);
                                       n->u.atrib.nome = (yyvsp[-3].str); n->u.atrib.expr = (yyvsp[-1].node); (yyval.node) = n; }
#line 1273 "parser.tab.c"
    break;

  case 10: /* desenho: TELA expressao ',' expressao ',' COR  */
#line 66 "parser.y"
        { AstNode *n = ast_novo(AST_TELA, linha_atual);
          n->u.tela.w = (yyvsp[-4].node); n->u.tela.h = (yyvsp[-2].node); n->u.tela.cor = ast_cor((yyvsp[0].str), linha_atual); (yyval.node) = n; }
#line 1280 "parser.tab.c"
    break;

  case 11: /* desenho: PIXEL expressao ',' expressao ',' COR  */
#line 69 "parser.y"
        { AstNode *n = ast_novo(AST_PIXEL, linha_atual);
          n->u.pixel.x = (yyvsp[-4].node); n->u.pixel.y = (yyvsp[-2].node); n->u.pixel.cor = ast_cor((yyvsp[0].str), linha_atual); (yyval.node) = n; }
#line 1287 "parser.tab.c"
    break;

  case 12: /* desenho: LINHA expressao ',' expressao ',' expressao ',' expressao ',' COR  */
#line 72 "parser.y"
        { AstNode *n = ast_novo(AST_LINHA, linha_atual);
          n->u.linha.x1=(yyvsp[-8].node); n->u.linha.y1=(yyvsp[-6].node); n->u.linha.x2=(yyvsp[-4].node); n->u.linha.y2=(yyvsp[-2].node);
          n->u.linha.cor = ast_cor((yyvsp[0].str), linha_atual); (yyval.node) = n; }
#line 1295 "parser.tab.c"
    break;

  case 13: /* desenho: RETANGULO expressao ',' expressao ',' expressao ',' expressao ',' COR  */
#line 76 "parser.y"
        { AstNode *n = ast_novo(AST_RETANGULO, linha_atual);
          n->u.retangulo.x=(yyvsp[-8].node); n->u.retangulo.y=(yyvsp[-6].node); n->u.retangulo.w=(yyvsp[-4].node); n->u.retangulo.h=(yyvsp[-2].node);
          n->u.retangulo.cor = ast_cor((yyvsp[0].str), linha_atual); (yyval.node) = n; }
#line 1303 "parser.tab.c"
    break;

  case 14: /* desenho: CIRCULO expressao ',' expressao ',' expressao ',' COR  */
#line 80 "parser.y"
        { AstNode *n = ast_novo(AST_CIRCULO, linha_atual);
          n->u.circulo.cx=(yyvsp[-6].node); n->u.circulo.cy=(yyvsp[-4].node); n->u.circulo.r=(yyvsp[-2].node);
          n->u.circulo.cor = ast_cor((yyvsp[0].str), linha_atual); (yyval.node) = n; }
#line 1311 "parser.tab.c"
    break;

  case 15: /* desenho: TEXTO STRING EM expressao ',' expressao ',' COR  */
#line 84 "parser.y"
        { AstNode *n = ast_novo(AST_TEXTO, linha_atual);
          n->u.texto.texto = (yyvsp[-6].str); n->u.texto.x = (yyvsp[-4].node); n->u.texto.y = (yyvsp[-2].node);
          n->u.texto.cor = ast_cor((yyvsp[0].str), linha_atual); (yyval.node) = n; }
#line 1319 "parser.tab.c"
    break;

  case 16: /* desenho: COR_FUNDO COR  */
#line 88 "parser.y"
        { AstNode *n = ast_novo(AST_COR_FUNDO, linha_atual);
          n->u.cor_fundo.cor = ast_cor((yyvsp[0].str), linha_atual); (yyval.node) = n; }
#line 1326 "parser.tab.c"
    break;

  case 17: /* desenho: SALVA STRING  */
#line 91 "parser.y"
    { AstNode *n = ast_novo(AST_SALVA, linha_atual);
      n->u.salva.arquivo = (yyvsp[0].str); (yyval.node) = n; }
#line 1333 "parser.tab.c"
    break;

  case 18: /* controle: SE expressao lista_cmds FIM  */
#line 97 "parser.y"
        { AstNode *n = ast_novo(AST_SE, linha_atual);
          n->u.se.cond = (yyvsp[-2].node); n->u.se.entao = (yyvsp[-1].node); n->u.se.senao = NULL; (yyval.node) = n; }
#line 1340 "parser.tab.c"
    break;

  case 19: /* controle: SE expressao lista_cmds SENAO lista_cmds FIM  */
#line 100 "parser.y"
        { AstNode *n = ast_novo(AST_SE, linha_atual);
          n->u.se.cond = (yyvsp[-4].node); n->u.se.entao = (yyvsp[-3].node); n->u.se.senao = (yyvsp[-1].node); (yyval.node) = n; }
#line 1347 "parser.tab.c"
    break;

  case 20: /* controle: REPETE expressao VEZES lista_cmds FIM  */
#line 103 "parser.y"
        { AstNode *n = ast_novo(AST_REPETE, linha_atual);
          n->u.repete.vezes = (yyvsp[-3].node); n->u.repete.corpo = (yyvsp[-1].node); (yyval.node) = n; }
#line 1354 "parser.tab.c"
    break;

  case 21: /* animacao: ANIMA FPS NUM ';'  */
#line 109 "parser.y"
        { AstNode *n = ast_novo(AST_ANIMA, linha_atual); n->u.anima.fps = (int)(yyvsp[-1].num); (yyval.node) = n; }
#line 1360 "parser.tab.c"
    break;

  case 22: /* animacao: MOVE IDENT PARA '(' expressao ',' expressao ')' EM expressao SEGUNDOS ';'  */
#line 111 "parser.y"
        { AstNode *n = ast_novo(AST_MOVE, linha_atual);
          n->u.move.alvo = (yyvsp[-10].str); n->u.move.x = (yyvsp[-7].node); n->u.move.y = (yyvsp[-5].node);
          n->u.move.segundos = (yyvsp[-2].node); (yyval.node) = n; }
#line 1368 "parser.tab.c"
    break;

  case 23: /* animacao: QUADRO lista_cmds FIM  */
#line 115 "parser.y"
        { AstNode *n = ast_novo(AST_QUADRO, linha_atual);
          n->u.quadro.corpo = (yyvsp[-1].node); (yyval.node) = n; }
#line 1375 "parser.tab.c"
    break;

  case 24: /* expressao: expr_logica  */
#line 119 "parser.y"
                       { (yyval.node) = (yyvsp[0].node); }
#line 1381 "parser.tab.c"
    break;

  case 25: /* expr_logica: expr_logica OU expr_logica  */
#line 122 "parser.y"
                                 { (yyval.node) = ast_binop(OP_OR, (yyvsp[-2].node), (yyvsp[0].node), linha_atual); }
#line 1387 "parser.tab.c"
    break;

  case 26: /* expr_logica: expr_logica E expr_logica  */
#line 123 "parser.y"
                                 { (yyval.node) = ast_binop(OP_AND, (yyvsp[-2].node), (yyvsp[0].node), linha_atual); }
#line 1393 "parser.tab.c"
    break;

  case 27: /* expr_logica: NAO expr_logica  */
#line 124 "parser.y"
                                 { (yyval.node) = ast_unop(OP_NOT, (yyvsp[0].node), linha_atual); }
#line 1399 "parser.tab.c"
    break;

  case 28: /* expr_logica: expr_rel  */
#line 125 "parser.y"
                                 { (yyval.node) = (yyvsp[0].node); }
#line 1405 "parser.tab.c"
    break;

  case 29: /* expr_rel: expr_rel EQ expr_rel  */
#line 129 "parser.y"
                           { (yyval.node) = ast_binop(OP_EQ, (yyvsp[-2].node), (yyvsp[0].node), linha_atual); }
#line 1411 "parser.tab.c"
    break;

  case 30: /* expr_rel: expr_rel NE expr_rel  */
#line 130 "parser.y"
                           { (yyval.node) = ast_binop(OP_NE, (yyvsp[-2].node), (yyvsp[0].node), linha_atual); }
#line 1417 "parser.tab.c"
    break;

  case 31: /* expr_rel: expr_rel LT expr_rel  */
#line 131 "parser.y"
                           { (yyval.node) = ast_binop(OP_LT, (yyvsp[-2].node), (yyvsp[0].node), linha_atual); }
#line 1423 "parser.tab.c"
    break;

  case 32: /* expr_rel: expr_rel GT expr_rel  */
#line 132 "parser.y"
                           { (yyval.node) = ast_binop(OP_GT, (yyvsp[-2].node), (yyvsp[0].node), linha_atual); }
#line 1429 "parser.tab.c"
    break;

  case 33: /* expr_rel: expr_rel LE expr_rel  */
#line 133 "parser.y"
                           { (yyval.node) = ast_binop(OP_LE, (yyvsp[-2].node), (yyvsp[0].node), linha_atual); }
#line 1435 "parser.tab.c"
    break;

  case 34: /* expr_rel: expr_rel GE expr_rel  */
#line 134 "parser.y"
                           { (yyval.node) = ast_binop(OP_GE, (yyvsp[-2].node), (yyvsp[0].node), linha_atual); }
#line 1441 "parser.tab.c"
    break;

  case 35: /* expr_rel: expr_arit  */
#line 135 "parser.y"
                           { (yyval.node) = (yyvsp[0].node); }
#line 1447 "parser.tab.c"
    break;

  case 36: /* expr_arit: expr_arit '+' expr_termo  */
#line 139 "parser.y"
                               { (yyval.node) = ast_binop(OP_ADD, (yyvsp[-2].node), (yyvsp[0].node), linha_atual); }
#line 1453 "parser.tab.c"
    break;

  case 37: /* expr_arit: expr_arit '-' expr_termo  */
#line 140 "parser.y"
                               { (yyval.node) = ast_binop(OP_SUB, (yyvsp[-2].node), (yyvsp[0].node), linha_atual); }
#line 1459 "parser.tab.c"
    break;

  case 38: /* expr_arit: expr_termo  */
#line 141 "parser.y"
                               { (yyval.node) = (yyvsp[0].node); }
#line 1465 "parser.tab.c"
    break;

  case 39: /* expr_termo: expr_termo '*' expr_fator  */
#line 145 "parser.y"
                               { (yyval.node) = ast_binop(OP_MUL, (yyvsp[-2].node), (yyvsp[0].node), linha_atual); }
#line 1471 "parser.tab.c"
    break;

  case 40: /* expr_termo: expr_termo '/' expr_fator  */
#line 146 "parser.y"
                               { (yyval.node) = ast_binop(OP_DIV, (yyvsp[-2].node), (yyvsp[0].node), linha_atual); }
#line 1477 "parser.tab.c"
    break;

  case 41: /* expr_termo: expr_termo '%' expr_fator  */
#line 147 "parser.y"
                               { (yyval.node) = ast_binop(OP_MOD, (yyvsp[-2].node), (yyvsp[0].node), linha_atual); }
#line 1483 "parser.tab.c"
    break;

  case 42: /* expr_termo: expr_fator  */
#line 148 "parser.y"
                               { (yyval.node) = (yyvsp[0].node); }
#line 1489 "parser.tab.c"
    break;

  case 43: /* expr_fator: NUM  */
#line 152 "parser.y"
                               { (yyval.node) = ast_num((yyvsp[0].num), linha_atual); }
#line 1495 "parser.tab.c"
    break;

  case 44: /* expr_fator: IDENT  */
#line 153 "parser.y"
                               { (yyval.node) = ast_ident((yyvsp[0].str), linha_atual); }
#line 1501 "parser.tab.c"
    break;

  case 45: /* expr_fator: '(' expressao ')'  */
#line 154 "parser.y"
                               { (yyval.node) = (yyvsp[-1].node); }
#line 1507 "parser.tab.c"
    break;

  case 46: /* expr_fator: '-' expr_fator  */
#line 155 "parser.y"
                               { (yyval.node) = ast_unop(OP_NOT, (yyvsp[0].node), linha_atual); }
#line 1513 "parser.tab.c"
    break;


#line 1517 "parser.tab.c"

      default: break;
    }
  /* User semantic actions sometimes alter yychar, and that requires
     that yytoken be updated with the new translation.  We take the
     approach of translating immediately before every use of yytoken.
     One alternative is translating here after every semantic action,
     but that translation would be missed if the semantic action invokes
     YYABORT, YYACCEPT, or YYERROR immediately after altering yychar or
     if it invokes YYBACKUP.  In the case of YYABORT or YYACCEPT, an
     incorrect destructor might then be invoked immediately.  In the
     case of YYERROR or YYBACKUP, subsequent parser actions might lead
     to an incorrect destructor call or verbose syntax error message
     before the lookahead is translated.  */
  YY_SYMBOL_PRINT ("-> $$ =", YY_CAST (yysymbol_kind_t, yyr1[yyn]), &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;

  *++yyvsp = yyval;

  /* Now 'shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */
  {
    const int yylhs = yyr1[yyn] - YYNTOKENS;
    const int yyi = yypgoto[yylhs] + *yyssp;
    yystate = (0 <= yyi && yyi <= YYLAST && yycheck[yyi] == *yyssp
               ? yytable[yyi]
               : yydefgoto[yylhs]);
  }

  goto yynewstate;


/*--------------------------------------.
| yyerrlab -- here on detecting error.  |
`--------------------------------------*/
yyerrlab:
  /* Make sure we have latest lookahead translation.  See comments at
     user semantic actions for why this is necessary.  */
  yytoken = yychar == YYEMPTY ? YYSYMBOL_YYEMPTY : YYTRANSLATE (yychar);
  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
      yyerror (YY_("syntax error"));
    }

  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
         error, discard it.  */

      if (yychar <= YYEOF)
        {
          /* Return failure if at end of input.  */
          if (yychar == YYEOF)
            YYABORT;
        }
      else
        {
          yydestruct ("Error: discarding",
                      yytoken, &yylval);
          yychar = YYEMPTY;
        }
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:
  /* Pacify compilers when the user code never invokes YYERROR and the
     label yyerrorlab therefore never appears in user code.  */
  if (0)
    YYERROR;
  ++yynerrs;

  /* Do not reclaim the symbols of the rule whose action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;      /* Each real token shifted decrements this.  */

  /* Pop stack until we find a state that shifts the error token.  */
  for (;;)
    {
      yyn = yypact[yystate];
      if (!yypact_value_is_default (yyn))
        {
          yyn += YYSYMBOL_YYerror;
          if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYSYMBOL_YYerror)
            {
              yyn = yytable[yyn];
              if (0 < yyn)
                break;
            }
        }

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
        YYABORT;


      yydestruct ("Error: popping",
                  YY_ACCESSING_SYMBOL (yystate), yyvsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END


  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", YY_ACCESSING_SYMBOL (yyn), yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturnlab;


/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturnlab;


/*-----------------------------------------------------------.
| yyexhaustedlab -- YYNOMEM (memory exhaustion) comes here.  |
`-----------------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  goto yyreturnlab;


/*----------------------------------------------------------.
| yyreturnlab -- parsing is finished, clean up and return.  |
`----------------------------------------------------------*/
yyreturnlab:
  if (yychar != YYEMPTY)
    {
      /* Make sure we have latest lookahead translation.  See comments at
         user semantic actions for why this is necessary.  */
      yytoken = YYTRANSLATE (yychar);
      yydestruct ("Cleanup: discarding lookahead",
                  yytoken, &yylval);
    }
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
                  YY_ACCESSING_SYMBOL (+*yyssp), yyvsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif

  return yyresult;
}

#line 158 "parser.y"


void yyerror(const char *s) {
    fprintf(stderr, "Erro sintático (linha %d): %s\n", linha_atual, s);
    tem_erro = 1;
}
