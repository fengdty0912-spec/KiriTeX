# Changelog

## 1.0.4 - 2026-08-19

### 数学规范（核心改动）

- **分式写法重订**：`\dfrac` 全面废弃。行内含分式的公式写 `\displaystyle \frac{...}{...}`（用 `\displaystyle` 显式展开、分式写 `\frac`），行间公式直接 `\frac`。同步修订 math-style spec §3。
- **数学量必须放进公式环境**（新增 spec §2.8）：区间 `$[a,b]$` / `$(0,2)$`、坐标与点 `$(x_0,y_0)$` / `$P(2,0,-3)$`、函数调用 `$f(x)$`、单字母变量与希腊字母 `$x$` / `$\xi$`，一律不裸写在中文正文。
- **分段函数规范**（新增 spec §5.1）：`\begin{cases}` 每行写「值, & 条件」，逗号后带空格（`, &`）。
- 矩阵、向量、变换矩阵统一 `\bm{}`：`\bm{A}`、`\bm{\alpha}`、变换矩阵 `\bm{T}`、单位阵 `\bm{E}`、零矩阵 `\bm{O}`；数域 `\mathbb{K}` / `\mathbb{R}`，向量空间 `\mathbb{V}`（AGENTS.md 与 spec 同步）。

### 工具与工作流

- `mineru2kiritex.py` 新增只读规范自检模式 `py mineru2kiritex.py --check file.tex`：检测 `\dfrac` 残留、行内 `\frac` 缺 `\displaystyle`、cases 逗号后缺空格、`$` / 花括号 / `\[...\]` / `problem` 系列环境平衡、正文裸区间坐标、疑似漏 `\bm` 的矩阵字母，只报告不改写。
- `docs/mineru-workflow.md` 新增「逐题研判」与「规范自检」两节：OCR 只是草稿，每题需人工判断公式实际写法与文本表述；回忆版题目按描述补全为完整可解题并标注。
- demo 两个文件按新分式/加粗规则更新并重新编译，README 维护节加入自检入口。

### 经验与教训（来自高数、线代两套真题制作）

- **规范必须直接写进 tex 源码**：用脚本事后补 `\bm`/`\mathbb` 等易出错（正则转义、矩阵行分隔符 `\\` 与 `\bm` 相邻、heredoc 吞反斜杠导致 `\b` 被当退格写入文件），且难以收尾。正确做法是手写时一次到位，再用 `--check` 复核。
- **行/列分隔符是地雷**：矩阵内 `\\` 后跟加粗项时是三反斜杠 `\\\bm{B}`，任何字符串级替换都可能误伤；后续工具改动应避免对数学内容做无差别文本替换。
- **交付前必须自检 + 双编译**：检查项至少包括 `--check` 清零、`xelatex` 双编译无错误/警告/缺字、old-version 与 draft 分别在独立目录避免污染。

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
