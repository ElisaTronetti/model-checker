from model_checker import modelcheck

# Used for test and LTL formula on all the paths files

#LTL formulas for the assignment
formula_1_a = "G(!(wolf_right && goat_right && !employee_right) && !(wolf_left && goat_left && !employee_left))"

formula_1_b = "G(!(popeye_right && spinach_right && !employee_right) && !(popeye_left && spinach_left && !employee_left))"

formula_1_c = """G(!(popeye_right && wine_right && computer_right && !employee_right) && 
!(popeye_left && wine_left && computer_left && !employee_left))"""

wolf_and_goat_unsupervised_right = "(wolf_right && goat_right && !employee_right)"
wolf_and_goat_unsupervised_left = "(wolf_left && goat_left && !employee_left)"
wolf_and_goat_unsupervised_right_for_four_states = "("+ wolf_and_goat_unsupervised_right +" && X("+ wolf_and_goat_unsupervised_right +" ) && X(X("+ wolf_and_goat_unsupervised_right +")) && X(X(X("+ wolf_and_goat_unsupervised_right +"))))"
wolf_and_goat_unsupervised_left_for_four_states = "("+ wolf_and_goat_unsupervised_left +" && X("+ wolf_and_goat_unsupervised_left +" ) && X(X("+ wolf_and_goat_unsupervised_left +")) && X(X(X("+ wolf_and_goat_unsupervised_left +"))))"
formula_2 = "G(!("+ wolf_and_goat_unsupervised_right_for_four_states +") && !("+ wolf_and_goat_unsupervised_left_for_four_states +"))"

employee_right_for_four_states = "(employee_right && X(employee_right) && X(X(employee_right)) && X(X(X(employee_right))))"
employee_left_for_four_states = "(employee_left && X(employee_left) && X(X(employee_left)) && X(X(X(employee_left))))"
formula_3 = "G(!("+ employee_right_for_four_states +") && !("+ employee_left_for_four_states +"))"

popeye_with_employee = "(popeye_right && employee_right && !spinach_right)"
employee_departed = "(popeye_right && !employee_right)"
formula_4 = "G(!("+ popeye_with_employee +" && X("+ popeye_with_employee +" U ("+ employee_departed +" && X("+ employee_departed +" U "+ popeye_with_employee +")))))"

formula_5 = "G(goat_trans -> X(!goat_trans U sheep_trans))"

formula_6 = "G((employee_right U employee_trans) || (employee_left U employee_trans))"

path = [
"paths/path0.txt",
"paths/path1.txt",
"paths/path2.txt",
"paths/path3.txt",
"paths/path4.txt",
"paths/path5.txt",
"paths/path6.txt",
"paths/path7.txt"
]

for p in path:
    modelcheck(p,formula_6)
    