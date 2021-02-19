Sudoku Instructions:

Simply you must fill each spot on the board with a number 1-9, without repeating any numbers in every row, column, and 
3x3 block (inside thicker lines on board). For more about the rules visit https://www.learn-sudoku.com/sudoku-rules.html. 


To run sudoku.py on repl.it:

1. Open the repl.it link (https://repl.it/@powdrild/Sudoku#main.py)

2. Click run at the top.

3. You will be shown a sudoku board on the screen. 

4. Press Enter to solve/verify the Sudoku board. If solving, all solved numbers will be in green. The program will then tell you whether
the board is solved/verified or incorrect/unsolvable.

5. Press the Spacebar to get a new random Sudoku board (requires internet).

6. If you want to put in your own Sudoku board to solve/verify, edit the variable grid on line 305 on repli.it (line 306 in python code file) with a board in the same style as shown 
in the code (a list of lists).

Example for verifying:
grid = [[6,4,2,1,3,8,5,7,9],
         [1,3,5,2,7,9,4,6,8],
         [7,8,9,4,5,6,1,2,3],
         [2,1,3,5,4,7,8,9,6],
         [4,5,6,8,9,2,3,1,7],
         [8,9,7,3,6,1,2,4,5],
         [3,6,1,7,2,5,9,8,4],
         [5,7,8,9,1,4,6,3,2],
         [9,2,4,6,8,3,7,5,1]]

Example for solving:
grid = [[0,0,0,1,0,0,5,0,0],
         [0,0,5,0,7,0,0,6,0],
         [0,0,0,4,0,0,0,0,0],
         [2,0,3,0,0,7,8,0,0],
         [4,5,0,8,9,2,3,1,0],
         [0,0,7,0,6,0,0,4,5],
         [0,6,1,7,2,0,9,0,0],
         [5,0,8,9,1,4,6,0,0],
         [9,0,4,0,0,3,0,5,1]]
