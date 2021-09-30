import time
from termcolor import colored
import requests
import copy


# Board class that will store the sudoku board and its methods
class Board:
    def __init__(self, grid):
        self.grid = grid  # array of 9 arrays containing the unsolved sudoku board numbers
        self.copy_grid = copy.deepcopy(self.grid)  # copy is needed for crosschecking user input with original grid
        self.border = colored(("+---" * 9) + "+", "blue")  # printed blue border for every 3x3 row top
        self.section_bottom = colored(("+" + ("-" * 11)) * 3 + "+", "blue")  # 3x3 row bottom

    def remove_zeros(self, grid):  # takes grid and replaces zero's with empty spaces
        for i in grid:
            for x, y in enumerate(i):
                if y == 0:
                    i[x] = " "

    def print_section(self, i):  # prints 3 3x3 sections - (3 rows of board)
        global row_index
        blue_post = colored("|", "blue")
        post = "|"
        print(blue_post + f" {(i[0])} "  # builds from left to right '|' and next number from the rows array
              + post + f" {(i[1])} "
              + post + f" {(i[2])} "
              + blue_post + f" {(i[3])} "
              + post + f" {(i[4])} "
              + post + f" {(i[5])} "
              + blue_post + f" {(i[6])} "
              + post + f" {(i[7])} "
              + post + f" {(i[8])} "
              + blue_post + row[row_index]
              )
        row_index += 1

    # printing the board in done by printing 3 rows at a time. This was the easiest way to get row
    # and column numbers and to have each 3x3 box to have ia nice border top and bottom
    def print_board(self):
        global row_index
        print("  1   2   3   4   5   6   7   8   9")  # column numbers reference
        print(self.border)  # border top of first 3x3 row
        for i in self.grid[0:3]:  # prints the first 3 arrays of the grid onto the board
            self.print_section(i)  # border bottom of first 3x3
        print(self.section_bottom)  # continue this way to print rest of board
        for i in self.grid[3:6]:
            self.print_section(i)
        print(self.section_bottom)
        for i in self.grid[6:9]:
            self.print_section(i)
        print(self.border)
        row_index = 0

    # To be able to input a number to a cell, the cell in the original grid must be empty
    # or the cell in the copy grid must be empty
    # if cell in the copy grid is empty, it means the space contains a number the user
    # inputted and therefore it can be updated
    def input_user_value(self, row, column, value):
        global row_values
        global column_values
        row_index_value = row_values.index(row.lower())
        column_index_value = column_values.index(int(column))
        if self.grid[row_index_value][column_index_value] == " " \
                or self.copy_grid[row_index_value][column_index_value] == " ":
            self.grid[row_index_value][column_index_value] = colored(value, "red")
        else:
            print("Square occupied")

    # when called there is no value - it will take the row and column
    # cross reference with a copy of the solved board and then input that
    # number into the game_board
    def generate_hint(self, row, column, value=None):
        global row_values
        global column_values
        row_index_value = row_values.index(row.lower())
        column_index_value = column_values.index(int(column))
        if value:
            if self.grid[row_index_value][column_index_value] == " ":
                self.grid[row_index_value][column_index_value] = value
            else:
                print("Square occupied")
        # this value will come from solved board
        else:
            value = self.grid[row_index_value][column_index_value]
            return value

    # checks if a cell is empty or not - if no empty cells board is full
    def check_solved(self, grid):
        for row in range(9):
            for column in range(9):
                if grid[row][column] == " ":
                    return False
        return True

    # goes through the board cell by cell to find the next empty cell
    def next_empty_cell(self, grid):
        for row in range(9):
            for column in range(9):
                if grid[row][column] == " ":  # found an empty cell
                    return row, column
        return None, None  # no empty cells - board is full
    #
    # #  checks if 1-9 will work in a cell
    # def possible(self, grid, number, row, column):
    #     row_values = grid[row]  # check row
    #     if number in row_values:
    #         return False
    #     col_values = [grid[row][column] for row in range(9)]  # check by column
    #     if number in col_values:
    #         return False
    #     row_start = (row // 3) * 3  # check 3x3 square
    #     col_start = (row // 3) * 3
    #
    #     for rows in range(row_start, row_start + 3):  # row of 3x3 grid
    #         for column in range(col_start, col_start + 3):  # column of 3x3 grid
    #             if grid[row][column] == number:
    #                 return False
    #     return True
    #
    # a lot of help from the following tutorials regarding recursion and backtracking:
    # 1) https://www.youtube.com/watch?v=8lhxIOAfDss
    # 2) https://www.youtube.com/watch?v=G_UYXzGuqvM
    # 3) https://www.youtube.com/watch?v=tvP_FZ-D9Ng
    def solve(self, grid):
        # step 1 is to find the next available empty cell
        row, column = self.next_empty_cell(grid)
        if row is None:  # board is full
            return True

        # step 2 is to try each number 1-9 to see if it a valid input
        for number in range(1, 10):
            if self.possible(grid, row, column, number):
                grid[row][column] = number
                # step 3 is to put the number in and try the next cell
                # if the board cannot be solved this way then go back to the last cell and make it empty
                # try again over and over until the board is solved
                if self.solve(grid):
                    return True
            grid[row][column] = " "  # didn't work so backtrack and try again
        return False

    def possible(self, grid, y, x, n):
        for i in range(0, 9):
            if self.grid[y][i] == n:
                return False
        for i in range (0, 9):
            if self.grid[i][x] == n:
                return False
        x0 = (x//3)*3
        y0 = (y//3)*3
        for i in range(0, 3):
            for j in range(0, 3):
                if self.grid[y0 + i][x0 + j] == n:
                    return False
        return True

    # def solve(self, grid):
    #     for y in range(9):
    #         for x in range(9):
    #             if self.grid[y][x] == " ":
    #                 for n in range(1, 10):
    #                     if self.possible(y, x, n):
    #                         self.grid[y][x] = n
    #                         self.solve(grid)
    #                     self.grid[y][x] = " "
    #                 self.grid = grid
    #                 return
    #
    #







# start game function called by main() function - will be called when program
# is run and if user wants to play another game when finished.
def start_game():
    print()
    print("############################################################################")
    print()
    print("Welcome to the Sudoku app!")
    print()
    print("To play, first select the level of difficulty")
    print()
    print("Easy: 1 ~ Medium: 2 ~ Hard: 3")
    print()
    # While loop for input validation - user must input 1, 2 or 3
    user_choice = input("please enter 1, 2 or 3: ")
    expected_input = ["1", "2", "3"]
    while user_choice not in expected_input:
        print("Sorry, to continue, you must enter 1 for easy, 2 for medium or 3 for hard: ")
        print()
        user_choice = input("please enter 1, 2 or 3: ")

    user_choice = int(user_choice)  # turn into an integer to be used by get_grid function
    game_board = Board(get_grid(user_choice))  # creates instance of Board class
    game_board.remove_zeros(game_board.grid)  # remove zeros and replace with empty string
    game_board.remove_zeros(game_board.copy_grid)   # same for copy of the game_board grid
    print()
    return game_board

# this function reaches out to an api called sugoku and returns an easy, medium or hard puzzle depending on user input
# information about the api and how to make requests can be found here: https://github.com/bertoort/sugoku
def get_grid(input):
    if input == 1:
        response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
        grid = response.json()["board"]
        return grid
    elif input == 2:
        response = requests.get("https://sugoku.herokuapp.com/board?difficulty=medium")
        grid = response.json()["board"]
        return grid
    if input == 3:
        response = requests.get("https://sugoku.herokuapp.com/board?difficulty=hard")
        grid = response.json()["board"]
        return grid


# global variables used throughout the program
hints = 5
# printed to the right of the board
row = ["  A     How to play Sudoku", "  B", "  C    . Every cell may contain a single number",
       "  D    . Only numbers 1-9 can be used", "  E    . Each 3x3 box can contain 1-9 once",
       "  F    . Each row can contain 1-9 once", "  G    . Each column can contain 1-9 once",
       "  H", f"  I            ~ Hints left: {hints}"]
row_index = 0  # keep track of how many rows printed during print section function in board class
row_values = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
column_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
hint_value = ["h"]
row_input = ""
column_input = 0

# the main game loop - called when program runs and if user wants to play again when a puzzle is solved
# it calls the start function which creates a grid and displays welcome message
# main function will then make a copy of the board and solve it to be used for generating hints later
# it will print the board and ask for user input to print numbers to the board in a while loop
# while loop ends when puzzle is solved
def main():
    game_board = (start_game())  # welcome message and generate grid
    game_board.print_board()  # initial print board to screen
    solved_board = Board(copy.deepcopy(game_board.grid))  # create a copy of board and solves it
    solved_board.solve(solved_board.grid)
    solved_board.print_board()

    unsolved = True
    while unsolved:
        # checking input - stores input as a row and column input to be turned into a row, column index later
        # input must be a letter (a - i) followed by a number (1-9)
        invalid_input = True
        while invalid_input:
            invalid_msg = "Sorry, to input to the board, you must enter a row letter(a-i) followed by a column " \
                          "number(1-9) - eg a5 or c7"
            try:
                # strips whitespace and - and /
                row_input, column_input = list(input("Enter a row and column to input to: ").strip().replace
                                               (" ", "").replace(",", "").replace("-", ""))

            except:
                # in case of any other invalid input will display error message
                # and remind user what to type and how to type it
                print(invalid_msg)
                print()

            else:
                if row_input.lower() in row_values and int(column_input) in column_values:
                    invalid_input = False  # means input is valid
                    print()
                else:
                    print(invalid_msg)  # any other exceptions that do not throw errors
                    print()

        invalid_input = True
        # checking input of (1-9)
        while invalid_input:
            # error message to display in case of error or unwanted input, eg pressing enter
            invalid_msg = "Sorry, to continue, you must only enter a digit between 1 - 9 or h for hint"
            try:
                input_value = input(
                    "Enter the number you wish to input to the board (0-9), or input 'h' for a hint: ").replace(" ", "")

            except:
                print(invalid_msg)
                print()

            else:
                if input_value.isalpha():  # ir if user enters "h"
                    if input_value.lower() in hint_value: # which only contains the letter "h"
                        invalid_input = False

                        # the value for the hint comes from the solved board
                        game_board.generate_hint(row_input, column_input,
                                                 solved_board.generate_hint(row_input, column_input))

                elif str(input_value).isalnum():  # written this way to check against pressing enter key
                    if int(input_value) in column_values:
                        invalid_input = False
                        row_index = row_values.index(row_input)
                        column_index = column_values.index(int(column_input))
                        # call possible() function to check if the inputted number is
                        # legal according to the rules of sudoku
                        if game_board.possible(game_board.grid, row_index, column_index, int(input_value)):
                            game_board.input_user_value(row_input, column_input, input_value)
                            print()
                        else:
                            print()
                            print("Sorry, that number doesn't work in that cell, please try again!")


                    else:
                        print(invalid_msg)
                        print()


                else:
                    print(invalid_msg)
                    print()

            finally:
                game_board.print_board()  # print updated game board
                if game_board.check_solved(game_board.grid):  # check if any empty cells left
                    unsolved = False
                    print()
                    print("Congratulations")
                    print()
                    invalid_choice = True
                    # check input - does user want to play again ?
                    while invalid_choice:
                        play_again = input("would you like to play again? y/n: ").replace(" ", "")
                        msg = "sorry, please input 'y' for yes, or 'n' for no"
                        try:
                            if play_again.lower() == "n":
                                invalid_choice = False
                                print("see you next time, thanks for playing")
                                print("program will close in 5 seconds.......")
                                time.sleep(5)   # close program

                            elif play_again.lower() == "y":
                                invalid_choice = False
                                main()  # restart game loop if user choice is 'y'

                            else:
                                print(msg)  # catch any invalid input
                                print()

                        except:  # in case of error
                            print(msg)
                            print()


main()  # initial call to run the game

# To do
# fix hints left
# when out of hints offer to print solution
# add timer to display how long it took to solve the board




