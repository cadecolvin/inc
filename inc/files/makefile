TARGET={target}

CC=gcc
CFLAGS=-Wall -Wextra -I.

LINKER=gcc
LFLAGS=-Wall -I. -lm

SRCDIR=src/
BINDIR=bin/
OBJDIR=bin/obj/

SOURCES := $(wildcard $(SRCDIR)*.c
INCLUDE := $(wildcard $(SRCDIR)*.h
OBJECTS := $(SOURCES:$(SRCDIR)%.c=$(OBJDIR)%.o)

$(BINDIR)$(TARGET): $(OBJECTS)
    @$(LINKER) $(OBJECTS) $(LFLAGS) -o $@

$(OBJECTS): $(OBJDIR)%.o: $(SRCDIR)%.c
    @$(CC) $(CFLAGS) -c $< -o $@

.PHONY clean
clean:
    rm -f $(OBJECTS)
    rm -f $(BINDIR)$(TARGET)
