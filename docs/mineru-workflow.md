# MinerU → KiriTeX 工作流

KiriTeX 通过 [MinerU](https://github.com/opendatalab/MinerU)（OpenDataLab 出品）获得一套 PDF/图片读取工作流：用 MinerU 抽取文档中的文字、公式与结构，再用 `tools/mineru2kiritex.py` 转成 KiriTeX 的 `.tex`，最后用 XeLaTeX 编译成排版良好的 PDF。

## 流程概览

```
PDF / 图片
   │  1. MinerU 抽取（公式→LaTeX，表格→HTML，图片→文件）
   ▼
Markdown / JSON（含 LaTeX 公式）
   │  2. mineru2kiritex.py 结构映射 + 公式清洗
   ▼
KiriTeX .tex
   │  3. xelatex 编译
   ▼
PDF
```

## 1. 安装 MinerU

需要 Python 3.10–3.13。推荐用 `uv`（或 `pip`）安装 `pipeline` 后端（纯 CPU 可跑）：

```powershell
uv tool install "mineru[core]" --index-url https://pypi.tuna.tsinghua.edu.cn/simple
# 或
pip install -U "mineru[core]"
```

国内网络建议配 PyPI 镜像（如上 `--index-url`），模型源用 ModelScope：

```powershell
$env:MINERU_MODEL_SOURCE = "modelscope"
```

首次运行会自动下载模型（pipeline 后端约 1–2 GB）。

## 2. 抽取 PDF / 图片

```powershell
mineru -p 2015.pdf -o outdir -b pipeline -m auto -l ch
```

- `-b pipeline`：CPU 快速稳定后端（高精度可选 `vlm-engine`，需 GPU）。
- `-m auto`：自动判断文本/扫描件；`-m ocr` 强制 OCR（扫描件）。
- `-l ch`：中文（提升 OCR 精度）。

输出在 `outdir/<name>/auto/` 下，关键文件：

- `<name>.md`：Markdown，公式已是 LaTeX。
- `<name>_content_list.json`：结构化内容（备用）。
- `images/`：抽取出的图片。

## 3. 转换为 KiriTeX

```powershell
py tools/mineru2kiritex.py outdir/2015/auto/2015.md -o 真题_高等数学.tex --title "高等数学真题"
```

转换器做**通用结构映射**：

- `# / ## / ###` → `\section / \subsection / \subsubsection`
- `$$ ... $$` → `\[ ... \]`，`$ ... $` 保留
- `![...](path)` → `figure` + `\includegraphics`
- 公式清洗：`\operatorname* { l i m }` → `\lim`、去掉 MinerU 括号/上下标周围的多余空格、`\begin{array}` → `\begin{aligned}`、拼接被空格拆开的数字等

它**不识别题型**。转成初稿后，再把题目手动包进 `problem` / `problemchoice` / `problemtf` 环境、补 `\problemblock` 填空等语义结构（参考 `demo-a4.tex` 与课程目录下的 `真题_线性代数.tex`）。

## 4. 编译

```powershell
xelatex -interaction=nonstopmode 真题_高等数学.tex
xelatex -interaction=nonstopmode 真题_高等数学.tex
```

编译需要 KiriTeX 的 `kiritex.cls`、`kiritex-env.sty`、`kiritex-pagestyle.sty` 与 `.tex` 同目录。

## 已知限制

- MinerU 的 OCR 公式是「脏」的：`\lim` 常被认成 `\operatorname* { l i m }`，复杂公式可能有漏括号、漏 `\to` 等错误。转换器能自动修掉系统性错误，但**个别 OCR 错仍需人工校正**。
- 结构是扁平的：题号 `1.`、`解：` 等都是正文文本，转换器不会自动识别成 `problem` 环境或答案块。
- 扫描件 / 手写 / 复杂版面质量低于文本型 PDF。
