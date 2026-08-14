# Changelog

## 1.0.3 - 2026-08-14

- Shrunk the body font: A4 uses 小五 (9pt), Pad uses 五号 (10.5pt). Body sizes are now set explicitly via `\zihao` in `\AtBeginDocument`.
- Added a display-formula punctuation rule to the math style guide and AGENTS.md: text after `\[ ... \]` must not begin with a period or other closing punctuation.
- Expanded the demos to showcase vectors/matrices, partial derivatives, gradients, units, mid-sentence `\problemblock`, and multi-option choices.
- Switched vectors and matrices to `\bm` (bold) consistently.
- Added `tools/mineru2kiritex.py` (MinerU Markdown → KiriTeX converter) and `docs/mineru-workflow.md` (PDF/image → KiriTeX workflow).

## 1.0.2 - 2026-08-14

- Removed the semantic-tag feature introduced in 1.1.0: `problem`, `problemtf`, and `problemchoice` no longer accept an optional `[标签]` argument, and no tag is rendered after the problem label. The `answers` option from 1.1.0 is retained.
- Updated demos, README, design spec, AGENTS.md, and the maintenance plan to drop tag syntax and wording.
- Added the `bm` package so authors can write matrices and tensors with `\bm{...}`.
- Added `docs/superpowers/specs/2026-08-14-kiritex-math-style.md`, a standalone math formula writing guide distilled from the linear-algebra and thermodynamics notes; linked from README, the design spec, AGENTS.md, and the maintenance plan.

## 1.1.0 - 2026-07-30

- Preserved the previous release at Git tag `v1.0.1`; this version is a compatible 1.x enhancement.
- Added the `answers` class option. `\answer{...}` is hidden by default and printed inline when `answers` is enabled.
- Added optional semantic tags to `problem`, `problemtf`, and `problemchoice`, e.g. `\begin{problem}[基础]`.
- Kept all KiriTeX 1.0 problem environment names unchanged: `problem`, `problemtf`, and `problemchoice`.
- Updated `demo-a4.tex` as an A4 teacher-edition sample with visible answers.
- Updated `demo-pad.tex` as a Pad student-edition sample with hidden answers and one problem per page.
- Rewrote README around the 1.1 workflow and documented the new answer/tag syntax.
- Updated the design spec and maintenance plan so future agents understand the new contracts.

## 1.0.1 - 2026-07-19

- Learned from the sibling KazeTeX history and documented the useful carry-over rules: robust logo construction, logo/title alignment on the cover, quiet formula watermarks, Pad TOC navigation via `\hypertarget`, and avoidance of decorative cover subtitles.
- Confirmed that KiriTeX 1.0 keeps its own API: `problem`, `problemtf`, `problemchoice`, `problemsubparts`, and `\problemblock`.
- Cleaned class/style-facing Chinese literals so generated problem labels use `题 <section>.<number>` and `\problemblock*` appends an un-underlined `。`.
- Rewrote the A4 and Pad demos with readable Chinese content that demonstrates subparts, fill-in blanks, true/false prompts, and multiple-choice prompts without duplicate numbering.
- Reorganized README as a user guide and moved dated history into this changelog.
- Updated agent-facing docs so future work is organized by feature area rather than by chat history.

## 1.0.0-pre - 2026-07-06

- Split KiriTeX files from KazeTeX into an independent workspace.
- Set western text to Latin Modern and reduced default font sizes.
- Fixed the `\KiriTeX` logo to render as mixed-case `KiriTeX` with `T > X > E`.
- Established the no-duplicate-numbering rule for titles, problem bodies, choices, headers, TOC entries, and cover metadata.
- Defined the 1.0 problem interface: `problem`, `problemtf`, and `problemchoice`, with no legacy aliases.
- Added `problemsubparts` for `(1)`, `(2)` subparts and `\problemblock` for fixed fill-in blanks.
