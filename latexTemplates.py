def latexHeader():
    #TODO Define
    header = """
    """
    return header


def programToTemplate(syllogism, latex_program):
    program = """$\CalP_{%s}$ consists of the following clauses:
\[
 \\begin{array}{l}
 %s
\]
 """ % (syllogism, latex_program)
    return program



def gPr:ogramToTemplate(syllogism, latex_program):
    program = """The grounded version of $\CalP_{%s}$ is as follows:
\[
 \\begin{array}{l}
 %s
\]
 """ % (syllogism, latex_program)
    return program


def minimalModelToTemplate(syllogism, trueModel, falseModel):
    minimalModelTemplate = """The least \L-model of $\CalP_{%s}$ is
\[
\\begin{array}{llllllllll}
\langle & \{ %s\}, \\ 
 & \{ %s \} & \rangle.
 \end{array}
 \] 
""" % (syllogism, trueModel, falseModel)
    return minimalModelTemplate
