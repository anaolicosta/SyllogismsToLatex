import config

#
#Translate a syllogism to its Latex representation
#using the correspondent abbreviation.
#Example: 'aa1' is translated to '\MA\MA 1'
def formatSyllogism(syllogism):
    formattedSyll = syllogism.upper()
    return "\\M"+ formattedSyll[0] + "\\M" + formattedSyll[1] + " " + formattedSyll[2]

#
#Header for the latex file.
#Define type of latex file, packages to include, title of the document,...
def latexHeader():
    header = r"""\documentclass[11pt]{article}
\usepackage{amssymb} 
\usepackage{amsmath}
\input{abbreviations} 

\title{\textbf{""" + config.doc_Title + r"""}}
\date{\today}

\begin{document}
%--------------------Title Page
\maketitle
     
\newpage
"""
    return header

#
#Ends Latex document.
def latexFooter():
    return "\end{document}"

#
#Add section for a given syllogism.
def syllSection(syllogism):
    return "\section{%s} \n" % syllogism

#
#Returns the program already translated to latex notation
#included already in our Latex template for programs.
def programToTemplate(syllogism, latex_program):
    program = """$\CalP_{%s}$ consists of the following clauses:
\[
 \\begin{array}{lll}
 %s
 \end{array}
\]
 """ % (syllogism, latex_program)
    return program
#
#Returns the grounded program already translated to latex notation
#included already in our Latex template for grounded programs.
def gProgramToTemplate(syllogism, latex_program):
    program = """The grounded version of $\CalP_{%s}$ is as follows:
\[
 \\begin{array}{l}
 %s
 \end{array}
\]
 """ % (syllogism, latex_program)
    return program

#
#Returns the least model already translated to latex notation
#included already in our latex template for least models.
def leastModelToTemplate(syllogism, trueModel, falseModel):
    leastModelTemplate = """The least \L-model of $\CalP_{%s}$ is
\[
\\begin{array}{llllllllll}
\langle & \{ %s\}, \\\\ 
 & \{ %s \} & \\rangle.
 \end{array}
 \] 
""" % (syllogism, trueModel, falseModel)
    return leastModelTemplate

#
#Returns the entailed conclusions already translated to latex notation
#included already in our latex template for least models.
def entailedToTemplate(entailed_conclusions, accuracy):
    entailedTemplate = """
Our entailed conclusions are: %s 
\n With accuracy: %s    
    """ % (entailed_conclusions,accuracy) 
    return entailedTemplate

#
#Returns the experiments results already translated to latex notation
#included already in our latex template for least models.
def experimentsToTemplate(experiments_results):
    resultsTemplate = """
The experiments results are: %s 
    """ % experiments_results
    return resultsTemplate
