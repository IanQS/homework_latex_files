# LaTeX command cheatsheet

The custom commands/environments this template provides, plus the most useful
bits of the packages it loads. Everything here is available in **both** `hw.tex`
and `essay.tex` unless marked **(HW)** or **(essay)**.

---

## Document structure (HW)

| Command / environment                              | What it does                                        | When to use                                   |
| -------------------------------------------------- | --------------------------------------------------- | --------------------------------------------- |
| `\begin{question} ... \end{question}`              | Starts a numbered "Question N" section              | One per problem on the assignment             |
| `\questiontext{...}`                               | Bold prompt line under a question                   | To restate the question before answering      |
| `\begin{subquestion}{Title} ... \end{subquestion}` | Numbered `(a)`, `(b)`, ... subsection               | Multi-part problems                           |
| `\begin{answer} ... \end{answer}`                  | Breakable boxed answer (aliases: `solution`, `sol`) | An environment that wraps your worked answer. |
| `\assignmentSection{TITLE}`                        | Centered horizontal-rule divider                    | Split a long assignment into major parts      |

**Title-page fields** (set near the top of `hw.tex` with `\newcommand`):
`\assignmentClassCode`, `\classTitle`, `\assignmentTitle`, `\assignmentQuestionName`
(prefix word — "Question", "Problem", ...), `\studentName`, `\studentNumber`, and
optional `\studentID`, `\assignmentDueDate`, `\assignmentClassInstructor`.

## Title / metadata (essay)

Set near the top of `essay.tex`: `\essayTitle`, `\essayAuthor`, `\essayDate`,
and optional `\essaySubtitle`. Then `\maketitle` prints the heading.

## Splitting into per-question files (subfiles)

| Command / step                                | What it does                                              |
| --------------------------------------------- | --------------------------------------------------------- |
| `make new Q=1` / `make new Q=1 FILE=essay`    | Scaffold `parts/q1.tex` (hw `question{}` or essay `section{}`) and link it into the master |
| `\subfile{parts/q1}` (in the master)          | Pulls a part into the master build (inserted for you by `make new`) |
| `\documentclass[hw.tex]{subfiles}`            | First line of a part — names its master (relative to the repo root) |
| `\ifSubfilesClassLoaded{...}{...}`            | Run code only when a part is previewed on its own (e.g. `\printbibliography`) |
| comment out a `\subfile{}` line               | Drop that question from the build; `make` builds the whole master |

Split a long document into one file per question — handy when your editor lacks
code folding. You build the whole master with `make`; to build a subset, comment
out the `\subfile{}` lines you don't want.

---

## Math (mathtools, amssymb, amsthm)

| Command / environment                                     | What it does                               | When to use                                      |
| --------------------------------------------------------- | ------------------------------------------ | ------------------------------------------------ |
| `$ ... $` / `\[ ... \]`                                   | Inline / display math                      | Anytime                                          |
| `\begin{equation}\label{eq:x} ... \end{equation}`         | Numbered, referable equation               | When you'll refer back to it (`\cref{eq:x}`)     |
| `\begin{align} ... \end{align}` (or `align*`)             | Multi-line aligned math (`*` = unnumbered) | Derivations, systems                             |
| `\coloneqq`, `\eqqcolon`                                  | `:=` and `=:` done right                   | Definitions                                      |
| `\abs{x}`, `\norm{v}`, `\ceil{x}`, `\floor{x}`            | Auto-sizing delimiters                     | Use `\abs*{...}` to force full-height delimiters |
| `\begin{theorem}` / `lemma` / `corollary` / `proposition` | Numbered theorem-like blocks               | Stating results                                  |
| `\begin{definition}` / `example`                          | Numbered, upright-text blocks              | Definitions, worked examples                     |
| `\begin{remark}`                                          | _Unnumbered_ aside                         | Side notes                                       |
| `\begin{proof} ... \end{proof}`                           | Proof block with QED box (amsthm)          | Proofs                                           |

## Units & numbers (siunitx)

| Command               | What it does                           | Example                                      |
| --------------------- | -------------------------------------- | -------------------------------------------- |
| `\qty{<num>}{<unit>}` | Number + unit, correct spacing         | `\qty{7.0}{\gram}`, `\qty{760}{\kilo\joule}` |
| `\num{<num>}`         | Format a number (thousands, exponents) | `\num{1.2e6}`                                |
| `\unit{<unit>}`       | A unit on its own                      | `\unit{\meter\per\second}`                   |

Use these instead of typing `7.0g` so spacing/formatting stays consistent.

---

## Cross-references (cleveref)

| Command             | What it does                               | When to use                                     |
| ------------------- | ------------------------------------------ | ----------------------------------------------- |
| `\label{type:name}` | Tag an equation/figure/table/section       | Right after `\caption{}` or inside the equation |
| `\cref{eq:x}`       | Smart reference → "equation 1", "figure 2" | Mid-sentence; auto-detects the type             |
| `\Cref{eq:x}`       | Capitalized version → "Equation 1"         | Start of a sentence                             |
| `\cref{a,b,c}`      | Lists/ranges → "figures 1 to 3"            | Referring to several at once                    |

Convention: prefix labels by type — `eq:`, `fig:`, `tab:`, `sec:`. Then you never
have to write the word "Figure"/"Equation" by hand.

## Figures & tables

| Command / environment                                                                | What it does                                  | When to use                                         |
| ------------------------------------------------------------------------------------ | --------------------------------------------- | --------------------------------------------------- |
| `\addfigure[width]{file}{caption}{label}`                                            | Centered figure + caption + label in one call | The quick path; `width` defaults to `0.9\textwidth` |
| `\begin{figure}[htbp]\centering \includegraphics{...}\caption{}\label{}\end{figure}` | Manual figure                                 | When you need subfigures or custom layout           |
| `\begin{subfigure}{...}` (subcaption)                                                | Side-by-side sub-figures                      | Multiple images under one figure number             |
| `\begin{table}[h]\centering ... \caption{}\label{}\end{table}`                       | Floating table                                | Tabular data you want numbered                      |
| `\toprule` / `\midrule` / `\bottomrule` (booktabs)                                   | Clean horizontal rules                        | Always, instead of `\hline`                         |

Images are looked up in `images/` automatically (`\graphicspath`).

---

## Code listings (listings, pre-styled)

| Command / environment                                      | What it does                             | When to use                             |
| ---------------------------------------------------------- | ---------------------------------------- | --------------------------------------- | --------------- | ------------------------------------------ |
| `\begin{lstlisting}[language=Python] ... \end{lstlisting}` | Block of source code, syntax-highlighted | Multi-line code (works inside `answer`) |
| `\lstinputlisting[language=C]{file.c}`                     | Include code from a file                 | Don't paste — pull the real file        |
| `\verb                                                     | ...                                      | `                                       | Inline verbatim | Short literal snippets / showing a command |
| `\codeword{foo}`                                           | Inline monospace (`\texttt`)             | Naming a function/flag in prose         |

## Lists (enumitem)

| Form                                    | What it does                  |
| --------------------------------------- | ----------------------------- |
| `\begin{itemize} ... \end{itemize}`     | Bullets                       |
| `\begin{enumerate} ... \end{enumerate}` | Numbered                      |
| `\begin{enumerate}[label=(\alph*)]`     | Custom labels → (a), (b), ... |
| `\begin{itemize}[noitemsep]`            | Tighten spacing               |

---

## Drafting

| Command                    | What it does                | When to use                                                           |
| -------------------------- | --------------------------- | --------------------------------------------------------------------- |
| `\todo{note}`              | Margin note while drafting  | A task to act on; auto-hidden in the final build                      |
| `\todo[inline]{note}`      | Inline (in-text) note       | Longer reminders                                                      |
| `\note{note}`              | Blue "note-to-self" (NOTE:) | An observation, not a task; same auto-hide as `\todo`                 |
| `\note[inline]{note}`      | Inline note-to-self         | Longer notes                                                          |
| `\listoftodos`             | Collected list of all todos | A drafting checklist page                                             |
| `make notes` / on save     | Compile todos + notes -> `NOTES.md` | One digest of every `\todo`/`\note` with its file + section; auto-runs on each build |
| `\newcommand{\finaldoc}{}` | Hides all `\todo`/`\note`   | Uncomment it (above `\usepackage{...style}`) for the submission build |

---

## Bibliography (essay — biblatex/biber)

| Command                    | What it does                             | When to use                              |
| -------------------------- | ---------------------------------------- | ---------------------------------------- |
| `\parencite{key}`          | Parenthetical citation → "(Author 2020)" | Most inline citations                    |
| `\autocite{key}`           | Style-appropriate cite                   | When you want the style's default form   |
| `\textcite{key}`           | "Author (2020) argues..."                | When the author is part of your sentence |
| `\printbibliography`       | Prints the reference list                | Once, at the end                         |
| `\enquote{...}` (csquotes) | Smart quotation marks                    | Quoting text; adapts to language         |

Add sources to `references.bib`; `key` is the entry's first field.
