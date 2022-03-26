def not_handler(subformula):
    truthTable = []
    for truth in subformula:
        truthTable.append(not truth)
    return truthTable

def x_handler(subformula,loopIndex):
    truthTable = subformula
    truthTable.pop(0)
    #the last element of the table is based on the first state of the loop
    truthTable.append(subformula[loopIndex])
    return truthTable

def and_handler(rightFormula, leftFormula):
    return [a and b for a, b in zip(rightFormula, leftFormula)]

def or_handler(rightFormula, leftFormula):
    return not_handler(and_handler(not_handler(rightFormula), not_handler(leftFormula)))

def impl_handler(rightFormula, leftFormula):
    return or_handler(not_handler(rightFormula), leftFormula)

def u_handler(rightFormula,leftFormula,loopIndex):
    truthTable = []
    pass

