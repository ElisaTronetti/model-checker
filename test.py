from model_checker import modelcheck

# Used for test and LTL formula on all the paths files

form = "(employee_right || employee_left) U employee_trans"

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
    modelcheck(p,form)