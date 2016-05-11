#### Configures behavior

#Pattern of our experiments. This is used to build the folder path.
pattern = "1212"

#
#Syllogisms to generate
#
generate = ['ae3', 'ie4', 'ie2', 'ea4', 'ei4']

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

