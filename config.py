import re

# Program's Prolog encoding pattern (used to process Prolog file)
program_pattern = r"([\w\(\)']+)\ ?:\-\ ?\[([\w,\(\)']+)\]"

# Regular expressions for programs and grounded programs
program_base_pattern = re.compile(r"clause\(" + program_pattern + "\)\.(\n)?")
gprogram_base_pattern = re.compile(r"clause_g\(\(" + program_pattern + "\)\)\.(\n)?")


#### Configures behavior

# Latex related config 

## Latex file name
latexFileName = "outputLatex/syllogisms.tex"

## Title of Latex document
doc_Title = "Check entailment"
#"Syllogisms with pattern " + pattern + " - Prediction for E mood"

## Syllogisms to generate
#78
#generate = ['aa2', 'aa4', 'ai4', 'ae4', 'ao2', 'ia2', 'ia3','ia4','ii2','ie3','io2','ea4','ei3','ee2','eo1','oa1','oa2','oa3','oi1','oe1']
#65
#generate = ['ae3', 'ie2','ie4','ea3','ei4']
#generate = []
#generate = ['ea1', 'ei1', 'ee1', 'eo1', 'ea3', 'ei3', 'ee3', 'eo3', 'ae3', 'ie3', 'oe3', 'ae2', 'ie2', 'ee2', 'oe2']
#generate = ['ea1', 'ee1', 'ea3', 'ee3', 'ae3','ae2', 'ee2']
generate = []

# filters for syllogisms, first element identifies type of filter, next elements are arguments:
#
# * [entails, syl_entails,...] : 
#    syl_entails - syllogisms to print in latex should entail at least one of the listed
#                  entailments (Aac,Eac,Iac,Oac,Aca,Eca,Ica,Oca or NVC)
# 
# * [results, syl_entails,...] : 
#    syl_entails -  syllogisms to print in latex should have as empirical results at least 
#                   one of the listed entailments (Aac,Eac,Iac,Oac,Aca,Eca,Ica,Oca or NVC)

#generate_filter= [['entails','NVC'],['results','NVC']]
generate_filter= [['results','NVC']]


## Information to include in latex file
include_Program = True
include_GProgram = False
include_LeastModel = True
include_EntailedConclusions = True
include_Experiments = True


# Settings related with folders and files

## Pattern of our experiments (this is used to build the folder path)
pattern = "1212"

## Base directory of experimental results
file_dir = "../" + pattern + "/" 


## Sub directories
#
#Inside of Base  directory we have the following folders:
# * groundP : result of grounding
# * leastmodels : least models computed by Prolog
# * Programs : Schema for programs
# And an .ods file with the results
#
ground_dir = file_dir + "groundP/"
leastmodels_dir = file_dir + "leastmodels/"
programs_dir = file_dir + "Programs/"

## .ods file with results
file_ods_results = file_dir + "overview-" + pattern +".ods"

## File terminations
#
#Each type of file output from Prolog has a different termination
#
prolog_file = ".pl"
ground_file = "g.pl"
leastmodel_file = "glm.pl"

## File created in the folder where python is running with results in .csv format
file_csv_results = "overview-" + pattern + ".csv"

