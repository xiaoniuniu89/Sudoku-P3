import time
import os
import copy
from termcolor import colored
import requests


# Board class that will store the sudoku board and its methods
class Board:
    def __init__(self, grid):
        # list of 9 lists containing the unsolved sudoku board numbers
        self.grid = grid
        # copy for crosschecking user input with original grid
        self.copy_grid = copy.deepcopy(self.grid)
        # printed blue border for every 3x3 row top
        self.border = colored(("+---" * 9) + "+", "blue")
        # 3x3 row bottom
        self.section_bottom = colored(("+" + ("-" * 11)) * 3 + "+", "blue")
        # printed to the right of the board
        self.side = ["  A        How to play Sudoku",
                     "  B . Each cell contains a single number",
                     "  C . Only numbers 1-9 can be used",
                     "  D . Each 3x3 box can't have duplicates",
                     "  E . Each row can't have duplicates",
                     "  F . Each column can't have duplicates",
                     "  G . If you are stuck, ask for a hint",
                     "  H . After you get a hint, dont forget",
                     "  I . to recheck your previous inputs"]
        # keep track of how many rows printed in print_section()
        self.row_index = 0

    # takes grid and replaces zero's with empty spaces
    def remove_zeros(self, grid):
        for i in grid:
            for x, y in enumerate(i):
                if y == 0:
                    i[x] = " "

    # prints 3 3x3 sections - (3 rows of board)
    def print_section(self, i):

        blue_post = colored("|", "blue")
        post = "|"
        # builds from left to right '|' and next number from row's list
        print(blue_post + f" {(i[0])} " +
              post + f" {(i[1])} " +
              post + f" {(i[2])} " +
              blue_post + f" {(i[3])} " +
              post + f" {(i[4])} " +
              post + f" {(i[5])} " +
              blue_post + f" {(i[6])} " +
              post + f" {(i[7])} " +
              post + f" {(i[8])} " +
              blue_post + self.side[self.row_index]
              )
        self.row_index += 1

    # printing the board is done by printing top
    # border and then 3 rows at a time.
    def print_board(self):

        # column numbers reference
        print("  1   2   3   4   5   6   7   8   9")
        # border top of first 3x3 row
        print(self.border)
        # prints the first 3 arrays of the grid onto the board
        for i in self.grid[0:3]:
            # border bottom of first 3x3
            self.print_section(i)
            # continue this way to print rest of board
        print(self.section_bottom)
        for i in self.grid[3:6]:
            self.print_section(i)
        print(self.section_bottom)
        for i in self.grid[6:9]:
            self.print_section(i)
        print(self.border)
        self.row_index = 0

    # To be able to input a number to a cell, the cell in
    # the original grid must be empty or the cell
    # in the copy grid must be empty. If the cell in the
    # copy grid is empty, it means the space contains a number
    # the user inputted and therefore it can be updated
    def input_user_value(self, row, column, value):
        global row_values
        global column_values
        row_index = row_values.index(row.lower())
        column_index = column_values.index(column)
        if self.grid[row_index][column_index] == " " \
                or self.copy_grid[row_index][column_index] == " ":
            self.grid[row_index][column_index] = colored(value, "red")
        else:
            print("Square occupied")

    # when called there is no value - it will take the row and column
    # cross reference with a copy of the solved board and then input that
    # number into the game_board
    def generate_hint(self, row, column, value=None):
        global row_values
        global column_values
        row_index = row_values.index(row.lower())
        column_index = column_values.index(column)
        if value:
            if self.grid[row_index][column_index] == " " \
                    or self.copy_grid[row_index][column_index] == " ":
                self.grid[row_index][column_index] = colored(value, "yellow")
                self.copy_grid[row_index][column_index] = value
            else:
                print("Square occupied")
        # this value will come from solved board
        else:
            value = self.grid[row_index][column_index]
            return value

    # checks if a cell is empty or not - if no empty cells board is full
    def check_solved(self):
        for row in range(9):
            for column in range(9):
                if self.grid[row][column] == " ":
                    return False
        return True

    # goes through the board cell by cell to find the next empty cell
    def next_empty_cell(self, grid):
        for row in range(9):
            for column in range(9):
                if grid[row][column] == " ":  # found an empty cell
                    return row, column
        return None, None  # no empty cells - board is full

    # a lot of help from the following tutorials
    # regarding recursion and backtracking:
    # 1) https://www.youtube.com/watch?v=8lhxIOAfDss
    # 2) https://www.youtube.com/watch?v=G_UYXzGuqvM
    # 3) https://www.youtube.com/watch?v=tvP_FZ-D9Ng

    def solve(self, grid):  # recursively solve the sudoku board
        # step 1 is to find the next available empty cell
        row, column = self.next_empty_cell(grid)
        if row is None:  # board is full
            return True

        # step 2 is to try each number 1-9 to see if it a valid input
        for number in range(1, 10):
            if self.possible(row, column, number):
                grid[row][column] = number
                # step 3 is to put the number in and try the next cell
                # if the board cannot be solved this way then go back
                # to the last cell and make it empty
                # try again over and over until the board is solved
                if self.solve(grid):
                    return True
            grid[row][column] = " "  # didn't work so backtrack and try again
        return False

    # will check each cell and see if number passed is a valid [placement
    def possible(self, y, x, n):  # y axis x axis and number
        for i in range(0, 9):
            if self.grid[y][i] == n:  # checking each row
                return False
        for i in range(0, 9):
            if self.grid[i][x] == n:  # checking each column
                return False
        x0 = (x // 3) * 3  # start of 3x3 box row
        y0 = (y // 3) * 3  # start of 3x3 box column
        for i in range(0, 3):
            for j in range(0, 3):
                # start of row/column plus 3 cells makes 3x3 box
                if self.grid[y0 + i][x0 + j] == n:
                    return False
        return True
        # if all of the above tests return false then it
        # means the number is a valid choice


# start game function called by main() function - will be called when program
# is run and if user wants to play another game when finished.
def start_game():
    print()
    print("#########################################"
          "#####################################")
    print()
    print("Welcome to the Sudoku app!")
    print()
    print("To play, first select the level of difficulty")
    print()
    print("Easy: 1 ~ Medium: 2 ~ Hard: 3")
    print()
    # While loop for input validation - user must input 1, 2 or 3
    user_choice = input("please enter 1, 2 or 3:\n")
    expected_input = ["1", "2", "3"]
    while user_choice not in expected_input:
        print()
        print("Sorry, to continue, you must enter 1 for "
              "easy, 2 for medium or 3 for hard: ")
        print()
        user_choice = input("please enter 1, 2 or 3:\n")

    # turn into an integer to be used by get_grid function
    user_choice = int(user_choice)
    # creates instance of Board class
    game_board = Board(get_grid(user_choice))
    # remove zeros and replace with empty string
    game_board.remove_zeros(game_board.grid)
    # same for copy of the game_board grid
    game_board.remove_zeros(game_board.copy_grid)
    print()
    return game_board


# this function reaches out to an api called sugoku and returns
# an easy, medium or hard puzzle depending on user input
# information about the api and how to make requests
# can be found here: https://github.com/bertoort/sugoku
def get_grid(user_input):
    if user_input == 1:
        response = requests.get("https://sugoku.herokuapp.com/"
                                "board?difficulty=easy")
        grid = response.json()["board"]
        return grid
    elif user_input == 2:
        response = requests.get("https://sugoku.herokuapp.com/"
                                "board?difficulty=medium")
        grid = response.json()["board"]
        return grid
    if user_input == 3:
        response = requests.get("https://sugoku.herokuapp.com/"
                                "board?difficulty=hard")
        grid = response.json()["board"]
        return grid


def finished():
    # checks if user is finished inputing to the board
    # called when board is full
    invalid_choice = True
    while invalid_choice:
        fin = input("Board is full, are you finished?"
                    " y/n:\n").replace(" ", "")
        msg = "sorry, please input 'y' for yes, or 'n' for no"
        # input validation
        try:
            if fin.lower() == "y":
                invalid_choice = False
                return True

            elif fin.lower() == "n":
                invalid_choice = False
                print()

            else:
                print(msg)  # catch any invalid input
                print()

        except:  # in case of error
            print(msg)
            print()


# global variables used throughout the program

row_values = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
column_values = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
hint_value = ["h"]
row_input = ""
column_input = 0


# the main game loop - called when program runs and if user
# wants to play again when a puzzle is solved
# it calls the start function which creates a grid and displays welcome message
# main function will then make a copy of the board and solve
# it to be used for generating hints later
# it will print the board and ask for user input to print
# numbers to the board in a while loop
# while loop ends when puzzle is solved
def main():
    game_board = (start_game())  # welcome message and generate grid
    os.system("clear")  # clear screen
    print()
    game_board.print_board()  # initial print board to screen
    solved_board = Board(copy.deepcopy(game_board.grid))  # create copy & solve
    solved_board.solve(solved_board.grid)
    start = time.time()

    unsolved = True
    while unsolved:
        # checking input - stores input as a row and column input to
        # be turned into a row, column index later
        # input must be a letter (a - i) followed by a number (1-9)
        # first check if square is occupied by
        # yellow(hint) or white(original) number
        square_occupied = True
        while square_occupied:
            invalid_input = True
            while invalid_input:
                invalid_msg = "Sorry, to input to the board, you must enter " \
                    "a row letter(a-i) followed by a \ncolumn " \
                    "number(1-9) - eg a5 or c7"
                try:
                    # strips whitespace and "-" and "/"
                    row_input, column_input = list(input(
                        "Enter a row (a-i) followed by a column (1-9) "
                        "to input to:\n").strip().replace
                        (" ", "").replace(",", "").replace("-", ""))

                except:
                    # in case of any other invalid input will display error
                    # message and remind user what to type and how to type it
                    print(invalid_msg)
                    print()

                else:
                    if (row_input.lower() in row_values and
                            column_input in column_values):
                        row_index = row_values.index(row_input.lower())
                        column_index = column_values.index(column_input)
                        if (game_board.copy_grid[row_index]
                           [column_index] != " "):
                            print()
                            print("Square occupied")
                            print()
                        else:
                            square_occupied = False
                            invalid_input = False  # input is valid
                            print()
                    else:
                        print(invalid_msg)  # any other exceptions
                        print()

        invalid_input = True
        # checking input of (1-9)
        while invalid_input:
            # error message to display in case of error or unwanted
            # input, eg pressing enter
            invalid_msg = "Sorry, to continue, you must only enter a digit " \
                          "between 1 - 9 or h for hint"
            try:
                input_value = input(
                    "Enter the number you wish to input to the board (1-9),"
                    " or input 'h' for a hint:\n").replace(" ", "")

            except:
                print(invalid_msg)
                print()

            else:
                if input_value.isalpha():
                    # checking if user enters "h"
                    # hint value list only contains "h"
                    if input_value.lower() not in hint_value:
                        print(invalid_msg)
                        print()
                    elif input_value.lower() in hint_value:
                        invalid_input = False
                        # the value for the hint comes from the solved board
                        game_board.generate_hint(row_input.lower(),
                                                 column_input,
                                                 solved_board.generate_hint
                                                 (row_input.lower(),
                                                 column_input))
                        print()

                elif str(input_value).isalnum():  # check pressing enter key
                    if input_value in column_values:  # check num is valid
                        row_index = row_values.index(row_input.lower())
                        column_index = column_values.index(column_input)
                        if not game_board.possible(row_index, column_index,
                                                   int(input_value)):
                            print()
                            print("Sorry, that number doesn't work in that"
                                  " cell, please try again!")
                            print()
                        else:
                            invalid_input = False
                            # call possible() function to check
                            # if the inputted number is legal
                            # according to the rules of sudoku
                            if (game_board.possible
                               (row_index, column_index, int(input_value))):
                                game_board.input_user_value(
                                    row_input, column_input, input_value)
                                print()

                    else:
                        print(invalid_msg)
                        print()

                else:
                    print(invalid_msg)
                    print()

            finally:
                if not invalid_input:
                    os.system("clear")  # clear screen
                    game_board.print_board()  # print updated game board
                if game_board.check_solved():  # check for empty cells
                    if finished():  # if user is finished inputting to board
                        unsolved = False
                        print()
                        print("Congratulations")
                        print()
                        # display how long it took user
                        # to complete the board
                        minutes = divmod((time.time() - start), 60)[0]
                        seconds = round(divmod((time.time() - start), 60)[1])
                        print(f"You completed the puzzle in {int(minutes)}"
                              f" minute(s) & {seconds} second(s)! ")
                        print()
                        # check if user would like to see the solution
                        invalid_choice = True
                        while invalid_choice:
                            display = input("would you like to see the "
                                            "solution?"
                                            " y/n:\n").replace(" ", "")
                            msg = "sorry, please input 'y' for yes, " \
                                "or 'n' for no"
                            # input validation
                            try:
                                if display.lower() == "y":
                                    invalid_choice = False
                                    print()
                                    print("Here is the correct solution")
                                    print()
                                    solved_board.print_board()

                                elif display.lower() == "n":
                                    invalid_choice = False
                                    print()

                                else:
                                    print(msg)  # catch any invalid input
                                    print()

                            except:  # in case of error
                                print(msg)
                                print()

                        # check input - does user want to play again ?
                        invalid_choice = True
                        while invalid_choice:
                            play_again = input("would you like to play again?"
                                               " y/n:\n").replace(" ", "")
                            msg = "sorry, please input 'y' for yes, " \
                                "or 'n' for no"
                            # input validation
                            try:
                                if play_again.lower() == "n":  # quits game
                                    invalid_choice = False
                                    print()
                                    print("see you next time, thanks "
                                          "for playing")

                                elif play_again.lower() == "y":
                                    invalid_choice = False
                                    main()  # restart game

                                else:
                                    print(msg)  # catch any invalid input
                                    print()

                            except:  # in case of error
                                print(msg)
                                print()


main()  # initial call to run the game
