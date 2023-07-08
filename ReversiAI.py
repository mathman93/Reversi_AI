# ReversiAI.py
# Purpose: To play Reversi optimally
# Last Updated: 7/4/2023
# Author: Timothy Anglea

# import math

# Global Variables
board_size = 8 # 8x8 board
board_positions = [] # possible board selections
row_names = ["A", "B", "C", "D", "E", "F", "G", "H"]
column_names = ["1", "2", "3", "4", "5", "6", "7", "8"]
for row in row_names:
    for column in column_names:
        board_positions.append(row+column)
    # End for column
# End for row

def main():
    [black_stones, white_stones] = InitializeBoard()
    #[black_total, white_total] = CountStones(black_stones, white_stones)
    #print("{0} - {1}".format(black_total, white_total))
    print("Starting Position:")
    PrintBoard(black_stones, white_stones)
    
    # Make move until end of game
    player_to_move = 0
    for move_number in range(2):
        [black_stones, white_stones] = MakeMove(player_to_move, black_stones, white_stones)
        PrintBoard(black_stones, white_stones)
        player_to_move = ~player_to_move # Switch turns
    # End for move_number
    
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
# End InitializeBoard

def MakeMove(player, b, w):
    # "player" = 0 for black, 1 for white
    if (player == 0):
        print("Black (X) to move...")
    else: # player == 1
        print("White (O) to move...")
    # End if
    # Determine possible moves
    pass
    # Have player choose a move
    while True:
        move_choice = input("Select a Move: ").upper()
        if move_choice in board_positions:
            break
        else: # Not a valid move
            print("Not a valid move. Please try again.")
    # End while
    move_shift = board_positions.index(move_choice) # Get board position index (0-63) of move choice
    if (player == 0):
        b |= (1 << move_shift) # Add black stone to state
        w &= ~(1 << move_shift) # Remove white stone from state (Not necessary if pre-checking valid moves)
        # (will be necessary for switching stone colors on capture)
    else: # player == 1
        w |= (1 << move_shift)
        b &= ~(1 << move_shift)
    # End if
    return [b, w]
# End MakeMove

def CountStones(b, w):
    black_count = 0 # Total number of black stones
    white_count = 0 # Total number of white stones
    for shift in range(64):
        if ((b >> shift) % 2 == 1):
            black_count += 1
        # End if
        if ((w >> shift) % 2 == 1):
            white_count += 1
        # End if
    # End for shift
    return [black_count, white_count]
# End CountStones

# Displays current state of game board
# Parameters
#   b = int; bitmap for "black" stones on game board (X)
#   w = int; bitmap for "white" stones on game board (O)
def PrintBoard(b, w):
    # Column Header
    row_string = " "
    for c in range(2*board_size + 1):
        if (c%2 == 1):
            row_string += column_names[c >> 1]
        else:
            row_string += " " # Space
        # End if
    # End for c
    print(row_string)
    # Board layout
    square = 0
    for r in range(2*board_size + 1): # Row counter
        row_string = ""
        if (r%2 == 1):
            row_string += row_names[r >> 1]
        else:
            row_string += " " # Space
        # End if
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
# End PrintBoard

## Main Code
main()
print("End")