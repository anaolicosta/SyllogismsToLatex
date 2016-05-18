from array import array

#To create .csv file with results
from subprocess import call

#To read a .csv file
import csv

#Regular expressions
import re

#File with methods to incorporate information into a predefined latex encoding
import latexTemplates 

#File with constants used to build path to files
import config


#
# Read prolog file and return a string with the program in latex format
def translateProgram(pattern, file_name): 
    fh = open(file_name, "r")
    lines = fh.readlines()
    
    latex_program = ""

    for i in range(0,len(lines)):
        #Escape commented lines
        if lines[i][0] != '%':
            new_line = lines[i]
            #Objects
            #This need to be done BEFORE translating implication
            new_line = new_line.replace("o", "o_")
            #Main pattern. Clean most of the stuff
            new_line = re.sub(pattern,r"\1 \leftarrow \2 \n", new_line)
            #Abnormalities
            new_line = translateAbnormalities(new_line)
            #Conjunction
            new_line = new_line.replace(",", r" \wedge ")
            #Negation atoms 
            new_line = new_line.replace("na", "a'") 
            new_line = new_line.replace("nb", "b'")
            new_line = new_line.replace("nc", "c'")
            #Add reference to new line
            new_line = new_line.replace("\n", "\\\\ \n")
            #Negation
            new_line = new_line.replace("n(", r"\neg ")
            #Top
            new_line = new_line.replace(r"t \\", r" \top \\")
            #Bottom
            new_line = new_line.replace(r"f \\", r" \bot \\")
            #To delete. Do it just in the end.
            new_line = new_line.replace("))", ")")    

            latex_program = latex_program + new_line

    #Take the last new line
    return latex_program


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

                #Get colunms numbers with experiments results
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
    #Objects
    model = model.replace("o", "o_")
    #Abnormalities
    model = translateAbnormalities(model)
    #Negation atoms 
    model = model.replace("na", "a'") 
    model = model.replace("nb", "b'")
    model = model.replace("nc", "c'")
    model = model.translate(None, "[]")
    return model.split("-", 1)        


#
# Replace each ab* by its latex abbreviation \Ab_{*}
def translateAbnormalities(str):
    return re.sub(r"(ab)([\w']+)", r"\Ab_{\2}", str)



# Create file
fh = open(config.latexFileName,"w")
#Add Latex file header
fh.write(latexTemplates.latexHeader())

# Get results of entailment and experiments
# Each of those  will only be evaluted with config.include_EntailedConclusions
# or config.include_Experiments are set to True, resp.
results_entailment_experiment = getEntailmentAndExperiments()

# Iterate through each syllogism listed in config.generate
# TODO: Add possibility of having this list empyt, then it should
# iterate over all syllogisms
syllToGenerate = []
if len(config.generate) > 0:
    syllToGenerate = config.generate
else:
    moods = ['a','i','e','o']
    for mood1 in moods:
        for mood2 in moods:
            for figure in ['1','2','3','4']:
                syllToGenerate.append(mood1 + mood2 + figure )

for syllogism in syllToGenerate:

    file_id = syllogism
    syllogism = latexTemplates.formatSyllogism(syllogism)
    
    #Syllogims section
    fh.write(latexTemplates.syllSection(syllogism))

    #Program
    if config.include_Program:
        latex_program = translateProgram(config.program_base_pattern, config.programs_dir + "/" + file_id + config.prolog_file)
        fh.write(latexTemplates.programToTemplate(syllogism, latex_program))

    #Grounded Program
    if config.include_GProgram:
        latex_program = translateProgram(config.gprogram_base_pattern, config.ground_dir + "/" + file_id + config.ground_file)
        fh.write(latexTemplates.gProgramToTemplate(syllogism, latex_program))

    #Least Model
    if config.include_LeastModel:
        models = translateLeastModel(file_id)
        fh.write(latexTemplates.leastModelToTemplate(syllogism, models[0], models[1]))    
    #EntailedConclusions
    if config.include_EntailedConclusions:
        entailed = str(results_entailment_experiment[file_id][0])
        #Remove '[' and ']'
        entailed = entailed[1:len(entailed)-1]
        fh.write(latexTemplates.entailedToTemplate(entailed))

    #Experiments
    if config.include_Experiments:
        experiments = str(results_entailment_experiment[file_id][1])
        #Remove '[' and ']'
        experiments = experiments[1:len(experiments)-1]
        fh.write(latexTemplates.experimentsToTemplate(experiments))

#Latex file footer
fh.write(latexTemplates.latexFooter())

fh.close()


