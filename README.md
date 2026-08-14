# KiriTeX

KiriTeX 是一个基于 XeLaTeX + ctex 的中文题本模板，适合数学、物理和工程类讲义。它用同一份源文件生成两种版式：

- `\documentclass{kiritex}`：A4 竖版，适合打印讲义。
- `\documentclass[pad]{kiritex}`：Pad 横版，默认一页一题，适合平板阅读和批注。
- `\documentclass[answers]{kiritex}`：教师版，显示 `\answer{...}` 写入的答案。

当前版本：`1.0.2`。

## 快速开始

```latex
\documentclass{kiritex}

\title{高等数学习题集}
\author{风待桐叶}
\date{2026 年 7 月}

\begin{document}
\maketitle
\tableofcontents

\section{极限与连续}
\subsection{极限的计算}

\begin{problem}
  求极限 $\displaystyle\lim_{x\to 0}\frac{\sin x}{x}$。
  \answer{极限值为 $1$。}
\end{problem}

\begin{problemchoice}
  极限 $\displaystyle\lim_{x\to 0}\frac{\sin x}{x}$ 的值是
  \choice{0}
  \choice{1}
  \choice{$\infty$}
  \choice{不存在}
  \answer{B。}
\end{problemchoice}
\end{document}
```

默认不显示答案。把第一行改成下面形式即可生成教师版：

```latex
\documentclass[answers]{kiritex}
```

## 编译

```bash
xelatex demo-a4.tex
xelatex demo-a4.tex
```

也可以使用 Makefile：

```bash
make a4
make pad
make all
```

## 写作规则

KiriTeX 自动管理章节编号、题号和选择题选项编号。正文只写内容，不手写序号。

- 正确：`\section{极限与连续}`
- 避免：`\section{第一章 极限与连续}` 或 `\section{1. 极限与连续}`
- 正确：`\begin{problem} 求极限 ... \end{problem}`
- 避免：题干开头写 `1.`、`题 1.1`、`第 1 题` 等重复编号
- 正确：`\choice{1}`
- 避免：`\choice{A. 1}`，选项字母由模板生成

这个规则同样适用于标题、题干、页眉、目录文本和封面元信息：除非序号本身是题目内容的一部分，否则不要手动加入序号。

## 公式写作

数学公式遵循 `docs/superpowers/specs/2026-08-14-kiritex-math-style.md` 的约定，要点如下：

- 行间公式用 `\[ ... \]`（默认不编号），行内用 `$ ... $`，多行对齐用 `align*`，需要编号时用 `equation`。
- 变量用斜体，函数名、常数、单位、化学式、微分算子用正体：`\sin x`、`\mathrm{e}`、`\mathrm{i}`、`\mathrm{d}x`、`\mathrm{Pa}`、`\mathrm{O_2}`。
- 多字母下标用正体：`P_{\mathrm{ext}}`。
- 向量用 `\vec{v}`，矩阵/张量用 `\bm{A}`。
- 积分写 `\int_a^b f(x)\,\mathrm{d}x`。

## 题型

### 简答题 / 计算题

```latex
\begin{problem}
  求函数 $f(x)=x^2\sin x$ 的导数。
  \answer{$f'(x)=2x\sin x+x^2\cos x$。}
\end{problem}

`problem` 环境会自动输出统一题号，格式如「题 1.1」。

大题下的小题使用 `problemsubparts`，只写 `\item`，不要手写小题编号。小题编号自动显示为英文括号形式 `(1)`、`(2)`，并从左侧正常顶齐。

```latex
\begin{problem}
  计算下列极限：
  \begin{problemsubparts}
    \item $\displaystyle\lim_{x\to 0}\frac{\sin x}{x}$
    \item $\displaystyle\lim_{x\to 0}\frac{1-\cos x}{x^2}$
  \end{problemsubparts}
\end{problem}
```

### 填空题

填空使用 `\problemblock`，固定渲染为：

```latex
\underline{\quad\quad\quad\quad\quad\quad}
```

句末填空用星号形式 `\problemblock*`，模板会在横线后补一个不带下划线的中文句号。

### 判断题

```latex
\begin{problemtf}
  若函数在一点可导，则它在该点连续。
  \answer{正确。}
\end{problemtf}
```

`problemtf` 与普通题共享同一套题号。判断题只输出题号和题干，题后不自动添加横线、括号或留空标记。

### 选择题

```latex
\begin{problemchoice}
  以下哪个函数在 $x=0$ 处连续
  \choice{$f(x)=x$}
  \choice{$f(x)=1/x$}
  \choice{$f(x)=|x|/x$}
  \choice{$f(x)=\tan(1/x)$}
  \answer{A。}
\end{problemchoice}
```

选择题题干末尾不写句号、问号或任何收尾标点。模板自动生成 A、B、C、D 等字母，并根据最长选项的宽度自动调整为每行四个、两个或一个选项。选择题题后不自动添加横线、括号或留空标记。

1.x 版本的题目环境仍为 `problem`、`problemtf`、`problemchoice`；小题用 `problemsubparts`，填空用 `\problemblock`。

## 答案

`\answer{...}` 默认隐藏，适合学生版。使用 `answers` 类选项后显示为教师版：

```latex
\documentclass[answers]{kiritex}
```

答案内容跟随题目书写，不建立额外编号，也不改变题号计数。

## 版式

A4 竖版适合连续阅读和打印，题目自然流动排版。Pad 横版适合平板阅读，每道题结束后自动换页。

正文西文字体为 Latin Modern，中文字体由 ctex 根据系统环境选择。默认字号偏紧凑：A4 使用五号，Pad 模式使用小四。

## 封面

封面由 `\maketitle` 生成，读取标准元信息：

```latex
\title{高等数学习题集}
\author{风待桐叶}
\date{2026 年 7 月}
```

封面采用左右分区：左侧为 navy 色带与 `\KiriTeX` 标识，右侧显示书名、作者和日期。A4 与 Pad 模式保持同一视觉语言，只根据纸张比例调整位置。

`KiriTeX` logo 保留大小写，TeX 后缀的高度关系为 `T > X > E`。

## 文件结构

| 文件 | 用途 |
| --- | --- |
| `kiritex.cls` | 类文件入口、选项解析、字体和基础包 |
| `kiritex-env.sty` | `problem` / `problemtf` / `problemchoice` 题型环境，小题、填空和答案命令 |
| `kiritex-pagestyle.sty` | 页面尺寸、页眉页脚、封面、颜色和 logo |
| `demo-a4.tex` | A4 竖版教师版示例 |
| `demo-pad.tex` | Pad 横版学生版示例 |
| `docs/superpowers/specs/2026-05-18-kiritex-design.md` | 稳定设计规范，供后续 agent 阅读 |
| `docs/superpowers/specs/2026-08-14-kiritex-math-style.md` | 数学公式写作规范 |
| `docs/superpowers/plans/2026-05-18-kiritex.md` | 按模块组织的维护计划 |
| `CHANGELOG.md` | 版本历史 |

## 维护

未来 agent 修改类文件或样式文件前，应先阅读设计规范和 `AGENTS.md`。KiriTeX 从 KazeTeX 的历史中保留了稳健 logo、封面公式水印、logo 与标题对齐、Pad 目录跳转等经验，但 1.x API 以本文档为准，不恢复旧命令名。

版本变化记录在 `CHANGELOG.md`。

## 依赖

- XeLaTeX
- ctex
- fontspec
- geometry, fancyhdr, titlesec, xcolor, amsmath, amssymb, hyperref, graphicx, tikz
