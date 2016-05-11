# Base directory
file_dir = "../"

""" 
Inside of Base  directory we have the following folders:
* groundP : result of grounding
* leastmodels : least models computed by Prolog
* Programs : Schema for programs
"""

#Sub directories
ground_dir = file_dir + "groundP//"
leastmodels_dir = file_dir + "leastmodels//"
programs_dir = file_dir + "Programs//"

"""
Each type of file can have a different termintation
"""
# Termination of files
prolog_file = ".pl"
ground_file = "g.pl"
leastmodel_file = "glm.pl"

"""
Syllogisms to generate
"""
generate = ['ae3', 'ie4', 'ie2', 'ea4', 'ei4']

"""
Pattern
"""
pattern = "1212"

"""
Information to include
"""
include_Program = True
include_GProgram = True
include_LeastModel = True
include_EntailedConclusions = True
include_Experiments = True
