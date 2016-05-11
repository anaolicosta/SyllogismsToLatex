from array import array

#To create .csv file with results
from subprocess import call

#To read a .csv file
import csv

#File with methods to incorporate information into a predefined latex encoding
import latexTemplates 
#File with constants used to build path to files
import config


def translateProgram(startClause, endClause, file_name): 
    fh = open(file_name, "r")
    lines = fh.readlines()
    
    latex_program = ""

    for i in range(0,len(lines)-1):
        #Escape commented lines
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


#
# Create a dictionary with elements of the form: 
# Syllogism ID: [[List Predictions by WCS], [List Results Experiments]]
def getEntailmentAndExperiments():
    dict_results = {}
    if config.include_EntailedConclusions or config.include_Experiments:
        #Create .csv
        return_code = call("soffice --headless --convert-to csv " + config.file_ods_results, shell=True)  
        if return_code == 0:
            print "CSV file with results created sucessfully!"
            #Read CSV file
            csv_file = open(config.file_csv_results, 'rb')
            try:
                reader = csv.reader(csv_file)
                #Save line with rows explanation
                #We need to iterate twice to save the second row
                rows_names = reader.next()
                rows_names = reader.next()

                #Get colunms numbers with WCS results
                first_WCS_col = rows_names.index("Aac")
                last_WCS_col = rows_names.index("NVC")

                #Ger colunms numbers with experiments results
                rows_names_no_wcs = rows_names[last_WCS_col+1:]

                first_exp_col = rows_names_no_wcs.index("Aac") + last_WCS_col + 1
                last_exp_col = rows_names_no_wcs.index("NVC") + last_WCS_col + 1

                
                for row in reader:
                    wcs_predictions = []
                    exp_results = []
                    
                    #Entailed conlusions
                    if config.include_EntailedConclusions:
                        i = first_WCS_col
                        for col in row[first_WCS_col:last_WCS_col+1]:
                            if col == '1':
                                wcs_predictions.append(rows_names[i].upper())
                        i = i+1

                    #Results from experiments
                    if config.include_Experiments:
                        i = first_exp_col
                        for col in row[first_exp_col:last_exp_col+1]:
                            if col == '1':
                                exp_results.append(rows_names[i].upper())
                        i = i+1

                    # Indice 0 has the row number
                    dict_results[row[1].lower()] = [wcs_predictions, exp_results]
 
            finally:
                csv_file.close() 
        
        return dict_results

#
# Return a list with two elements: 
# * first: list with atoms that are True
# * second: list with atoms that are False
#
# Attention: It is assumed that there is only one line in the file
def translateLeastModel(syllogism):
    fh = open(config.leastmodels_dir + syllogism + config.leastmodel_file, "r")
    lines = fh.readlines()
    model = lines[0]
    model = model.replace("o", "o_")
    #Abnormalities
    #TODO: Missing negation!!!!
    model = model.replace("abab", r" \Ab_{ab}")
    model = model.replace("abba", r" \Ab_{ba}")
    model = model.replace("abac", r" \Ab_{ac}")
    model = model.replace("abca", r" \Ab_{ca}")
    model = model.replace("abcb", r" \Ab_{cb}")
    model = model.replace("abbc", r" \Ab_{bc}")    
    model = model.translate(None, '.[]')

    return model.split("-", 1)        

fh = open("translate.tex","w")

#Latex file header
fh.write(latexTemplates.latexHeader())

results_entailment_experiment = getEntailmentAndExperiments()

for syllogism in config.generate:
    file_id = syllogism
    syllogism = latexTemplates.formatSyllogism(syllogism)
    
    #Syllogims section
    fh.write(latexTemplates.syllSection(syllogism))

    #Program
    if config.include_Program:
        latex_program = translateProgram("clause(", ").", config.programs_dir + "/" + file_id + config.prolog_file)
        fh.write(latexTemplates.programToTemplate(syllogism, latex_program))

    #Grounded Program
    if config.include_GProgram:
        latex_program = translateProgram("clause_g((", ")).", config.ground_dir + "/" + file_id + config.ground_file)
        fh.write(latexTemplates.gProgramToTemplate(syllogism, latex_program))

    #TODO: Least Model
    if config.include_LeastModel:
        models = translateLeastModel(file_id)
        fh.write("\\\\Least model:\\\\ $\{" + str(models[0]) + " \}$\\\\ $\{" + str(models[1])+ "\}$" )    
    #TODO: EntailedConclusions
    if config.include_EntailedConclusions:
        fh.write("\\\\Entailed conlusions: " + str(results_entailment_experiment[file_id][0]))
    #TODO: Experiments
    if config.include_Experiments:
        fh.write("\\\\Experiments results: " + str(results_entailment_experiment[file_id][1]))

#Latex file footer
fh.write(latexTemplates.latexFooter())

fh.close()


