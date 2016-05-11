"""
Translate a syllogism to its Latex representation
using the correspondent abbreviature.
Example: 'aa1' is translated to '\MA\MA 1'
"""
def formatSyllogism(syllogism):
    formattedSyll = syllogism.upper()
    return "\\M"+ formattedSyll[0] + "\\M" + formattedSyll[1] + " " + formattedSyll[2]

"""
Header for the latex file.
Define type of latex file, packages to include, title of the document,...
"""
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

"""
Ends Latex document.
"""
def latexFooter():
    return "\end{document}"

"""
Add section for a given syllogism.
"""
def syllSection(syllogism):
    return "\section{%s} \n" % syllogism

"""
Returns the program already translated to latex notation
inserted in our Latex template for programs.
"""
def programToTemplate(syllogism, latex_program):
    program = """$\CalP_{%s}$ consists of the following clauses:
\[
 \\begin{array}{l}
 %s
 \end{array}
\]
 """ % (syllogism, latex_program)
    return program
"""
Returns the grounded program already translated to latex notation
inserted in our Latex template for grounded programs.
"""
def gProgramToTemplate(syllogism, latex_program):
    program = """The grounded version of $\CalP_{%s}$ is as follows:
\[
 \\begin{array}{l}
 %s
 \end{array}
\]
 """ % (syllogism, latex_program)
    return program

"""
Returns the least model already translated to latex notation
inserted in out latex template for least models.
"""
def leastModelToTemplate(syllogism, trueModel, falseModel):
    leastModelTemplate = """The least \L-model of $\CalP_{%s}$ is
\[
\\begin{array}{llllllllll}
\langle & \{ %s\}, \\ 
 & \{ %s \} & \\rangle.
 \end{array}
 \] 
""" % (syllogism, trueModel, falseModel)
    return minimalModelTemplate
