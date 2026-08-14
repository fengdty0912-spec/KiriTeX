# KiriTeX

KiriTeX 是一个基于 XeLaTeX + ctex 的刷题本模板，适合中文数学、物理和工程类题集。模板提供两种版式：

- `\documentclass{kiritex}`：A4 竖版，适合打印讲义。
- `\documentclass[pad]{kiritex}`：Pad 横版，默认一页一题，适合平板阅读和批注。

## 快速开始

```latex
\documentclass{kiritex}

\title{高等数学习题集}
\author{风待桐叶}
\date{2026 年 6 月}

\begin{document}
\maketitle
\tableofcontents

\section{极限与连续}
\subsection{极限的计算}

\begin{problem}
  求极限 $\displaystyle\lim_{x\to 0}\frac{\sin x}{x}$。
\end{problem}

\begin{problemchoice}
  极限 $\displaystyle\lim_{x\to 0}\frac{\sin x}{x}$ 的值是多少
  \choice{0}
  \choice{1}
  \choice{$\infty$}
  \choice{不存在}
\end{problemchoice}

\begin{problemtf}
  极限 $\displaystyle\lim_{x\to 0}\frac{\sin x}{x}=1$。
\end{problemtf}
\end{document}
```

编译示例：

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

KiriTeX 自动管理章节、题号和选择题选项编号。正文只写内容，不手写序号。

- 正确：`\section{极限与连续}`
- 避免：`\section{第一章 极限与连续}` 或 `\section{1. 极限与连续}`
- 正确：`\begin{problem} 求极限 ... \end{problem}`
- 避免：题干开头写 `1.`、`题 1.1`、`第 1 题` 等重复编号
- 正确：`\choice{1}`
- 避免：`\choice{A. 1}`，选项字母由模板生成

这个规则同样适用于标题、题干、页眉、目录文本和封面元信息：除非序号本身是题目内容的一部分，否则不要手动加入序号。

## 题型

### 简答题 / 计算题

```latex
\begin{problem}
  求函数 $f(x)=x^2\sin x$ 的导数。
\end{problem}
```

`problem` 环境会自动输出统一题号，格式如「题 1.1」。

### 判断题

```latex
\begin{problemtf}
  若函数在一点可导，则它在该点连续。
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
\end{problemchoice}
```

`problemchoice` 用 `\choice{...}` 写选项内容。选择题题干末尾不写句号、问号或任何收尾标点。模板自动生成 A、B、C、D 等字母，并根据最长选项的宽度自动调整为每行四个、两个或一个选项。选择题题后不自动添加横线、括号或留空标记。

1.0 版本只提供 `problem`、`problemtf`、`problemchoice` 三个题目环境，不保留旧环境名。

## 版式

A4 竖版适合连续阅读和打印，题目自然流动排版。Pad 横版适合平板阅读，每道题结束后自动换页。

正文西文字体为 Latin Modern，中文字体由 ctex 根据系统环境选择。默认字号偏紧凑：A4 使用五号，Pad 模式使用小四。

## 封面

封面由 `\maketitle` 生成，读取标准元信息：

```latex
\title{高等数学习题集}
\author{风待桐叶}
\date{2026 年 6 月}
```

封面采用左右分区：左侧为 navy 色带与 `\KiriTeX` 标识，右侧显示书名、作者和日期。A4 与 Pad 模式保持同一视觉语言，只根据纸张比例调整位置。

`KiriTeX` logo 保留大小写，TeX 后缀的高度关系为 `T > X > E`。

## 答案

模板默认不内置答案系统，避免题本和答案耦合。需要答案时，可以使用外部宏包或条件编译。

使用 `answers` 宏包的基本方式：

```latex
\usepackage{answers}
\Newassociation{sol}{Solution}{ans}
\newcommand{\answer}[1]{\begin{sol}#1\end{sol}}

\begin{document}
\Opensolutionfile{ans}

\section{极限}
\begin{problem}
  求 $\displaystyle\lim_{x\to 0}\frac{\sin x}{x}$。
\end{problem}
\answer{极限值为 1。}

\Closesolutionfile{ans}
\newpage
\section*{参考答案}
\input{ans}
\end{document}
```

## 文件结构

| 文件 | 用途 |
| --- | --- |
| `kiritex.cls` | 类文件入口、选项解析、字体和基础包 |
| `kiritex-env.sty` | `problem` / `problemtf` / `problemchoice` 题型环境 |
| `kiritex-pagestyle.sty` | 页面尺寸、页眉页脚、封面、颜色和 logo |
| `demo-a4.tex` | A4 竖版示例 |
| `demo-pad.tex` | Pad 横版示例 |
| `docs/superpowers/specs/2026-05-18-kiritex-design.md` | 稳定设计规范，供后续 agent 阅读 |
| `docs/superpowers/plans/2026-05-18-kiritex.md` | 按模块组织的维护计划 |

## 维护日志

- 2026-07-06：从 KazeTeX 中分离 KiriTeX 文件，建立独立工作区。
- 2026-07-06：将正文西文字体设为 Latin Modern，并缩小默认字号。
- 2026-07-06：修正 `\KiriTeX` logo：保留 `KiriTeX` 大小写，并明确 TeX 后缀高度关系为 `T > X > E`。
- 2026-07-06：写入编号规则：标题、题干和选项内容不得重复手写模板已自动生成的序号。
- 2026-07-06：重写 README、设计规范和维护计划，使文档按题型、封面、版式、编号规则等模块组织。
- 2026-07-06：1.0 题型接口定为 `problem` / `problemtf` / `problemchoice`，并统一选择题自适应选项布局。
- 2026-07-06：规定选择题题干末尾不写句号、问号或任何收尾标点。

## 依赖

- XeLaTeX
- ctex
- fontspec
- geometry, fancyhdr, titlesec, xcolor, amsmath, amssymb, hyperref, graphicx, tikz
