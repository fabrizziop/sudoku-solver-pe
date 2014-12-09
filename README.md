sudoku-solver-pe
================

Sudoku Solver in the Project Euler format (Python 3.4)

The program uses 3 "smart" methods:

* First, it computes all possible numbers in each cell. If a cell can only contain a number then it is placed there.
* Second, if in a row or column, there is only one possible cell for a given number, it is placed there.
* Third, if in any 3x3 square, there is only one possible cell for a given number, it is placed there.

These methods are applied to all puzzles until no cell is filled with any of them in a pass. As soon as that happens, a smart bruteforce tries a number of the possible number list of a cell, then it tries to advance the puzzle again with the past methods. If the sudoku is deemed incongruent (an empty cell with no possible number is detected) then it traces back and changes the number of the last brute forced cell. 

It works and it is fast enough for me.
