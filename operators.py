# Minimum set of operators

def NOT_handler(subformula):
    truthTable = []
    for truth in subformula:
        truthTable.append(not truth)
    return truthTable

def X_handler(subformula,loopIndex):
    truthTable = subformula.copy()
    truthTable.pop(0)
    #the last element of the table is based on the first state of the loop
    truthTable.append(subformula[loopIndex])
    return truthTable

def AND_handler(leftFormula,rightFormula):
    return [a and b for a, b in zip(leftFormula, rightFormula)]

def U_handler(leftFormula,rightFormula,loopIndex):
    truthTable = []
    toCompile = 0
    currentIndex = 0
    for left, right in zip(leftFormula, rightFormula):
        if right or ((left is False) and (right is False)):
            truthTable.insert(currentIndex, right)
            while toCompile > 0:
                truthTable[currentIndex - toCompile] = truthTable[currentIndex]
                toCompile -= 1
        else:
            truthTable.insert(currentIndex, False)
            toCompile += 1
        currentIndex += 1
    while toCompile > 0:
        truthTable[currentIndex - toCompile] = truthTable[loopIndex]
        toCompile -= 1
    return truthTable

# Derived operators

def OR_handler(leftFormula, rightFormula):
    return NOT_handler(AND_handler(NOT_handler(leftFormula), NOT_handler(rightFormula)))

def IMPL_handler(leftFormula, rightFormula):
    return OR_handler(NOT_handler(leftFormula), rightFormula)

def W_handler(leftFormula,rightFormula,loopIndex):
    return R_handler(rightFormula, OR_handler(leftFormula,rightFormula),loopIndex)

def R_handler(leftFormula,rightFormula,loopIndex):
    return NOT_handler(U_handler(NOT_handler(leftFormula),NOT_handler(rightFormula),loopIndex))

def F_handler(subformula,loopIndex):
    trueFormula = [True] * (len(subformula))
    return U_handler(trueFormula,subformula,loopIndex)

def G_handler(subformula,loopIndex):
    falseFormula = [False] * (len(subformula))
    return R_handler(falseFormula,subformula,loopIndex)
