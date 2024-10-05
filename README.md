# Source

The original source was: [latextemplates.com/template/cleese-assignment](https://www.latextemplates.com/template/cleese-assignment), but I have modified it for my needs.

## Commands

Run the following `make X` where X is any of the following:

- `clean`, removes all the noise and mess that gets output. Read the file if you want more info

**Note**: add the name of the top-level file at the end of the `build` command in the makefile e.g

Go from

`pdflatex  -synctex=1 -interaction=nonstopmode -file-line-error -recorder `

`pdflatex  -synctex=1 -interaction=nonstopmode -file-line-error -recorder add_the_top_level_here.tex`

- `build`, runs the build process

# Support

Fork this repo and modify it for your own needs. Unfortunately, I don't have time to help you debug, or make modifications. This is a living doc, so its contents will change over time.

Good luck and happy homework solving!s
