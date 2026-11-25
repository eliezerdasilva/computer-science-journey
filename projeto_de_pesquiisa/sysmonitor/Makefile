CC       := gcc
NASM     := nasm
PKG_CONFIG := pkg-config
BUILD    := build
GTK_CFLAGS = $(shell $(PKG_CONFIG) --cflags gtk4)
CFLAGS   = -std=c11 -O2 -Wall -Wextra -Wpedantic -I src/include $(GTK_CFLAGS)
GTK_LIBS = $(shell $(PKG_CONFIG) --libs gtk4)
NASMFLAGS := -f elf64 -g -F dwarf

ASM_SOURCES := src/assembly/core/syscalls.asm src/assembly/core/parser.asm \
               src/assembly/modules/cpu.asm src/assembly/modules/memory.asm \
               src/assembly/modules/uptime.asm src/assembly/modules/network.asm \
               src/assembly/modules/process.asm src/assembly/modules/storage.asm \
               src/assembly/modules/sensors.asm
ASM_OBJECTS := $(patsubst src/assembly/%.asm,$(BUILD)/asm/%.o,$(ASM_SOURCES))
C_SOURCES := src/c/main.c
C_OBJECTS := $(patsubst src/c/%.c,$(BUILD)/c/%.o,$(C_SOURCES))

.PHONY: all clean run check-deps
all: $(BUILD)/sysmonitor

check-deps:
	@command -v $(CC) >/dev/null || (echo 'gcc não encontrado'; exit 1)
	@command -v $(NASM) >/dev/null || (echo 'NASM não encontrado'; exit 1)
	@$(PKG_CONFIG) --exists gtk4 || (echo 'GTK 4 de desenvolvimento não encontrado (libgtk-4-dev)'; exit 1)

$(BUILD)/sysmonitor: $(ASM_OBJECTS) $(C_OBJECTS)
	$(CC) -o $@ $^ $(GTK_LIBS)

$(BUILD)/asm/%.o: src/assembly/%.asm
	@mkdir -p $(dir $@)
	$(NASM) $(NASMFLAGS) $< -o $@

$(BUILD)/c/%.o: src/c/%.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c $< -o $@

run: all
	./$(BUILD)/sysmonitor

clean:
	rm -rf $(BUILD)

.PHONY: test-layout
test-layout:
	@mkdir -p $(BUILD)
	$(CC) -std=c11 -Wall -Wextra -Wpedantic -I src/include tests/layout_check.c -o $(BUILD)/layout_check
	./$(BUILD)/layout_check
