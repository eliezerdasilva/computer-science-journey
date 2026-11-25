NOME = lerPosicao

all: $(NOME)

$(NOME): $(NOME).o
	ld -m elf_i386 -s -o $@ $^
	rm -f *.o

%.o: %.asm
	nasm -f elf32 $< -o $@

.PHONY: all