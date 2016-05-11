from array import array

#File with methods to incorporate information into a predefined latex encoding
import latexTemplates 
#File with constants used to build path to files
import config


def translateProgram(startClause, endClause, file_name): 
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
            #Negation 
            #This needs to be done BEFORE Abnormalities, to keep nx inside of them
            new_line = new_line.replace("na", "a'") 
            new_line = new_line.replace("nb", "b'")
            new_line = new_line.replace("nc", "c'")
            #Abnormalities
            #TODO: Missing negation!!!!
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

#Latex file header
fh.write(latexTemplates.latexHeader())

directory = config.file_dir + config.pattern + "//"

for syllogism in config.generate:
    file_id = syllogism
    syllogism = latexTemplates.formatSyllogism(syllogism)
    
    #Syllogims section
    fh.write(latexTemplates.syllSection(syllogism))

    #Program
    if config.include_Program:
        latex_program = translateProgram("clause(", ").", directory + config.programs_dir + "/" + file_id + config.prolog_file)
        fh.write(latexTemplates.programToTemplate(syllogism, latex_program))

    #Grounded Program
    if config.include_GProgram:
        latex_program = translateProgram("clause_g((", ")).", directory + config.ground_dir + "/" + file_id + config.ground_file)
        fh.write(latexTemplates.gProgramToTemplate(syllogism, latex_program))

    #TODO: Least Model

    #TODO: EntailedConclusions

    #TODO: Experiments

#Latex file footer
fh.write(latexTemplates.latexFooter())

fh.close()


