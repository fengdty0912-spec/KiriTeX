# KiriTeX 数学公式写作规范

**状态**：1.0.2 起生效
**面向**：作者（写题、写讲义）与后续 agent

本文档约定 KiriTeX 文档中数学公式的书写方式，目标是让同一份源文件里的公式风格统一、可读、可维护。它与主设计规范 `2026-05-18-kiritex-design.md` 配套使用，规范从线性代数笔记与热力学讲义两份历史源中提炼。

## 1. 公式定界符

- 行内公式：`$ ... $`
- 行间公式（默认不编号）：`\[ ... \]`
- 需要编号的公式：`\begin{equation} ... \end{equation}`
- 多行对齐（不编号）：`\begin{align*} ... \end{align*}`，用 `&` 对齐、`\\` 换行
- 需要编号的多行：`\begin{align} ... \end{align}`

禁止使用 `$$ ... $$`。

行间公式之后的正文不得以句号（或任何收尾标点）开头：句号应写进公式内部，或改写句式，避免行首出现句号。例如：

```latex
% 错误：公式后换行、句号顶在下一行行首
\[
f(x) = x^2
\]
。所以……

% 正确：句号放进公式内部
\[
f(x) = x^2.
\]
所以……
```

## 2. 正体与斜体

正斜体是公式规范的核心：变量用斜体，函数名、常数、单位、化学式、微分算子用正体。

### 2.1 函数名用命令

标准函数名一律用反斜杠命令，不直接写字母：

| 正确 | 错误 |
| --- | --- |
| `\sin x` | `sin x` |
| `\cos x` | `cos x` |
| `\tan x` | `tan x` |
| `\ln x` | `ln x` |
| `\log x` | `log x` |
| `\lim_{x\to0}` | `lim_{x\to0}` |

可用命令：`\sin \cos \tan \cot \sec \csc \ln \log \exp \lim \max \min \det \dim \gcd \inf \sup \arg`。

### 2.2 常数与微分算子用正体

- 自然对数底：`\mathrm{e}`（不写 `e`）
- 虚数单位：`\mathrm{i}`（不写 `i`）
- 微分算子：`\mathrm{d}x`、`\frac{\mathrm{d}y}{\mathrm{d}x}`（不写 `dx`）

### 2.3 物理单位用正体

单位与词头用正体，数字与单位之间加一个空格 `\ `：

```latex
$1\ \mathrm{bar} = 10^5\ \mathrm{Pa}$
$298\ \mathrm{K}$，$0.029\ \mathrm{kg/mol}$
```

单位乘积用 `\cdot` 或指数：`\mathrm{J\cdot mol^{-1}\cdot K^{-1}}`、`\mathrm{Pa^{-1}}`、`\mathrm{m^3}`。

### 2.4 化学式用正体

```latex
$\mathrm{O_2}$、$\mathrm{H_2}$、$\mathrm{N_2}$、$\mathrm{He}$
```

### 2.5 多字母下标/上标用正体

下标是词（非单字母变量）时用 `\mathrm{}`：

```latex
P_{\mathrm{ext}}，T_{\mathrm{ext}}，n_{\mathrm{total}}，V_{\mathrm{moy}}，u^{*}_{\mathrm{air}}
```

### 2.6 变量用斜体

普通变量保持斜体：`x`、`y`、`P`、`V`、`T`、`f`、`n`。单字母变量下标也用斜体：`a_{ij}`、`P_i`。

## 3. 分数与上下标

- 分数：`\frac{1}{2}`、`\frac{n!}{(1-x)^{n+1}}`
- 行内复杂分数、极限、积分可用 `\displaystyle` 展开（与现有 demo 一致）
- 指数：`(-1)^{n}`、`x^2`、`\mathrm{e}^{x}`
- 根式：`\sqrt{...}`

## 4. 求和、求积、极限、导数、积分

- 求和：`\sum_{i=1}^{n}`
- 求积：`\prod_{i=1}^{n}`
- 极限：`\lim_{x\to 0}`、`\lim_{x\to\infty}`
- 导数：`f'(x)`、`y''`；算符形式 `\frac{\mathrm{d}}{\mathrm{d}x}`
- 偏导：`\frac{\partial V}{\partial T}`；偏导条件用 `\left( \frac{\partial V}{\partial P} \right)_{T}`
- 定积分：`\int_{a}^{b} f(x)\,\mathrm{d}x`（积分号与被积函数间 `\,`，微分 `\mathrm{d}` 前 `\,`）

## 5. 向量与矩阵

- 向量：`\bm{v}`、`\bm{f}`、`\bm{n}`（粗体）
- 矩阵/张量：`\bm{A}`、`\bm{B}`（粗体，需 `bm` 宏包）
- 零矩阵 `\bm{O}`、单位矩阵 `\bm{I}`
- 转置：`(x_1, x_2, \ldots, x_n)^{\mathrm{T}}`

矩阵环境：

```latex
\begin{vmatrix} ... \end{vmatrix}   % 行列式
\begin{pmatrix} ... \end{pmatrix}   % 圆括号矩阵
\begin{bmatrix} ... \end{bmatrix}   % 方括号矩阵
\begin{cases} ... \end{cases}       % 分段函数
```

元素用 `&` 分隔、`\\` 换行。

## 6. 括号

成对括号用 `\left ... \right` 自适应大小：

```latex
\left( \frac{1}{x} \right)，\left[ -1, 1 \right]，\left| x \right|
```

## 7. 省略号

- 中间省略号 `\cdots`：`a_1, a_2, \cdots, a_n`、矩阵行间
- 下方省略号 `\ldots`：`1, 2, \ldots, n`

## 8. 间距

- 积分：`\int ... \,\mathrm{d}x`
- 数字与单位之间：`\ `
- 关系符号两侧按需要 `\quad` 或 `\qquad`
- 平均值：`\langle v^2 \rangle`

## 9. 常用符号速查

| 符号 | 命令 |
| --- | --- |
| 乘号 | `\times` |
| 点乘 | `\cdot` |
| 约等于 | `\approx` |
| 趋于 | `\to` |
| 不等于 | `\neq` |
| 属于 | `\in` |
| 蕴含 | `\implies` |
| 梯度 | `\nabla` |
| 变化量 | `\Delta` |
| 无穷 | `\infty` |
| 希腊字母 | `\pi \rho \lambda \mu \tau \chi \alpha \beta \Omega \sigma \xi \theta` |

## 10. 证明与解答收尾

- 证明收尾用 `\hfill $\square$`
- 题解与答案正文用中文标点，公式后标点与中文文本保持一致
