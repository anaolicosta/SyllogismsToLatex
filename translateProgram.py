from array import array

import latexTemplates 
import config


def translateProgram(startClause, endClause, file_name): 
    #raw_input("File name: ")

    fh = open(file_name, "r")
    lines = fh.readlines()
    
    latex_program = ""

    for i in range(0,len(lines)-1):
        if lines[i][0] != '%':
            new_line = lines[i]
            #Objects
            #This need to be done BEFORE translating implication
            new_line = new_line.replace("o", "o_")
            #Implication
            new_line = new_line.replace(":-", r" \leftarrow ")
            #Conjunction
            new_line = new_line.replace(",", r" \wedge ")
            #Negation
            new_line = new_line.replace("n(", r" \neg ")
            #Abnormalities
            new_line = new_line.replace("abab", r" \Ab_{ab}")
            new_line = new_line.replace("abba", r" \Ab_{ba}")
            new_line = new_line.replace("abac", r" \Ab_{ac}")
            new_line = new_line.replace("abca", r" \Ab_{ca}")
            new_line = new_line.replace("abcb", r" \Ab_{cb}")
            new_line = new_line.replace("abbc", r" \Ab_{bc}")    
            #Top
            new_line = new_line.replace("[t]", r" \top ")
            #Bottom
            new_line = new_line.replace("[f]", r" \bot ")
            #Add reference to new line
            new_line = new_line.replace("\n", "\\\\ \n")
            #To delete. Do it just in the end.
            new_line = new_line.replace(startClause, "")
            new_line = new_line.replace(endClause, "")
            new_line = new_line.replace("))", ")")    
            new_line = new_line.translate(None, '.[]')

            #new_lines.append(new_line + r"\\ \n")
            latex_program = latex_program + new_line

    #Take the last new line
    return latex_program[:len(latex_program)-1]




fh = open("translate.tex","w")

fh.write(latexTemplates.latexHeader())

syllogism = "aa1"

fh.write(latexTemplates.syllSection(syllogism))

latex_program = translateProgram("clause(", ").", "../1212/" + config.programs_dir + "/" + syllogism + config.prolog_file)

fh.write(latexTemplates.programToTemplate(syllogism, latex_program))

latex_program = translateProgram("clause_g((", ")).", "../1212/" + config.ground_dir + "/" + syllogism + config.ground_file)
fh.write(latexTemplates.gProgramToTemplate(syllogism, latex_program))


fh.write(latexTemplates.latexFooter())
fh.close()


