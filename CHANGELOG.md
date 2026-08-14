# Changelog

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
