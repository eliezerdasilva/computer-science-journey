CC = gcc
CFLAGS = -Wall -Wextra -g -I.
LDFLAGS = -lgd -lgif -lm

SRCS = parser.tab.c lex.yy.c ast.c semantic.c codegen.c main.c
TARGET = meudsl

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

parser.tab.c parser.tab.h: parser.y
	bison -d -o parser.tab.c parser.y

lex.yy.c: lexer.l parser.tab.h
	flex -o lex.yy.c lexer.l

clean:
	rm -f $(TARGET) parser.tab.c parser.tab.h lex.yy.c

.PHONY: cleanma