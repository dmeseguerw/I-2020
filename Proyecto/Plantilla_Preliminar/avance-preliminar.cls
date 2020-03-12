% ------------------------------------
% Universidad de Costa Rica
% Facultad de Ingeniería
% Escuela de Ingeniería Eléctrica
% IE0499 - Proyecto Eléctrico
%
% CLASE DE LATEX DEL AVANCE PRELIMINAR
% ------------------------------------

% Declaraciones iniciales
% -----------------------

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{avance-preliminar}[2020/03/09 Avance Preliminar del Proyecto Eléctrico de Ingeniería Eléctrica - UCR]

% Documento con espacios vacíos
\newif\ifvacio
\DeclareOption{vacio}{\vaciotrue}

% Cualquier otra opción se pasa a 'memoir'
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}

% Procesar las opciones
\ProcessOptions\relax

% Cargar la clase base ('article')
% --------------------------------

\LoadClass[letterpaper]{article}

% Paquetes requeridos
% -------------------

% General
\RequirePackage[spanish]{babel}
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{lipsum}
\RequirePackage{array}
\RequirePackage{multicol}

% Nuevos comandos especiales
% --------------------------
\newcolumntype{C}[1]{>{\centering\arraybackslash}m{#1}}

\newcommand{\linea}[1]{$\vcenter{\hbox{\rule{#1}{0.1pt}}}$}

\newcommand{\ajustado}{\itemsep0pt\parskip0pt\parsep0pt}

\ifvacio
	\newcommand{\seleccionar}{\raisebox{4pt}{\circle{8}}}
\else
	\newcommand{\seleccionar}[1]{\raisebox{4pt}{\circle#1{8}}}
\fi

% Tipografía
% ----------
\usepackage{libertine}
\usepackage[T1]{fontenc}
\renewcommand*{\ttdefault}{cmtt}

% Formato de la página y área de escritura
% ----------------------------------------
\usepackage{geometry}                         
	\geometry{left=21mm,right=21mm,top=21mm,bottom=21mm}
    
% Textos predefinidos
\newcommand{\UCR}{Universidad de Costa Rica}
\newcommand{\FI}{Facultad de Ingeniería}
\newcommand{\EIE}{Escuela de Ingeniería Eléctrica}
\newcommand{\PE}{IE0499 -- Proyecto Eléctrico}
\newcommand{\por}{por}
\newcommand{\lugar}{Ciudad Universitaria Rodrigo Facio}
\newcommand{\ante}{Avance preliminar}
\newcommand{\introestudiante}{Estudiante}
\newcommand{\introguia}{Profesor guía}
\newcommand{\introlectorA}{Profesor lector}
\newcommand{\introlectorB}{Profesor lector}

% Definición de datos globales del avance preliminar
% --------------------------------------------------

\def\titulo#1{\gdef\@titulo{#1}}
\def\autor#1{\gdef\@autor{#1}}
\def\carne#1{\gdef\@carne{#1}}
\def\email#1{\gdef\@email{#1}}
\def\telefono#1{\gdef\@telefono{#1}}
\def\guia#1{\gdef\@guia{#1}}
\def\eguia#1{\gdef\@eguia{#1}}
\def\lectorA#1{\gdef\@lectorA{#1}}
\def\electorA#1{\gdef\@electorA{#1}}
\def\lectorB#1{\gdef\@lectorB{#1}}
\def\fecha#1{\gdef\@fecha{#1}}
\def\electorB#1{\gdef\@electorB{#1}}
\def\sem#1{\gdef\@sem{#1}}
\def\ano#1{\gdef\@ano{#1}}

% 1. Formato de encabezado
% ------------------------

\newcommand{\encabezado}{
\thispagestyle{empty}
%\pdfbookmark[1]{Portada}{portada}
\begin{center}
	{\Large\bfseries\scshape\UCR}
    \vskip 0.6em
    {\Large\bfseries\FI}
    \vskip 0.5em
    {\Large\bfseries\EIE}
	\vskip 2em
    {\large\bfseries\PE}
    \vskip 1em
    {\LARGE\bfseries\ante}
    \vskip 1em
    {\@sem\ -- \@ano}
	\vskip 2em
\end{center}
}

% 2. Instrucciones
% ----------------

\newcommand{\instrucciones}{
\begin{itemize}\itemsep0pt
\item El avance preliminar representa la formalización entre el estudiante y los profesores para trabajar en un tema determinado.
\item Esta es una propuesta inicial y puede sufrir modificaciones. Aún así, el trabajo debe ser similar en alcance e intensidad.
\item El documento debe ser impreso y firmado. Se entrega al coordinador del curso.
\end{itemize}
}

% 3. Formato de los datos del estudiante
% --------------------------------------

\newcommand{\estudiante}{
\vspace{2mm}\noindent
\begin{tabular}{p{9cm}p{3cm}}
	\ifvacio\else\@autor\fi
	& \ifvacio\else\@carne\fi
	\\
	\linea{8cm} 
	& \linea{2cm}
	\\ 
	{\itshape Nombre completo}
	& {\itshape Carné}
\end{tabular}

\vspace{1em}
\noindent
\begin{tabular}{p{8cm}p{4cm}}
 	\ifvacio\else\@email\fi
	& \ifvacio\else\@telefono\fi
	\\
	\linea{7cm}
	& \linea{3cm}
	\\ 
	{\itshape Correo electrónico}
	& {\itshape Teléfono}
\end{tabular}
}

% 4. Formato de los datos del profesor guía
% -----------------------------------------

\newcommand{\profesorguia}{
\vspace{2mm}\noindent
\begin{tabular}{p{9cm}p{7cm}}
	\ifvacio\else\@guia\fi
	& \ifvacio\else\@eguia\fi
	\\
	\linea{8cm}
	& \linea{6cm}
	\\ 
	{\itshape Nombre completo}
	& {\itshape Correo electrónico}
\end{tabular}
}

% 5. Formato de los datos de los profesores lectores
% --------------------------------------------------

\newcommand{\profesoreslectores}{
\vspace{2mm}\noindent
\begin{tabular}{p{9cm}p{7cm}}
	\ifvacio\else\@lectorA\fi
	& \ifvacio\else\@electorA\fi
	\\
	\linea{8cm}
	& \linea{6cm} 
	\\ 
	{\itshape Nombre completo} \vspace{1em}
	& {\itshape Correo electrónico} \vspace{1em}
\end{tabular}

\noindent
\begin{tabular}{p{9cm}p{7cm}}
	\ifvacio\else\@lectorB\fi
	& \ifvacio\else\@electorB\fi
	\\
	\linea{8cm} 
	& \linea{6cm} 
	\\ 
	{\itshape Nombre completo}
	& {\itshape Correo electrónico}
\end{tabular}
}

% 6. El título
% ------------

\newcommand{\eltitulo}{
\begin{center}
\large\itshape 
\ifvacio\else\@titulo\fi
\end{center}
}

% 7. Formato de las firmas
% ------------------------

\newcommand{\firmas}{
\begin{center}
\vspace{4em}
\begin{tabular}{C{8cm}C{8cm}}
	\linea{7cm}
	& \linea{7cm}
	\\
	\ifvacio\else\large\normalfont\@guia\fi
	& \ifvacio\else\large\normalfont\@autor\fi 
	\\ 
	\large\itshape\introguia \vspace{4em}
	& \large\itshape\introestudiante \vspace{4em}
	\\ 
	\linea{7cm} 
	& \linea{7cm} 
	\\
	\ifvacio\else\large\normalfont\@lectorA\fi
	& \ifvacio\else\large\normalfont\@lectorB\fi
	\\ 
	\large\itshape\introlectorA 
	& \large\itshape\introlectorB
\end{tabular}
\end{center}
}

%%%%%%%%%
\endinput
%%%%%%%%%
