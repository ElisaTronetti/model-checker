from operator import le
from re import S, sub
from interface import parse, getpath
from operators import AND_handler, F_handler, G_handler, IMPL_handler, NOT_handler, OR_handler, R_handler, U_handler, W_handler, X_handler
from parsing.parser import Parser
from parsing.lexer import Lexer
from input_paths.path import Path 
from parsing.ast import Ast
from parsing.token import Token, TokenType

# A model checker for LTL on regular paths

""" Starting point.
	Takes in input the path of the file and the LTL formula. """
def modelcheck(m,f):
	print("File ", m, " result: ", evaluate(m,f))

""" Creates the AST from the formula and the data structure for the path file. """
def evaluate(path,form):
	ast = parse(form)
	subformulas = _extract_subformulas(ast,[]) #the subformulas are in the column of the truth table
	parsedPath = getpath(path)
	states = parsedPath.path
	loopIndex = parsedPath.total - parsedPath.loop
	table = _formula_expansion(subformulas, states, loopIndex)
	_,truth = table[len(table) - 1] #takes the last row of the formula expansions
	return check_formula_satisfaction(truth) #return if the LTL formula is satisfied

def check_formula_satisfaction(truthTable):
	if all(truthTable):
		return True
	else:
		print("The LTL formula is not satisfied in the following state indexes ",
		[i for i, n in enumerate(truthTable) if n])
		return False

""" Recursive method used to extract all the subformulas from the AST. """
def _extract_subformulas(ast,subformulas):
	subformulas.insert(0,ast) #adding always in the head of the list to keep the order correct
	for node in ast.children():
		_extract_subformulas(node,subformulas)
	return subformulas

""" Creates the truth table for each subformula found previously. """
def _formula_expansion(subformulas,states,loopIndex):
	table = []
	for formula in subformulas:
		res = _evaluate_formula(formula,states,table,loopIndex)
		if res not in table:
			#to avoid duplicates in the truth table
			table.append(res)
	return table

""" Check the arity of the formula to separate responsabilities fo the handling of it. """
def _evaluate_formula(formula,states,currentTable,loopIndex):
	if formula.arity() == 0:
		res = (formula, _handle_atom(formula,states))
	elif formula.arity() == 1:
		res = (formula, _handle_unary(formula,currentTable,loopIndex))
	elif formula.arity() == 2:
		res = (formula, _handle_binary(formula,currentTable,loopIndex))
	return res

""" In the case of an atom, it is just checked for every state if it is present or not. """
def _handle_atom(atom,states):
	atomEvaluation = []
	for state in states:
		atomEvaluation.append(atom in state.labeling)
	return atomEvaluation

""" Retrieves the subformula's truth table needed to evaluate the formula and than resolves the current operator. """
def _handle_unary(formula,currentTable,loopIndex):
	truthTable = _find_subformula(formula.child(),currentTable)
	match formula.oper():
		case TokenType.NOT:
			return NOT_handler(truthTable)
		case TokenType.X:
			return X_handler(truthTable,loopIndex)
		case TokenType.F:
			return F_handler(truthTable,loopIndex)
		case TokenType.G:
			return G_handler(truthTable,loopIndex)

""" Retrieves the two subformulas's truth tables needed to evaluate the formula and than resolves the current operator. """
def _handle_binary(formula,currentTable,loopIndex):
	leftChildrenTable = _find_subformula(formula.children()[0],currentTable)
	rightChildrenTable =  _find_subformula(formula.children()[1],currentTable)
	match formula.oper():
		case TokenType.AND:
			return AND_handler(leftChildrenTable,rightChildrenTable)
		case TokenType.OR:
			return OR_handler(leftChildrenTable,rightChildrenTable)
		case TokenType.IMPL:
			return IMPL_handler(leftChildrenTable,rightChildrenTable)
		case TokenType.U:
			return U_handler(leftChildrenTable,rightChildrenTable,loopIndex)
		case TokenType.R:
			return R_handler(leftChildrenTable,rightChildrenTable,loopIndex)
		case TokenType.W:
			return W_handler(leftChildrenTable,rightChildrenTable,loopIndex)

""" Given a formula it finds in the current truth table its values. """
def _find_subformula(formula,currentTable): 
	for subformula,truthTable in currentTable:
		if formula == subformula:
			return truthTable
