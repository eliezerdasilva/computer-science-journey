CC      = gcc
CFLAGS  = -Wall -Wextra -g -I.
LDFLAGS = -lgd -lgif -lm
OBJS    = parser.tab.o lex.yy.o ast.o semantic.o codegen.o main.o

all: meudsl

meudsl: $(OBJS)
	$(CC) -o $@ $(OBJS) $(LDFLAGS)

parser.tab.c parser.tab.h: parser.y
	bison -d -o parser.tab.c parser.y

lex.yy.c: lexer.l parser.tab.h
	flex -o lex.yy.c lexer.l

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

parser.tab.o: parser.tab.c parser.tab.h
lex.yy.o:     lex.yy.c parser.tab.h
ast.o:        ast.c ast.h
semantic.o:   semantic.c semantic.h ast.h
codegen.o:    codegen.c codegen.h ast.h
main.o:       main.c ast.h semantic.h codegen.h

# Limpa só o build — PRESERVA saida_gerada.c, saida_gerada e saida.png
clean:
	rm -f meudsl *.o parser.tab.c parser.tab.h lex.yy.c

# Limpa as saídas — use quando quiser
clean-output:
	rm -f saida_gerada saida_gerada.c saida.png

distclean: clean clean-output

.PHONY: all clean clean-output distclean