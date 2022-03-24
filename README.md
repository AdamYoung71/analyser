# COMP0174 Analyser

This is a program analyser for experimenting with Datalog-based analyses.

## Installation

The easiest way to use the analyser is through Docker, but you can also install Souffle, Graphviz and Python dependencies locally.

When using Docker, please build an analyser image:

    docker build . -t comp0174-analyser

The image has to be rebuild each time a file in the `analyses` or `examples` directories is modified.

## Usage

To run an analysis `rd_il1` (defined in `analyses/rd_il1.dl`) on a program `examples/rd.il1.c`, please execute the following command:

    docker run -ti --rm comp0174-analyser python3 analyse.py --analysis rd_il1 examples/rd.il1.c
    
The same analysis can be executed in three steps: (1) generating a Datalog EDB, (2) executing Souffle, and (3) printing the result (using a volume `comp0174-vol` for persistent storage):

    docker run -ti --rm -v comp0174-vol:/comp0174/results comp0174-analyser \
        python3 analyse.py --output-edb results/edb1 examples/rd.il1.c
    
    docker run -ti --rm -v comp0174-vol:/comp0174/results comp0174-analyser \
        souffle --fact-dir=results/edb1 --output-dir=results/output1 analyses/rd_il1.dl

    docker run -ti --rm -v comp0174-vol:/comp0174/results comp0174-analyser \
        cat results/output1/result.csv

## Input Language

The input language is a subset of C with the following restrictions:

* A program is defined in a single file.
* A program consists of the single function `main` without parameters.
* Only the following statements are allowed:
  * Compound statements (blocks)
  * If conditions
  * While loops
  * Assignments
  * Function calls
  * Returns
* Function calls are only allowed as separate statements, not parts of expressions.
* Functions are not associated with any implementations and considered as black boxes.
* Pointer arithmetics is not allowed.
* Only integer types are allowed.
* Local variables do not need to be declared.

We consider two variants of the input language:

* IL1: language without pointers
* IL2: language with pointers

## Datalog Relations

Analyses are defined as Datalog programs that read input relations, and write output in the relation `result`. COMP0174 Analyser transforms a given program to a set of input relations stored in `*.facts` files compatible with Souffle Datalog solver.

Input relations for IL1 and IL2:

* `label(L)`: `L` is a label of an elementary block. Labels are named as `l1`, `l23`, etc where 1 and 23 are the lines numbers.
* `flow(L1,L2)`: there is an arc between `L1` and `L2` in the control flow graph.
* `init(L)`: `L` is the initial label.
* `final(L)`: `L` is the final label.
* `variable(V)`: `V` is a variable.
* `assignment(L)`: `L` is a label of an assignment statement.
* `condition(L)`: `L` is a label of an if or loop condition.
* `return(L)`: `L` is a label of a return statement.
* `function(M)`: `M` is a function.
* `call(M, L)`: the function `M` is called at the statement `L`.
* `used(V, L)`: one of the following is true:
  * `assignment(L)` and the variable `V` is used in the RHS of the assingment;
  * `condition(L)` and the variable `V` is used in the condition;
  * `call(M, L)` and the variable `V` is used in the arguments of the call;
  * `return(L)` and the variable `V` is used in the returned expression.
* `defined(V, L)`: `assignment(L)` and `V` is the LHS of the assignment.

Input relations only for IL2:

* `deref_defined(V, L)`: `assignment(L)` and a dereference of `V` is the LHS of the assignment.
* `deref_used(V, L)`: one of the following is true:
  * `assignment(L)` and a dereference of `V` is used in the RHS of the assingment;
  * `condition(L)` and a dereference of `V` is used in the condition;
  * `call(M, L)` and a dereference of `V` is used in the arguments of the call;
  * `return(L)` and a dereference of `V` is used in the returned expression.
* `deref_rhs(V, L)`: `assignment(L)` and a dereference of `V` is the RHS of the assingment.
