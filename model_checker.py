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


def evaluate(path,form):
	# You do not have to use evaluate as it is here;
	# you can implement modelcheck however you like.
	# This is only a hint.
	pass
	

def modelcheck(m,f):
	return evaluate(m,f)[0]


def _extract_subformulas(ast,subformulas):
	subformulas.insert(0,ast)
	for node in ast.children():
		_extract_subformulas(node,subformulas)
	return subformulas

def _formula_expansion(subformulas,states,loopIndex):
	table = []
	for formula in subformulas:
		res = _evaluate_formula(formula,states,table,loopIndex)
		if res not in table:
			table.append(res)
	return table

def _evaluate_formula(formula,states,currentTable,loopIndex):
	if formula.arity() == 0:
		res = (formula, _handle_atom(formula,states))
	elif formula.arity() == 1:
		res = (formula, _handle_unary(formula,currentTable,loopIndex))
	elif formula.arity() == 2:
		res = (formula, _handle_binary(formula,currentTable,loopIndex))
	return res

def _handle_atom(atom,states):
	atomEvaluation = []
	for state in states:
		atomEvaluation.append(atom in state.labeling)
	return atomEvaluation

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

def _handle_binary(formula,currentTable,loopIndex):
	rightChildrenTable = _find_subformula(formula.children()[0],currentTable)
	leftChildrenTable =  _find_subformula(formula.children()[1],currentTable)
	match formula.oper():
		case TokenType.AND:
			return AND_handler(rightChildrenTable,leftChildrenTable)
		case TokenType.OR:
			return OR_handler(rightChildrenTable,leftChildrenTable)
		case TokenType.IMPL:
			return IMPL_handler(rightChildrenTable,leftChildrenTable)
		case TokenType.U:
			return U_handler(rightChildrenTable,leftChildrenTable,loopIndex)
		case TokenType.R:
			return R_handler(rightChildrenTable,leftChildrenTable,loopIndex)
		case TokenType.W:
			return W_handler(rightChildrenTable,leftChildrenTable,loopIndex)

def _find_subformula(formula,currentTable):
	for subformula,truthTable in currentTable:
		if formula == subformula:
			return truthTable

ast = parse("employee_right W employee_trans")
subformulas = _extract_subformulas(ast,[])
path = getpath("paths/path0.txt")
states = path.path
loopIndex = path.total - path.loop
print(loopIndex)
table = _formula_expansion(subformulas, states, loopIndex)
print(table)
