import re

# String with program's prolog encoding to be use in the regular expression
program_pattern = r"([\w\(\)']+)\ ?:\-\ ?\[([\w,\(\)']+)\]"

# Regular expressions for programs and groundded programs
program_base_pattern = re.compile(r"clause\(" + program_pattern + "\)\.(\n)?")
gprogram_base_pattern = re.compile(r"clause_g\(\(" + program_pattern + "\)\)\.(\n)?")


#### Configures behavior

# File name for latex file to create
latexFileName = "syllogisms.tex"

#Pattern of our experiments. This is used to build the folder path.
pattern = "1212"

#Title of document
doc_Title = "Syllogisms with pattern " + pattern

#
#Syllogisms to generate

#78
#generate = ['aa2', 'aa4', 'ai4', 'ae4', 'ao2', 'ia2', 'ia3','ia4','ii2','ie3','io2','ea4','ei3','ee2','eo1','oa1','oa2','oa3','oi1','oe1']
#65
#generate = ['ae3', 'ie2','ie4','ea3','ei4']
generate = []
#
#Information to include in latex file
#
include_Program = True
include_GProgram = True
include_LeastModel = True
include_EntailedConclusions = True
include_Experiments = True


#### Settings related with folders and files

# Base directory
file_dir = "../" + pattern + "/" 

#
#Inside of Base  directory we have the following folders:
# * groundP : result of grounding
# * leastmodels : least models computed by Prolog
# * Programs : Schema for programs
# And an .ods file with the results
#
#Sub directories
ground_dir = file_dir + "groundP/"
leastmodels_dir = file_dir + "leastmodels/"
programs_dir = file_dir + "Programs/"

#.ods file with results
file_ods_results = file_dir + "overview-" + pattern +".ods"

#
#Each type of file output from Prolog has a different termination
#
prolog_file = ".pl"
ground_file = "g.pl"
leastmodel_file = "glm.pl"

# File created in the folder where python is running with results in .csv format
file_csv_results = "overview-" + pattern + ".csv"

