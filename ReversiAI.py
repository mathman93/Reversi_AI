# ReversiAI.py
# Purpose: To play Reversi optimally
# Last Updated: 7/4/2023
# Author: Timothy Anglea

import math

def main():
    pass
# End def main

def PrintBoard():
    board_size = 8 # 8x8 board
    for r in range(2*board_size + 1): # Row counter
        row_string = ""
        for c in range(2*board_size + 1): # Column counter
            if (r%2 == 0):
                row_string += "-" # horizontal lines
            elif (c%2 == 0):
                row_string += "|" # vertical lines
            else:
                row_string += " " # pieces
            # End if
        print(row_string)
        # End for column
    # End for row

    print("") # Space after board layout
# End def PrintBoard

## Main Code
print("Starting Position:")
PrintBoard()

print("End")