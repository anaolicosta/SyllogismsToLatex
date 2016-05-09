# Base directory
file_dir = ""

""" 
Inside of Base  directory we have the following folders:
* groundP : result of grounding
* leastmodels : least models computed by Prolog
* Programs : Schema for programs
"""

#Sub directories
#TO CHECK: Do we need to take care of // and /??
gound_dir = file_dir + "groundP"
leastmodels_dir = file_dir + "leastmodels"
programs_dor = file_dir + "Programs"

"""
Each type of file can have a different termintation
"""
# Termination of files
prolog_file = ".pl"
ground_file = "g.pl"
leastmodel_file = "glm.pl"

