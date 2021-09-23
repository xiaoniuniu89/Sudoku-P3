import numpy as np 
from termcolor import colored 
import requests 

# Board class that will store the sudoku board and its methods
class Board:
    def __init__(self, grid):
        self.grid = grid
        self.border = colored(("+---"*9)+"+", "blue")
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
      




def start_game():
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

#some variable
row = ["  A", "  B", "  C", "  D", "  E", "  F", "  G", "  H", "  I"]
row_index = 0
row_values = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
column_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# main game loop

game_board = (start_game())
game_board.print_board()

