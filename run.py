import time
from termcolor import colored
import requests
import copy


# Board class that will store the sudoku board and its methods
class Board:
    def __init__(self, grid):
        self.grid = grid
        self.border = colored(("+---" * 9) + "+", "blue")
        self.section_bottom = colored(("+" + ("-" * 11)) * 3 + "+", "blue")

    def remove_zeros(self):
        for i in self.grid:
            for x, y in enumerate(i):
                if y == 0:
                    i[x] = " "

    def print_section(self, i):
        global row_index
        blue_post = colored("|", "blue")
        post = "|"
        print(blue_post + f" {(i[0])} "
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

    def print_board(self):
        global row_index
        print("  1   2   3   4   5   6   7   8   9")
        print(self.border)
        for i in self.grid[0:3]:
            self.print_section(i)
        print(self.section_bottom)
        for i in self.grid[3:6]:
            self.print_section(i)
        print(self.section_bottom)
        for i in self.grid[6:9]:
            self.print_section(i)
        print(self.border)
        row_index = 0

    def input_user_value(self, row, column, value):
        global row_values
        global column_values
        row_index_value = row_values.index(row.lower())
        column_index_value = column_values.index(int(column))
        if self.grid[row_index_value][column_index_value] == " ":
            self.grid[row_index_value][column_index_value] = colored(value, "red")
        else:
            print("Square occupied")

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

        else:
            value = self.grid[row_index_value][column_index_value]
            return value

    def check_solved(self, grid):
        for row in range(9):
            for column in range(9):
                if grid[row][column] == " ":
                    return False
        return True

    def next_empty_cell(self, grid):
        for row in range(9):
            for column in range(9):
                if grid[row][column] == " ":
                    return row, column
        return None, None

    def possible(self, grid, number, row, column):
        row_values = grid[row]
        if number in row_values:
            return False
        col_values = [grid[row][column] for row in range(9)]
        if number in col_values:
            return False
        row_start = (row // 3) * 3
        col_start = (row // 3) * 3

        for rows in range(row_start, row_start + 3):
            for column in range(col_start, col_start + 3):
                if grid[row][column] == number:
                    return False
        return True

    def solve(self, grid):
        row, column = self.next_empty_cell(grid)
        if row is None:
            return True

        for number in range(1, 10):
            if self.possible(grid, number, row, column):
                grid[row][column] = number
                if self.solve(grid):
                    return True
            grid[row][column] = " "
        return False


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

    game_board = Board(get_grid(user_choice))
    game_board.remove_zeros()
    print()
    return game_board


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


# some variable
row = ["  A", "  B", "  C", "  D", "  E", "  F", "  G", "  H", "  I"]
row_index = 0
row_values = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
column_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
hint_value = ["h"]
row_input = ""
column_input = 0


def main():
    game_board = (start_game())
    game_board.print_board()
    copy_board = Board(copy.deepcopy(game_board.grid))
    solved_board = Board(copy.deepcopy(game_board.grid))
    solved_board.solve(solved_board.grid)

    unsolved = True
    while unsolved:
        # checking input
        invalid_input = True
        while invalid_input:
            invalid_msg = "Sorry, to input to the board, you must enter a row letter(a-i) followed by a column " \
                          "number(1-9) - eg a5 or c7"
            try:
                row_input, column_input = list(input("Enter a row and column to input to: ").strip().replace
                                               (" ", "").replace(",", "").replace("-", ""))

            except:
                print(invalid_msg)
                print()

            else:
                if row_input.lower() in row_values and int(column_input) in column_values:
                    invalid_input = False
                    print()
                else:
                    print(invalid_msg)
                    print()

        invalid_input = True
        while invalid_input:
            invalid_msg = "Sorry, to continue, you must only enter a digit between 1 - 9 or h for hint"
            try:
                input_value = input(
                    "Enter the number you wish to input to the board (0-9), or input 'h' for a hint: ").replace(" ", "")

            except:
                print(invalid_msg)
                print()

            else:
                if input_value.isalpha():
                    if input_value.lower() in hint_value:
                        invalid_input = False
                        game_board.generate_hint(row_input, column_input,
                                                 solved_board.generate_hint(row_input, column_input))

                elif str(input_value).isalnum():
                    if int(input_value) in column_values:
                        invalid_input = False
                        game_board.input_user_value(row_input, column_input, input_value)
                        print()

                    else:
                        print(invalid_msg)
                        print()

                else:
                    print(invalid_msg)
                    print()

            finally:
                game_board.print_board()
                if game_board.check_solved(game_board.grid):
                    unsolved = False
                    print()
                    print("Congratulations")
                    print()
                    invalid_choice = True
                    while invalid_choice:
                        play_again = input("would you like to play again? y/n: ").replace(" ", "")
                        msg = "sorry, please input 'y' for yes, or 'n' for no"
                        try:
                            if play_again.lower() == "n":
                                invalid_choice = False
                                print("see you next time, thanks for playing")
                                print("program will close in 5 seconds.......")
                                time.sleep(5)

                            elif play_again.lower() == "y":
                                invalid_choice = False
                                main()

                            else:
                                print(msg)
                                print()

                        except:
                            print(msg)
                            print()


main()
