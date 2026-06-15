# LaTeX template Makefile. Build settings live in .latexmkrc (everything ->
# build/, styles/ on the search path). `make build` copies the finished PDF up
# to the repo root as the committable deliverable.
#
#   make                 build hw.tex (the default)
#   make FILE=essay      build essay.tex (runs biber for the bibliography)
#   make new Q=1         split out one question into parts/q1.tex and link it
#                        into the master (FILE); picks a hw or essay skeleton
#                        (build a subset by commenting out \subfile{} lines)
#   make watch FILE=...  rebuild continuously as you edit
#   make write FILE=...  open the file in Helix "typewriter" mode
#   make wordcount FILE=... prose-aware word count (skips LaTeX markup)
#   make notes           compile all \todo + \note annotations into NOTES.md
#                        (also runs automatically on every build / editor save)
#   make clean           remove the build/ aux files (keep the PDF)
#   make cleanall        remove the build/ aux files AND the PDF
#
# FILE is the entry-file name without the .tex extension (default: hw).

FILE ?= hw

.PHONY: build new watch write wordcount notes clean cleanall

build:
	latexmk $(FILE).tex
	@cp -f build/$(FILE).pdf $(FILE).pdf   # publish a committable copy of the PDF at the repo root

new:
	@test -n "$(Q)" || { echo "usage: make new Q=<number> [FILE=hw|essay]"; exit 1; }
	@test ! -e parts/q$(Q).tex || { echo "parts/q$(Q).tex already exists — refusing to overwrite"; exit 1; }
	@mkdir -p parts
	@if grep -q hwstyle $(FILE).tex; then tpl=parts/_question.tex; else tpl=parts/_section.tex; fi; \
		sed "s/QNUM/$(Q)/g; s/MASTER/$(FILE)/g" $$tpl > parts/q$(Q).tex
	@awk '/% PARTS-END/{print "\\subfile{parts/q$(Q)}"; print; next} {print}' $(FILE).tex > $(FILE).tex.tmp && mv $(FILE).tex.tmp $(FILE).tex
	@echo "created parts/q$(Q).tex and linked it into $(FILE).tex"

watch:
	latexmk -pvc $(FILE).tex

write:
	hx -c .helix/typewriter_mode.toml $(FILE).tex

wordcount:
	@texcount -inc -sum -brief $(FILE).tex

notes:
	@python3 scripts/collect-notes.py

clean:
	latexmk -c $(FILE).tex

cleanall:
	latexmk -C $(FILE).tex
