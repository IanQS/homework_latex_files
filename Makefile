clean:
	rm *.fls; rm *.log;rm *.aux; rm *.fdb_latexmk; rm *.gz;

build:
	pdflatex  -synctex=1 -interaction=nonstopmode -file-line-error -recorder  sol_template.tex
