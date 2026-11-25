# DSL de Animação 2D e Pixel Art — Compilador One-Step em C

Compilador completo para uma **DSL de animação 2D e pixel art**, escrito em **C** com **Flex** (análise léxica) e **Bison** (análise sintática). O pipeline é **one-step**: lê um arquivo `.dsl`, analisa, valida semanticamente, executa as instruções diretamente sobre a AST e produz uma imagem `.png` ou um `.gif` animado.

## Pré-requisitos

- `flex`
- `bison`
- `gcc`
- `libgd-dev`
- `libgif-dev`

```bash
sudo apt install flex bison gcc libgd-dev libgif-dev
```

## Compilação

```bash
make
```

## Execução

```bash
# Inspecionar a AST gerada
./meudsl --ast exemplos/animacao.dsl

# Gerar a imagem/GIF final
./meudsl exemplos/estatico.dsl
```

## Gramática EBNF Completa

```ebnf
Programa     ::= ListaCmds

ListaCmds    ::= { Comando }

Comando      ::= Desenho ';'
               | Controle
               | Animacao
               | 'VAR' IDENT '=' Expressao ';'
               | IDENT '=' Expressao ';'

Desenho      ::= 'TELA' Expressao ',' Expressao ',' Cor
               | 'PIXEL' Expressao ',' Expressao ',' Cor
               | 'LINHA' Expressao ',' Expressao ',' Expressao ',' Expressao ',' Cor
               | 'RETANGULO' Expressao ',' Expressao ',' Expressao ',' Expressao ',' Cor
               | 'CIRCULO' Expressao ',' Expressao ',' Expressao ',' Cor
               | 'TEXTO' String 'EM' Expressao ',' Expressao ',' Cor
               | 'COR_FUNDO' Cor
               | 'SALVA' String ';'

Controle     ::= 'SE' Expressao ListaCmds ['SENAO' ListaCmds] 'FIM'
               | 'REPETE' Expressao 'VEZES' ListaCmds 'FIM'

Animacao     ::= 'ANIMA' 'FPS' NUM ';'
               | 'MOVE' IDENT 'PARA' '(' Expressao ',' Expressao ')' 'EM' Expressao 'SEGUNDOS' ';'
               | 'QUADRO' ListaCmds 'FIM'

Expressao    ::= ExprLogica

ExprLogica   ::= ExprLogica 'OU' ExprLogica
               | ExprLogica 'E' ExprLogica
               | 'NAO' ExprLogica
               | ExprRel

ExprRel      ::= ExprRel ('==' | '!=' | '<' | '>' | '<=' | '>=') ExprRel
               | ExprArit

ExprArit     ::= ExprArit ('+' | '-') ExprTermo
               | ExprTermo

ExprTermo    ::= ExprTermo ('*' | '/' | '%') ExprFator
               | ExprFator

ExprFator    ::= NUM
               | IDENT
               | '(' Expressao ')'
               | '-' ExprFator

Cor          ::= '#' HEX HEX HEX HEX HEX HEX

String       ::= '"' { caractere } '"'
```

**Precedência** (do menor para o maior): `OU` < `E` < `NAO` < relacionais < `+ -` < `* / %` < unário.

## Arquitetura

Pipeline do compilador:

```
arquivo.dsl
    │
    ▼
┌─────────┐     ┌─────────┐     ┌────────────┐     ┌─────────┐     ┌─────────┐
│  Flex   │ ──▶ │  Bison  │ ──▶ │ Semântico  │ ──▶ │ Codegen │ ──▶ │ Saída   │
│ (tokens)│     │  (AST)  │     │ (tabela)   │     │ (exec.) │     │ PNG/GIF │
└─────────┘     └─────────┘     └────────────┘     └─────────┘     └─────────┘
```

Estrutura de arquivos:

```
projeto/
├── Makefile
├── lexer.l              # Especificação Flex
├── parser.y             # Especificação Bison
├── ast.h / ast.c        # Nós da AST e construção/liberação
├── semantic.h / .c      # Tabela de símbolos e validações
├── codegen.h / .c       # Execução direta + geração de PNG/GIF
├── main.c               # Ponto de entrada e orquestração
├── exemplos/
│   ├── estatico.dsl
│   ├── loop.dsl
│   └── animacao.dsl
└── README.md
```

## Tratamento de Erros

As mensagens incluem a linha onde o erro foi detectado.

**Erro sintático** (ex.: falta `;` ou `FIM`):

```
Erro sintático (linha 6): syntax error
Falha na análise sintática.
```

**Erro semântico** (ex.: variável não declarada, FPS inválido):

```
Erro semântico (linha 5): variável não declarada
Falha na análise semântica.
```

## Decisões de Projeto

- **Abordagem B (execução direta)**: o compilador percorre a AST e executa as instruções diretamente, chamando funções da `libgd`. Evita a complexidade de gerar código C sintaticamente correto e mantém o pipeline one-step simples.
- **libgd** para desenho de primitivas (pixels, linhas, retângulos, círculos, texto) e exportação PNG.
- **giflib** para escrita do GIF final.
- **AST com `union`**: cada nó usa uma união para armazenar os campos específicos do seu tipo, economizando memória e mantendo o código organizado.
- **Flex + Bison** para garantir análise léxica e sintática robustas, com precedência explícita de operadores.

## Limitações Conhecidas

- **GIF animado simplificado**: na versão base, apenas o primeiro frame é gravado no GIF. A animação completa quadro a quadro é uma extensão planejada.
- **`MOVE` não interpola múltiplos frames automaticamente**: o comando atualiza a variável alvo, mas a geração dos frames intermediários precisa ser feita com `QUADRO` dentro de `REPETE`.
- **Sem tabela de símbolos com escopo**: variáveis têm escopo global.

## Referências

- Documentação do Flex: <https://github.com/westes/flex>
- Documentação do Bison: <https://www.gnu.org/software/bison/>
- libgd: <https://libgd.github.io/>
- giflib: <https://giflib.sourceforge.net/>
- PixelScript Compiler (referência arquitetural): repositório original em Python/Pillow, usado apenas como inspiração — a implementação deste projeto é 100% em C.