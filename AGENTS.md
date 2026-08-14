# KiriTeX Agent Notes

Read `docs/superpowers/specs/2026-05-18-kiritex-design.md` before changing class or style behavior.

Historical source:

- KiriTeX was split from the sibling `KazeTeX` project. Use KazeTeX history only as design evidence, not as an API source to copy blindly.
- KazeTeX history shows useful lessons: robust logo commands, cover logo/title alignment, quiet formula watermarks, `\hypertarget` for TOC navigation, and avoiding decorative cover subtitles.
- Do not restore KazeTeX-era legacy names such as `tfproblem`, `choiceproblem`, `\chapter`, `\subject`, `\problemrange`, or `\problemcount` unless the user explicitly redesigns KiriTeX 1.0.

Required project rules:

- `\KiriTeX` must render as mixed-case `KiriTeX`, not `KIRITEX`.
- In the TeX suffix, the visual height relation is `T > X > E`.
- Do not manually add sequence numbers to section titles, subsection titles, problem bodies, choice text, headers, TOC entries, or cover metadata.
- KiriTeX owns generated numbering: section numbers, problem labels such as `题 1.1`, and choice labels such as `A.`.
- KiriTeX 1.x problem environments are `problem`, `problemtf`, and `problemchoice`; do not add legacy aliases.
- KiriTeX 1.1 adds optional semantic tags on problem-like environments, e.g. `\begin{problem}[基础]`; tags are metadata, not sequence numbers.
- KiriTeX 1.1 adds the `answers` class option and `\answer{...}`. Answers are hidden by default and printed inline only when `answers` is enabled.
- `problemtf` and `problemchoice` must not append automatic parentheses, blanks, or rules.
- `problemchoice` prompts must not end with a period, question mark, Chinese full stop, Chinese question mark, or any other closing punctuation.
- Subparts under one problem must use `problemsubparts`, render as `(1)`, `(2)`, etc. with English parentheses, and start from the left edge.
- Fill-in blanks use `\problemblock`; the fixed blank is `\underline{\quad\quad\quad\quad\quad\quad}`. Use `\problemblock*` at sentence end to append an un-underlined Chinese full stop.
- README and design docs should be organized by feature area, not by chronological implementation notes.
- Keep the CHANGELOG as the place for dated changes.
- Preserve old released versions with Git tags; `v1.0.1` is the compatibility baseline before 1.1.0.

After editing `.cls` or `.sty` files, compile both demos twice:

```powershell
xelatex -interaction=nonstopmode demo-a4.tex
xelatex -interaction=nonstopmode demo-a4.tex
xelatex -interaction=nonstopmode demo-pad.tex
xelatex -interaction=nonstopmode demo-pad.tex
```
