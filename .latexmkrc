# latexmk configuration. This is the SINGLE SOURCE OF TRUTH for where the build
# goes: it's read automatically by `make`, by a bare `latexmk`, AND by texlab
# (the editor LSP shells out to latexmk too). Because everyone reads it, the
# editor and `make` can no longer disagree about output paths.

$pdf_mode = 4;  # build a PDF with LuaLaTeX
$lualatex = 'lualatex -shell-escape -synctex=1 '
          . '-interaction=nonstopmode -file-line-error %O %S';

# Everything -- aux (.aux/.log/.bcf/.fls/...), the .pdf, and .synctex.gz -- lands
# in build/. Keeping aux_dir == out_dir means latexmk just passes
# -output-directory=build to the engine: no files get copied to the repo root, so
# nothing leaks, and the editor and `make` share one fdb_latexmk cache instead of
# thrashing it (different out_dirs used to force redundant full rebuilds).
# (No $emulate_aux: that was only needed to SPLIT aux_dir from out_dir. With them
#  equal, biber finds build/<job>.bcf with no emulation.)
$out_dir = 'build';

# `make build` copies build/<file>.pdf up to the repo root as the committable
# deliverable; the editor views build/<file>.pdf directly (point your viewer there).

# Let \usepackage{hwstyle} / \RequirePackage{preamble} find the styles/ folder,
# and let biber find references.bib at the top level.
$ENV{'TEXINPUTS'} = '.:styles:' . ($ENV{'TEXINPUTS'} // '') . ':';
$ENV{'BIBINPUTS'} = '.:'         . ($ENV{'BIBINPUTS'} // '') . ':';

# --- Draft annotations -> NOTES.md -----------------------------------------
# Collect every \todo and \note (note-to-self) into NOTES.md, each tagged with
# its source file and section breadcrumb. See scripts/collect-notes.py.
#
# Wired here because everyone builds through latexmk: texlab's on-save build,
# `make build`, and `make watch` all read this file. The top-level system() runs
# once per fresh latexmk launch (covers on-save + `make build`); $compiling_cmd
# re-runs it on every rebuild during `make watch` (latexmk -pvc stays resident).
my $collect_notes = 'python3 scripts/collect-notes.py';
system($collect_notes) if -e 'scripts/collect-notes.py';
$compiling_cmd = $collect_notes;
