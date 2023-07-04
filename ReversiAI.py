# ReversiAI.py
# Purpose: To play Reversi optimally
# Last Updated: 7/4/2023
# Author: Timothy Anglea

import math

board_size = 8 # 8x8 board

def main():
    [black_stones, white_stones] = InitializeBoard()
    print("Starting Position:")
    PrintBoard(black_stones, white_stones)
# End main

# Sets initial configuration for the game board
def InitializeBoard():
    # Starting position for game
    b = 0x0000001008000000
    w = 0x0000000810000000
    # basic check for board state
    if (b & w > 0):
        print("ERROR: two stones on same square")
    # End if
    return [b, w]
# End def InitializeBoard

# Displays current state of game board
# Parameters
#   b = int; bitmap for "black" stones on game board (X)
#   w = int; bitmap for "white" stones on game board (O)
def PrintBoard(b, w):
    square = 0
    for r in range(2*board_size + 1): # Row counter
        row_string = ""
        for c in range(2*board_size + 1): # Column counter
            if (r%2 == 0):
                row_string += "-" # horizontal lines
            elif (c%2 == 0):
                row_string += "|" # vertical lines
            else: # game pieces
                if ((b >> square) % 2== 1):
                    row_string += "X" # black stone
                elif ((w >> square) % 2 == 1):
                    row_string += "O" # white stone
                else:
                    row_string += " " # no stones
                # End if
                square += 1
            # End if
        # End for column
        print(row_string)
    # End for row

    print("") # Space after board layout
# End def PrintBoard

## Main Code
main()
print("End")