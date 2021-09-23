import numpy as np 
from termcolor import colored 
import requests 

# Board class that will store the sudoku board and its methods
class Board:
    def __init__(self, grid):
        self.grid = grid

    



def welcome_message():
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
  print(f'you chose the number {user_choice}')
  


welcome_message()