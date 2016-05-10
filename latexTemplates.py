def latexHeader():
    header = r"""\documentclass[11pt]{article}
\usepackage{amssymb} 
\usepackage{amsmath}
\input{abbreviations} 

\title{\textbf{Translation Syllogisms}}
\date{\today}

\begin{document}
%--------------------Title Page
\maketitle
     
\newpage
"""
    return header

def latexFooter():
    return "\end{document}"

def programToTemplate(syllogism, latex_program):
    program = """$\CalP_{%s}$ consists of the following clauses:
\[
 \\begin{array}{l}
 %s
 \end{array}
\]
 """ % (syllogism, latex_program)
    return program

def syllSection(syllogism):
    return "\section{%s} \n" % syllogism

def gProgramToTemplate(syllogism, latex_program):
    program = """The grounded version of $\CalP_{%s}$ is as follows:
\[
 \\begin{array}{l}
 %s
 \end{array}
\]
 """ % (syllogism, latex_program)
    return program


def minimalModelToTemplate(syllogism, trueModel, falseModel):
    minimalModelTemplate = """The least \L-model of $\CalP_{%s}$ is
\[
\\begin{array}{llllllllll}
\langle & \{ %s\}, \\ 
 & \{ %s \} & \\rangle.
 \end{array}
 \] 
""" % (syllogism, trueModel, falseModel)
    return minimalModelTemplate
