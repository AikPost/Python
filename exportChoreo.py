document_head=r"""\documentclass[10pt,a4paper]{article}
\usepackage{multirow}
\usepackage[utf8]{inputenc}
\usepackage[dvipsnames]{xcolor}
\usepackage[german]{babel}
\usepackage[T1]{fontenc}
\usepackage{amsmath}
\usepackage{multicol}
\usepackage{amsfonts}
\usepackage{tikz}
\usepackage{tabularx}
\usepackage{amssymb}

\usepackage{makecell}

% Pie chart drawing library
\usepackage{pgf-pie}
\usepackage[left=1cm,right=1cm,top=1cm,bottom=1.5cm]{geometry}
\author{Tobias Post}
\begin{document}


"""

block1=r"""\begin{center}
\begin{LARGE}
"""
#Name des Bildes
block2=r"""\\\noindent\rule{\textwidth}{1pt}
\end{LARGE}
\end{center}
\begin{center}
"""
#scalebox
tikzHead=r"""
\begin{tikzpicture}
\draw[very thin,color=lightgray] (-8,-8) grid (8,8);
\draw[thick] (-8,-8) -- (8,-8);
\draw[thick] (-8,-8) -- (-8,8);
\draw[thick] (8,8) -- (8,-8);
\draw[thick] (8,8) -- (-8,8);
\draw[semithick] (-8,0) -- (8,0);
\draw[semithick] (0,-8) -- (0,8);
\node at (0,9) {Hinten};
\node at (0,-9) {Vorne};
\foreach \x in {-6,-3,0,3,6}
\draw[thin, color=gray, dashed] (\x,8) -- (\x,-8);
\foreach \y in {-6,-3,0,3,6}
\draw[thin, color=gray, dashed] (8,\y) -- (-8,\y);
\foreach \x/\xtext in {-6/-6, -3/-3, 0/0, 3/3, 6/6}
\draw[shift={(\x,8)}] (0pt,2pt) -- (0pt,-2pt) node[above] {$\xtext$};
\foreach \x/\xtext in {-6/-6, -3/-3, 0/0, 3/3, 6/6}
\draw[shift={(\x,-8)}] (0pt,2pt) -- (0pt,-2pt) node[below] {$\xtext$};
\foreach \y/\ytext in {-6/-6, -3/-3, 0/0, 3/3, 6/6}
\draw[shift={(8,\y)}] (2pt,0pt) -- (-2pt,0pt) node[right] {$\ytext$};
\foreach \y/\ytext in {-6/-6, -3/-3, 0/0, 3/3, 6/6}
\draw[shift={(-8,\y)}] (2pt,0pt) -- (-2pt,0pt) node[left] {$\ytext$};
"""
tablehead="""\\begin{tabular}[c]{|>{\\centering\\arraybackslash}p{20pt}|>{\\centering\\arraybackslash}p{60pt}|>{\\centering\\arraybackslash}p{60pt}|>{\\arraybackslash}p{200pt}|}\\hline
Nr & Herren & Damen & Anmerkungen \\\\ \\hline"""


print(document_head,block1,block2)
