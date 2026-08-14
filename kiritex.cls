\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{kiritex}[2026/08/14 v1.0.3 KiriTeX problem workbook template]

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

% Load base class. Body sizes are set explicitly via \zihao in \AtBeginDocument
% because the zihao class option only supports 5, -4, false in TL2026.
\LoadClass[a4paper]{ctexart}

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
\newcommand{\kiritexversion}{1.0.3}

\AtBeginDocument{%
  \if@kiritex@pad
    \zihao{5}%    Pad: 五号 (10.5pt)
  \else
    \zihao{-5}%   A4:  小五 (9pt)
  \fi
  \pagestyle{kiriheadings}%
}
