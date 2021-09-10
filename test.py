#import random
from board import Board
from minesweeper_solver import MinesweeperSolver

board = Board(10,10)
board.make_new_board()
board.assign_values_to_board()

minesweeper = MinesweeperSolver(board)
for x in range(len(minesweeper.probabilities)):
    print(minesweeper.probabilities[x])
print("=============================================")
data = minesweeper.get_state()
for x in range(len(data)):
    print(data[x])
print("=============================================")
board.dig(5,5)
data = minesweeper.get_state()
for x in range(len(data)):
    print(data[x])
print("=============================================")
minesweeper.predict_probability()
for x in range(len(minesweeper.probabilities)):
    print(minesweeper.probabilities[x])
print("=============================================")

"""data = minesweeper.get_state()
for x in range(len(data)):
    print(data[x])
print("=============================================")
minesweeper.predict_probability()
for x in range(len(minesweeper.probabilities)):
    print(minesweeper.probabilities[x])"""
#print(board)
