\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{esposito-thesis}[2019/03/04 Andrea Esposito's Thesis]

\LoadClass[a4paper,twoside,openright,11pt]{book}

\RequirePackage[inner=3.5cm, outer=2.5cm]{geometry}
\RequirePackage{amssymb}
\RequirePackage[utf8]{inputenc}
\RequirePackage[table,xcdraw]{xcolor}
\definecolor{UniBlue}{HTML}{00388C}
\RequirePackage[explicit]{titlesec}
\RequirePackage{calc}
\RequirePackage{soul}
\RequirePackage{fourier}
\RequirePackage{booktabs}
\RequirePackage{float}
\RequirePackage{wrapfig}
\RequirePackage[labelfont=bf]{caption}
\RequirePackage[labelfont=bf]{subcaption}
\providecommand{\abstract}{}
\RequirePackage{abstract}
\RequirePackage{fancyhdr}
\renewcommand\abstractnamefont{\huge\bfseries\scshape\color{UniBlue}}

\RequirePackage{lettrine}
\setcounter{DefaultLines}{3}

\RequirePackage{hyperref}

% Uncomment for italian
% \def\sectionautorefname{\S}
% \def\subsectionautorefname{\S}
% \def\subsubsectionautorefname{\S}
% \def\tableautorefname{tabella}

\DeclareOption{fancyheader}{\newcommand{\fancyheader}{yes}}
\ProcessOptions\relax

\makeatletter
\@ifundefined{fancyheader}{}{%
	\newsavebox{\feline@chapter}%
	\newcommand\feline@chapter@marker[1][4cm]{%
		\sbox\feline@chapter{%
			\resizebox{!}{#1}{\fboxsep=1pt%
				\colorbox{UniBlue}{\color{white}\bfseries\sffamily\thechapter}%
		}}%
		\rotatebox{90}{%
			\resizebox{%
				\heightof{\usebox{\feline@chapter}}+\depthof{\usebox{\feline@chapter}}}%
			{!}{\scshape\so\@chapapp}}\quad%
		\raisebox{\depthof{\usebox{\feline@chapter}}}{\usebox{\feline@chapter}}%
	}%
	\newcommand\feline@chm[1][4cm]{%
		\sbox\feline@chapter{\feline@chapter@marker[#1]}%
		\makebox[0pt][l]{%
			\makebox[1cm][r]{\usebox\feline@chapter}%
		}%
	}%
	\titleformat{\chapter}[display]{\normalfont}{\hfill\feline@chm[2.5cm]}{0pt}{\flushright\huge\bfseries\scshape\color{UniBlue}{#1}}[\vspace*{2ex}]%
	\titlespacing*{\chapter}{0pt}{0ex}{2ex}%
}
\makeatother


% --- Comandi per la pagina del titolo --- %

\makeatletter
\newcommand\university[1]{\renewcommand\@university{#1}}
\newcommand\@university{}
\newcommand\supervisor[1]{\renewcommand\@supervisor{#1}}
\newcommand\@supervisor{}
\newcommand\degreetype[1]{\renewcommand\@degreetype{#1}}
\newcommand\@degreetype{}
\newcommand\course[1]{\renewcommand\@course{#1}}
\newcommand\@course{}
\newcommand\department[1]{\renewcommand\@department{#1}}
\newcommand\@department{}
\makeatother

% --- La pagina del titolo --- %
\makeatletter
\def\maketitle{%
	\null
	\pagestyle{empty}
	\begin{center}
		\includegraphics[width=7cm]{UniBa}\\[1cm]
		\vspace*{\fill}
		\textsc{\@degreetype{} in}\\
		\textsc{\large\color{UniBlue} \@course}\\[5mm]
		\rule[0.5ex]{\linewidth}{1pt}\\[\baselineskip]
		{\huge \textsc{\@title}\\[4mm]}
		\rule[0.5ex]{\linewidth}{1pt}\vspace*{\baselineskip}
		\vspace{1cm}
		\begin{minipage}[t]{0.5\textwidth}
			\begin{flushleft} \large
				\emph{Author:}\\
				{\color{UniBlue} \@author~({\small 677021})}
			\end{flushleft}
		\end{minipage}%
		\begin{minipage}[t]{0.5\textwidth}
			\begin{flushright} \large
				\emph{Supervisor:} \\
				{\color{UniBlue} \@supervisor}
			\end{flushright}
		\end{minipage}\\
		\vspace{11mm}
		{\large \@department\\
			\textsc{\color{UniBlue} \@university}}\\
		\vspace*{20mm}
		{\large\textsc{\@date}}
	\end{center}
	\vspace*{\fill}
}
\makeatother

\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE,RO]{\leftmark}
\fancyhead[RE,LO]{\rightmark}
\fancyfoot[CE,CO]{}
\fancyfoot[LE,RO]{\thepage}
\renewcommand{\headrulewidth}{1pt}
  \renewcommand{\footrulewidth}{1pt}

\fancypagestyle{plain}{ %
  \fancyhf{} % remove everything
  \fancyfoot[LE,RO]{\thepage}
  \renewcommand{\headrulewidth}{0pt} % remove lines as well
  \renewcommand{\footrulewidth}{1pt}
}
