# Sudoku-P3 

## Table of Contents 
- <a href="#about">About Sudoku-P3</a>
- <a href="#how_to">How to play</a>
- <a href="#features">Features</a>
  - <a href="#difficulty">Difficulty Settings</a>
  - <a href="#board">Board</a>
  - <a href="#input">Colored Input</a>
  - <a href="#rules">Rules</a>
  - <a href="#val_check">Validity Check</a>
  - <a href="#timer">Timer</a>
  - <a href="#solution">Solution</a>
  - <a href="#play_again">Play Again</a>
  - <a href="#input_val">Input Validation</a>
  - <a href="#future">Future Features</a>

<section id="about">

# About Sudoku-p3
Sudoku-P3 is a Python terminal game. It is deployed on heroku and uses a mock terminal made by Code institute. 

Users can play the classic game of Sudoku popularised by Maki Kaji.

Users can select an easy, medium or hard Sudoku puzzle to solve, get hints if they are stuck on a square, and after finishing the puzzle if their solution is wrong they can see the correct solution. 

[The deployed site is here!](https://sudoku-p3.herokuapp.com/)

<img src="assets/images/am-i-responsive.png">

</section>
<section id="how_to">

# How to play 

Sudoku-P3 is based on the classic pen and paper game Sudoku, popularised by Maki Kanji. You can learn more about Sudoku [here](https://en.wikipedia.org/wiki/Sudoku)

The rules for Sudoku are quite simple. 

- There is a 9 x 9 grid which must be filled with numbers
- The game starts with some squares already filled in
- only the numbers 1 - 9 can be used 
- Every square must contain one number 
- Each 3×3 box can only contain each number from 1 to 9 once
- Each vertical column can only contain each number from 1 to 9 once
- Each horizontal row can only contain each number from 1 to 9 once

</section>

<section id="features">

# Features 

## <p id="difficulty">Difficulty Settings</p>
- Users can select the level of difficulty, easy, medium or hard. 
- The program will make a request to an API called [suGOku](https://sugoku.herokuapp.com/) and return the numbers for the board in the form of a Python list. 
- More information about making requests to suGOku can be found [here](https://github.com/bertoort/sugoku).

<img src="assets/images/select-difficulty.png">

## <p id="board">Board</p>

- Blue borders for each 3x3 grid to make the different lines and grids stand out for the user. 
- Rows lettered A - I.
- Columns numbered 1 - 9.

<img src="assets/images/board.png">

## <p id="input">Colored Input</a>
- User input in red.
- Hint input in yellow 
- numbers generated by board are in white 

<img src="assets/images/input.png">

## <p id="rules">Rules</p>
- The rules for how to play are to the right of the board.

<img src="assets/images/rules.png">

## <p id="val_check">Validity Checker</p>
- If, by the rules of sudoku, a number conflicts with yellow or white number, it can not be inputed. 
- If a number wants to be placed in a cell containing a white or yellow number, it can not be placed. 
- Red numbers can be updated.


<img src="assets/images/val_input.png">

## <p id="timer">Timer</p>
- When user has finished filling the board a message displaying how long it took to finish the puzzle is displayed. 


<img src="assets/images/timer.png">

## <p id="solution">Solution</p>
- When user has finished filling the board they can choose to see the solution to the board. 


<img src="assets/images/solution.png">

## <p id="play_again">Play Again</p>
- When user has finished filling the board they can choose play again or quit. 



<img src="assets/images/play_again.png">


</section>