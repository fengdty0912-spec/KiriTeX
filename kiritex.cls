\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{kiritex}[2026/08/14 v1.0.2 KiriTeX problem workbook template]

% ---- class option toggles ----
\newif\if@kiritex@pad
\@kiritex@padfalse
\newif\if@kiritex@answers
\@kiritex@answersfalse
\DeclareOption{pad}{\@kiritex@padtrue}
\DeclareOption{answers}{\@kiritex@answerstrue}

% Pass unknown options to ctexart
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{ctexart}}
\ProcessOptions\relax

% Load base class (zihao as class option only supports 5, -4, false in TL2026)
% Keep the default text smaller; pad mode bumps this once at begin document.
\LoadClass[zihao=5,a4paper]{ctexart}

% ---- required packages ----
\RequirePackage{xcolor}
\RequirePackage{geometry}
\RequirePackage{fancyhdr}
\RequirePackage{titlesec}
\RequirePackage{amsmath,amssymb}
\RequirePackage{bm}
\RequirePackage{hyperref}
\RequirePackage{graphicx}
\RequirePackage{xparse}

% ---- Latin font family ----
\setmainfont{Latin Modern Roman}
\setsansfont{Latin Modern Sans}
\setmonofont{Latin Modern Mono}

% ---- colors (used by both sty files; define here for correct load order) ----
\definecolor{kirinavy}{HTML}{1a5276}
\definecolor{kiriteal}{HTML}{117a65}
\definecolor{kirinavylight}{HTML}{d4e6f1}
\definecolor{kirigray}{HTML}{95a5a6}

% ---- load internal style files ----
\RequirePackage{kiritex-env}
\RequirePackage{kiritex-pagestyle}

% ---- additional settings ----
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.5\baselineskip}
\newcommand{\kiritexversion}{1.0.2}

\AtBeginDocument{%
  \if@kiritex@pad\zihao{-4}\fi
  \pagestyle{kiriheadings}%
}
