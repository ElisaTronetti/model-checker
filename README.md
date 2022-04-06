# LTL model checker
This is a simple LTL model checker developed for an assignment for the course __Logic in Computer Science__ (T-505-ROKF) taken in Reykjavìk University.

# Assignmnet premises
This is not a general LTL model checker, but it is design to work with regular path, which makes it simpler.  

In fact, the schedule to work with is a regular path: it has the form of a __lasso__, meaning that it has an initial part _I_, and a loop _L_ whtat is repeated for ever after that. So it results in _I L L L ..._ .  
Each schedule for the assignment is given as a text file. The first line of the file has two integers: the first integer is the total length of the schedule (|_I_| + |_L_|), and the second one is the lenght of the loop (_L_). Each line after that gives the labeling of the states of the schedule in order.  

Parts of the implementation are provided. It has to be implement the model checker itself, which involves the development of the __model\_checker.py__ and __operators.py__. For tests porpuses it has been implemented also __test.py__.

# LTL model checker design
The core part of the model checker is in the __model\_checker.py__ file.  
Since the scheduler has the form of a lasso, it is not necessary to implement a general LTL model checker. They are going to be used formulas expansion to compile a truth table which is going to be used to find the final result.  
In order to explain it better, the whole design will be divided in steps, that are just the order in which the different function implemented are invoked:
- The first step consist on the creation of the __Abstract Syntax Tree__, which makes possible to have a the actual structure of the LTL formula given in input;
- Next, from the abstract syntax tree it is possible to extract the sub-formulas. In fact, in order to be able to evaluate the formulas, it is necessary to evaluate the abstract syntax tree from the leaves until the root of the tree.  
The sub-formulas are extracted by a recursive method called __\_extract\_subformulas__, which adds the root formula at the head of the list, then it extract the children of that formula (which can be one or two) and call the itself recursively. In this way, the atoms will be at the beginning of the list and the root at the end, providing a list of formulas ready to be evaluated;
- Once the sub-formulas are ready, it is necessary to parse the states from the file provided and to save the loop index that is going to be useful when the operators in the formulas are evaluated.  
- Now that all the elements are ready, it is possible to call the __\_formula\_expansion__ method, which is going to create the truth table. Starting from the list of sub-formulas, each of them is evaluated and added to the truth table if not already present.  
In order to evaluate a formula it is used the method __\_evaluate\_formula__, which need the current formula to evaluate, the states, the current truth table and the index of the loop.  
The __\_evaluate\_formula__ changes its behavior basing on the arity of the formula:
    - __Arity 0:__ if the arity is 0, then a leaf has been found. The method __\_handle\_atom__ is called, in which, for every state the atom is evaluated. It results true if the atom's label is present in the current state, it is false otherwise;  
    - __Arity 1__: it is the case of an unary operator. Given the current formula, it is searched in the current truth table the row of its sub-formula, in order to base the result of the current formula on its already evaluated sub-formula. The possible unary operators are $ \lnot $, X, F and G, and each of them has its handler; 
    - __Arity 2__: finally there is the case of binary operators. In this case it is necessary to find from the current formula, its left sub-formula and its right sub-formula rows from the truth table. Then the handler of the correct formula operator is called. The possible binary operators are $ \wedge $, $ \vee $, $ \rightarrow $, U, R and W.  
- Once the truth table is completed, it is possible to tell if a model satisfies the provided formula. In order to do that, it is used the __check\_formula\_satisfaction__ method. This will take the last row of the truth table, which contains the complete formula. Then, the first element of that row is checked: this is done because if there is not a G operator specified, then only the first path checks if it satisfy the formula. If that is true, then the formula is satisfied. If it is not, then the states in which the formula is not satisfied are printed. To have them match with the row number in the file, a 2 is added to the index.

## Minimum set of operators
Since it is possible to express some operators by using other operators, it was important to take a decision about which operators to implement.  
They are going to be discusses first the implemented operators, and then there are going to be details about the equivalence formulas used to derive the other operators.  
The operators can be found in the code in the __operators.py__ file.

\noindent The minimum set of operators chosen is the following: {$ \wedge $, $ \lnot $, X, U }:  
- $ \phi \wedge \psi $ :  
it is a binary operator, so it is necessary to have the truth table of its left sub-formula ($ \phi $) and its right sub-formula ($ \psi $). Then, it is a simple "and" operation between the two truth tables for each state.
- $ \lnot \phi $ :  
 it is a unary operator, so in order to implement it, it is enough to use the truth table of its sub-formula ($ \phi $) and to negate it.
- X $ \phi $ :  
 next is a unary temporal operator. It needs only the truth table of its sub-formula ($ \phi $) and one state assumes the value of the next states. Since the schedule is a lasso, to evaluate the last state, it is needed the loop index, in order to be able to check the actual next state of the last state.  
- $ \phi $ U $ \psi $:  
 until is a binary temporal operator. So, it requires the left ($ \phi $) and the right ($ \psi $) sub-formulas. It also require the loop index to specify which state comes after the last state.  
 For each pair of the two sub-formulas tables, if $ \psi $ is true, then true is insert in that state, if $ \phi $ and $ \psi $ are both false, then false is added. These are considered the base cases. If $ \phi $ is true and $ \psi $ is false, then that state can not be resolved until one of the base cases are encountered. Even though it is not resolved, a false is added in the table: this is made to avoid an empty truth table if any of the pair matches with the base cases. Once a non base case is encountered it is incremented a counter, which keeps track of how many states must be resolved once a base case is found. So, when a base case is found, the counter is checked, and if there are states to resolve, they are changed with the value of the base case (so if the base case is true, all the unresolved occurrences are true, and if it is false, then all the unresolved occurrences are false).  
 Once all the pairs are checked, there might still be unresolved states, which can be resolved by check the loop index value.

The other operators are implemented by using the following equivalence formulas:
- $ \phi \vee \psi $ $\equiv \lnot (\lnot \phi \wedge \lnot \psi) $  
- $ \phi \rightarrow \psi $ $\equiv  \lnot \phi \vee \psi $
- $ \phi $ R $ \psi $ $\equiv \lnot (\lnot \phi U \lnot \psi) $
- $ \phi $ W  $ \psi $ $\equiv \psi R (\phi \vee \psi)$
- F $ \phi $ $\equiv \top U \phi $
- G $ \phi $ $\equiv \bot R \phi $

# Technical setup
The technical setup chosen is very simple and it consists of:
- Python version >= __3.10.3__

# How to run
To run the project it is possible to use the predisposed file __test.py__. In the file there are the formulas created for the assignement already written, but it is possible to write new LTL formulas.  
The formulas are going to be tested on all the provided pathX.txt files provided, but new files can be created.  
Once the formulas and the model are decided, it is possible to change the arguments in the __modelcheck__ methos, with accept a path and an LTL formula.  

To run the following command has to be run:
```
python test.py
```

The output of the program consists of:
- for every file it is specified if the LTL formula holds or not;
- if the formula does not hold, then the state where it does not hold are specified. The number of the state specified correspond to the row of that state in the file, in order to avoid confusion.