from array import array

#To create .csv file with results
from subprocess import call

#To read a .csv file
import csv

#Regular expressions
import re

#File with methods to incorporate information into a predefined latex encoding
import latexTemplates 

#File with constants that configure behavior of this script
import config


#
# Read prolog file and return a string with program in latex format
#
# Input: 
# -> Pattern to analyze
# -> Name of the file to generate
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
            new_line = re.sub(pattern,r"\1 & \leftarrow & \2 \n", new_line)
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
#
# This dictionary is built from information in .csv file
def getEntailmentAndExperiments():
    dict_results = {}
    # This method is only needed when the we want the data 
    # from entailed conclusions or experimental results
    # in the latex file.
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

                #Get columns numbers with WCS results
                first_WCS_col = rows_names.index("Aac")
                last_WCS_col = rows_names.index("NVC")

                #Get columns numbers with experiments results
                rows_names_no_wcs = rows_names[last_WCS_col+1:]

                first_exp_col = rows_names_no_wcs.index("Aac") + last_WCS_col + 1
                last_exp_col = rows_names_no_wcs.index("NVC") + last_WCS_col + 1

                #Iterate over each row in the file
                for row in reader:
                    wcs_predictions = []
                    exp_results = []
                    
                    #Entailed WCS conclusions
                    if config.include_EntailedConclusions:
                        i = first_WCS_col
                        for col in row[first_WCS_col:last_WCS_col+1]:
                            if col == '1':
                                if rows_names[i].find("NVC")>-1:
                                    wcs_predictions.append('\NVC')
                                else:
                                    wcs_predictions.append('\M' + rows_names[i][0]+ ' '+ rows_names[i][1:])
                            i = i+1
                        #Accuracy. 
                        #Gets last element in the row
                        wcs_predictions.append(row[-1])

                    #Results from experiments
                    if config.include_Experiments:
                        i = first_exp_col
                        for col in row[first_exp_col:last_exp_col+1]:
                            if col == '1':
                                if rows_names[i].find("NVC")>-1:
                                    exp_results.append('\NVC')
                                else:
                                    exp_results.append('\M' + rows_names[i][0]+ ' '+ rows_names[i][1:] )
                            i = i+1

                    #Index 0 has the row number
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


##### This is where the magic starts :-D 

# Create file
fh = open(config.latexFileName,"w")
#Add Latex file header
fh.write(latexTemplates.latexHeader())

# Get results of entailment and experiments
# Each of those  will only be evaluated if 
# config.include_EntailedConclusions
# or config.include_Experiments 
# are set to True, resp.
results_entailment_experiment = getEntailmentAndExperiments()

# Iterate through each syllogism listed in config.generate
# If the list is empty it iterated through all the syllogisms.
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

    isToAddToFile = (len(config.generate_filter) == 0)
    for config_filter in config.generate_filter:
        
        if config_filter[0] == 'entails':
            #Check if at least one of the entailnments is listed
            #in the property.
            for entailed in results_entailment_experiment[file_id][0]:
                isToAddToFile |= (entailed in config_filter[1:]) 
                
        elif config_filter[0] == 'results':
            #Check if at least one of the results is listed
            #in the property.
            for entailed in results_entailment_experiment[file_id][1]:
                isToAddToFile |= (entailed in config_filter[1:]) 



    if isToAddToFile:
        syllogism = latexTemplates.formatSyllogism(syllogism)
        
        #Syllogism section
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
              
        #Entailed Conclusions
        if config.include_EntailedConclusions:
            entailed = results_entailment_experiment[file_id][0]
            entailed_conclusions = entailed[0]
            for entail in entailed[1:-1]:
                entailed_conclusions = entailed_conclusions + ", " + entail
            fh.write(latexTemplates.entailedToTemplate(entailed_conclusions, str(entailed[-1])))
    
        #Experiments
        if config.include_Experiments:
            exp_results = results_entailment_experiment[file_id][1]
            experiments = exp_results[0]
            for experiment in exp_results[1:-1]:
                experiments = experiments + ", " + experiment
            fh.write(latexTemplates.experimentsToTemplate(experiments))

#Latex file footer
fh.write(latexTemplates.latexFooter())

fh.close()


