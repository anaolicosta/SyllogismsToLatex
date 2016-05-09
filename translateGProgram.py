from array import array


file_name = "../1212/groundP/aa1g.pl" 
#raw_input("File name: ")

fh = open(file_name, "r")
lines = fh.readlines()
new_lines = []

name_clause = "clause_g(("
termination_clause ="))."

for i in range(0,len(lines)-1):
    new_line = lines[i]
    #Objects 
    #This need to be done BEFORE translating the implication
    new_line = new_line.replace("o", "o_")
    #Implication
    new_line = new_line.replace(":-", r" \leftarrow ")
    #Conjunction
    new_line = new_line.replace(",", r" \wedge ")
    #Negation
    new_line = new_line.replace("n(", r" \neg ")
    #Abnormalities
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
    #To delete. Do it just in the end.
    new_line = new_line.replace(name_clause, "")
    new_line = new_line.replace(termination_clause, "")
    new_line = new_line.replace("))", ")")    
    new_line = new_line.translate(None, '.[]')

    new_lines.append(new_line)


fh = open("translateG.tex","w")
for line in new_lines:
    fh.write(line)

fh.close()


