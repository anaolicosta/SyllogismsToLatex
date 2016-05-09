
"""
File with variables related with location of paths
and identification of relevant files.
"""

import config_folders

"""
Building the syllogisms
"""
moods = ['a','e','i','o']
syllogisms = []
for i in range(1,5):
    for mood in moods:
	for mood2 in moods:
            syllogisms.append(mood + mood2 + str(i))

print "My syl: %s \nLenght: %s" % (syllogisms, len(syllogisms))






