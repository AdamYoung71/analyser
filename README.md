# COMP0174 Analyser

This is a program analyser for experimenting with Datalog-based analyses.

## Usage

Build an analyser image (alternatively, you can install Souffle and Python dependencies locally):

    docker build . -t comp0174-analyser
    
The image has to be rebuild each time a file in the `analyses` or `examples` directories is modified.

To run an analysis `rd_il1` (stored in `analyses/rd_il1.dl`) on a program `examples/program1.c`, please execute the following command:

    docker run -ti --rm comp0174-analyser /comp0174/analyse --analysis rd_il1 examples/program1.c
    
Alternatively, the program can be passed as an input stream (this example is for a local file `program2.c`):

    docker run -ti --rm comp0174-analyser /comp0174/analyse --analysis rd_il1 - < program2.c
    
The same analysis can be executed in three steps: (1) generating a Datalog EDB, (2) executing Souffle, and (3) printing the result (using a volume `comp0174-vol` for persistent storage):

    docker run -ti --rm comp0174-analyser -v comp0174-vol:/comp0174/results \
        /comp0174/analyse --output-edb /comp0174/results/edb1 - < program2.c
    
    docker run -ti --rm comp0174-analyser -v comp0174-vol:/comp0174/results \
        souffle --fact-dir=/comp0174/results/edb1 --output-dir=/comp0174/results/output1 analyses/rd_il1.dl

    docker run -ti --rm comp0174-analyser -v comp0174-vol:/comp0174/results \
        head /comp0174/results/output1/*

## Input Language

The input language is a subset of C. A program consists of the single function `main` without arguments in a single file. One line can contain at most one elementary block. Variable names do not repeat. We consider two variants of the input language:

* IL1: language without pointers
* IL2: language with pointers

## Datalog Relations

COMP0174 Analyser transforms a given program to a set of relations stored in `*.facts` files compatible with Souffle Datalog solver.

Relations for IL1 and IL2:

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

Relations only for IL2:

* `deref_defined(V, L)`: `assignment(L)` and a dereference of `V` is the LHS of the assignment.
* `deref_used(V, L)`: one of the following is true:
  * `assignment(L)` and a dereference of `V` is used in the RHS of the assingment;
  * `condition(L)` and a dereference of `V` is used in the condition;
  * `return(L)` and a dereference of `V` is used in the returned expression.
* `deref_rhs(V, L)`: `assignment(L)` and a dereference of `V` is the RHS of the assingment.
