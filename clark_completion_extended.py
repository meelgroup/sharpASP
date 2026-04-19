import os, sys
import networkx as nx

dependency_graph = nx.DiGraph()

def sortByIntegerKey(elem):
    return int(elem[0])
def writeToFile(output_file, string):
    string += "\n"
    output_file.write(string)
    return 0
def writeANDFormulaToCNF(output_file, key, definition, numberOfClauses):
    clauseToWrite = str(key) + " "
    for child in definition:
        clauseToWrite += (str(-1 * int(child)) + " ")
        clause = str(-1 * int(key)) + " " + str(child) + " 0"
        writeToFile(output_file, clause)
        numberOfClauses = numberOfClauses + 1
    clauseToWrite += "0"
    writeToFile(output_file, clauseToWrite)
    numberOfClauses = numberOfClauses + 1
    return numberOfClauses
def writeORFormulaToCNF(output_file, key, literals, numberOfClauses):
    clauseToWrite = str(-1 * int(key)) + " "
    for child in literals:
        clause = ""
        clauseToWrite += (str(child) + " ")
        clause = key + " " + str(-1 * int(child)) + " 0"
        writeToFile(output_file, clause)
        numberOfClauses = numberOfClauses + 1
    clauseToWrite += "0"
    writeToFile(output_file, clauseToWrite)
    numberOfClauses = numberOfClauses + 1
    return numberOfClauses
def writeUnitLiteralToCNF(output_file, key):
    clause = str(key) + " 0"
    writeToFile(output_file, clause)
    return 0

if len(sys.argv) == 1:
    exit("There is no input file.")
inputfile = sys.argv[1]
outputFile = "comp_copy_" + inputfile[:len(inputfile)] + ".cnf"

inputFile = open(inputfile,'r+')                  # input file for logic program
outputCNFFile = open(outputFile,'w')              # output file for cnf formula

lastVariable = 1
numberOfRule = 0
definition = dict()
ruleFinished = False
BPlus = False
BPlusAtom = list()
BMinus = False
BMinusAtom = list()
standard_variables = set()
founded_variable = set()
new_variable = 1

for line in inputFile: 
    literals = line.rstrip("\n").split(" ")
    if len(line.strip()) == 0:
        continue
    if ruleFinished == True:
        if literals[0] == '0':   # comment section finished
            ruleFinished = False
            BPlus = True
        # else:
        #     writeToFile(outputCNFFile, "c " + line.rstrip("\n"))
        continue
    if literals[0] == '6':
        print("Optimization Statement skipped.")
        continue
    elif BPlus == True:
        if literals[0] == '0':
            BMinus = True
            BPlus = False
        elif not line.startswith("B+"):
            BPlusAtom.append(int(literals[0]))
        continue
    
    elif BMinus == True:
        if literals[0] == '0':
            break
        elif not line.startswith("B-"):
            BMinusAtom.append(int(literals[0]))
        continue

    elif literals[0] == '0' and ruleFinished == False:
        ruleFinished = True    # comment section begin
        continue
    
    elif literals[0] == '1':
        numberOfRule = numberOfRule + 1
        body = list()
        atom = 4
        numberOfNegativeLiteral = int(literals[3])
        edge_sets = []
        lastVariable = max(lastVariable, int(literals[1]))
        while atom < len(literals):
            lastVariable = max(lastVariable, int(literals[atom]))
            if atom - 4 < numberOfNegativeLiteral:
                body.append(-1 * int(literals[atom]))
            else:
                body.append(int(literals[atom])) 
                edge_sets.append((int(literals[1]), int(literals[atom]))) 
            atom = atom + 1
        if len(body) > 0:
            founded_variable.add(int(literals[1]))
        if literals[1] in definition:
            lastValue = definition[literals[1]]
            if len(body) > 1:
                lastValue.append({"body": body, "atom": new_variable})
                new_variable += 1
            elif len(body) == 1:
                lastValue.append({"body": body, "atom": body[0]})
            else:
                BPlusAtom.append(literals[1])
            modifiedKey = {literals[1] : lastValue}
            definition.update(modifiedKey)
        else:
            if len(body) > 1:
                newKey = {literals[1] : [{"body": body, "atom": new_variable}]}
                new_variable += 1
                definition.update(newKey)
            elif len(body) == 1:
                newKey = {literals[1] : [{"body": body, "atom": body[0]}]}
                definition.update(newKey)
            else:
                BPlusAtom.append(literals[1])
        if len(edge_sets):
            dependency_graph.add_edges_from(edge_sets)

    elif literals[0] == '3':
        numberOfRule = numberOfRule + 1
        standard_variables.add(int(literals[2]))
        lastVariable = max(lastVariable, int(literals[2]))
    else:
        print(line)
        print("Undefined Rule Type")    

print("Number of literals in logic program: " + str(lastVariable))
print("Number of rules in logic program: "+ str(numberOfRule))

atoms_on_loop = list()

SCCs = list(nx.strongly_connected_components(dependency_graph))
return_value = False
for each_scc in SCCs:
    if len(each_scc) > 1:
        for loop_atom in each_scc:
            atoms_on_loop.append(loop_atom)

# print("Number of loop atoms: " + str(len(atoms_on_loop)))
# creating copy of each variables:
copy_of_loop_atoms = list()


definition = dict(sorted(definition.items(), key = sortByIntegerKey))

# print("The number of founded variables: {0}".format(len(founded_variable)))

# for _ in definition:
#     print(_, definition[_])

for _ in definition:
    for body in definition[_]:
        # numbering the body atoms
        if len(body['body']) > 1:
            body['atom'] = body['atom'] + lastVariable

# for _ in definition:
#     print(_, definition[_])

index = 0
        




# writeUnitLiteralToCNF(outputCNFFile, "-1")
numberOfClauses = 0

# print(standard_variables)
# print(founded_variable)
# print(BPlusAtom)
# print(BMinusAtom)

for bminusatom in BMinusAtom:
    writeUnitLiteralToCNF(outputCNFFile, str(-1 * bminusatom))
    numberOfClauses = numberOfClauses + 1

for bplusatom in BPlusAtom:
    writeUnitLiteralToCNF(outputCNFFile, str(bplusatom))
    numberOfClauses = numberOfClauses + 1

for key in definition:
    # if len(definition[key]) == 1:
    #     # need to double check this
    #     numberOfClauses = writeANDFormulaToCNF(outputCNFFile, key, definition[key][0]["body"], numberOfClauses)
    #     continue
    literalsForORRule = []
    for perChild in definition[key]:
        if len(perChild["body"]) > 1:
            numberOfClauses = writeANDFormulaToCNF(outputCNFFile, perChild["atom"], perChild["body"], numberOfClauses)
            literalsForORRule.append(perChild["atom"])
        elif len(perChild["body"]) == 1:
            literalsForORRule.append(perChild["body"][0])
    numberOfClauses = writeORFormulaToCNF(outputCNFFile, key, literalsForORRule, numberOfClauses) 


def add_one_round_copy_variables(next_variable):
    # making copy of each loop variables
    # next_variable = lastVariable + new_variable
    global numberOfClauses
    copy_variable_mapping = dict()
    for _ in atoms_on_loop:
        copy_variable_mapping[_] = next_variable
        next_variable += 1

    # print("The copy variables are: {0}".format(copy_variable_mapping))
    # relation between loop atom and copy variables
    for _ in atoms_on_loop:
        clause = "-{0} {1} 0".format(copy_variable_mapping[_], _)
        writeToFile(outputCNFFile, clause)
        numberOfClauses = numberOfClauses + 1

    for key in atoms_on_loop:
        # print("key: {0}".format(key))
        for perChild in definition['{0}'.format(key)]:
            # print(perChild)
            clauseToWrite = "{0} ".format(copy_variable_mapping[key])
            for child in perChild["body"]:
                if int(child) > 0:
                    if int(child) in atoms_on_loop:
                        clauseToWrite += "-{0} ".format(copy_variable_mapping[int(child)])
                    else:
                        clauseToWrite += "-{0} ".format(int(child))

                else:
                    if -int(child) in atoms_on_loop:
                        clauseToWrite += "{0} ".format(-copy_variable_mapping[int(child)])
                    else:
                        clauseToWrite += "{0} ".format(-int(child))
            clauseToWrite += "0"
            writeToFile(outputCNFFile, clauseToWrite)
            numberOfClauses = numberOfClauses + 1

    return copy_variable_mapping, next_variable

copy_set1, next_var = add_one_round_copy_variables(lastVariable + new_variable)

outputCNFFile.close()
# projection variables
projection_var = "c ind "
d4 = ""
for _ in standard_variables:
    projection_var += str(_) + " "
    d4 = d4 + str(_) + "," 

for _ in founded_variable:
    projection_var += str(_) + " "
    d4 = d4 + str(_) + ","
projection_var += "0"
# print("Number of variables in propositional formula: " + str(next_var - 1))
# print("Number of clauses in propositional formula: " + str(numberOfClauses))

firstLineOfCNFFile = "p cnf " + str(next_var - 1) + " " + str(numberOfClauses)

with open(outputFile, 'r+') as cnffile:
    content = cnffile.read()
    cnffile.seek(0, 0)
    cnffile.write(firstLineOfCNFFile.rstrip('\r\n') + '\n' + projection_var + '\n')
    # number of scc
    # cnffile.write("c s 1\n")
    # founded variables
    # for _ in founded_variable:
        # cnffile.write("c f {0} 0\n".format(_))
    
    # rule of the asp program
    # for _ in definition:
    #     for rule in definition[_]:
    #         # NO need to print the rule in CNF comments
    #         rule_string = "c r 0 {0}".format(_)
    #         # numbering the body atoms
    #         rule_string = rule_string + " {0} ".format(rule["atom"])
    #         l = sorted(rule["body"], reverse=True)
    #         neg = True
    #         for body_atom in l:
    #             if body_atom < 0 and neg == True:
    #                 neg = False
    #                 rule_string = rule_string + "0 "

    #             rule_string = rule_string + "{0} ".format(abs(body_atom))
    #         if neg:
    #             rule_string = rule_string + "0 "
    #         rule_string = rule_string + "0"

            # cnffile.write(rule_string + "\n")

    cnffile.write(content)
    cnffile.close()

# python3 cnf_converter.py gringo_graph_reliablity.lp
