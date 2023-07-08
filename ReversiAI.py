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
    print("Starting Position:")
    PrintBoard(black_stones, white_stones)
    
    # Make move until end of game
    player_to_move = 0
    for move_number in range(20):
        [black_stones, white_stones] = MakeMove(player_to_move, black_stones, white_stones)
        PrintBoard(black_stones, white_stones)
        player_to_move = ~player_to_move # Switch turns
    # End for move_number
    
    [black_total, white_total] = CountStones(black_stones, white_stones)
    print("Black: {0} - White: {1}".format(black_total, white_total))
    if (black_total == white_total):
        print("It's a tie! Good game.")
    elif (black_total > white_total):
        print("Black wins! Good game.")
    else:
        print("White wins! Good game.")
    # End if
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
    valid_dictionary = DetermineMoves(player, b, w)
    #print(valid_positions) # for testing
    print(valid_dictionary) # for testing
    valid_positions = [board_positions[x] for x in valid_dictionary.keys()]

    # Have player choose a move
    while True:
        move_choice = input("Select a Move: ").upper()
        if move_choice in valid_positions:
            break
        else: # Not a valid move
            print("Not a valid move. Please try again.")
            print("Valid positions: {0}".format(valid_positions))
    # End while
    

    # Update Board state
    move_shift = board_positions.index(move_choice) # Get board position index (0-63) of move choice
    if (player == 0):
        b |= (1 << move_shift) # add player's move to state
        for flips in valid_dictionary[move_shift]:
            # Swap opponents stones to player's stones
            b |= (1 << flips)
            w &= ~(1 << flips)
        # End for
    else:
        w |= (1 << move_shift)
        for flips in valid_dictionary[move_shift]:
            w |= (1 << flips)
            b &= ~(1 << flips)
        # End for
    # End if

    # Return updated board state
    return [b, w]
# End MakeMove

def DetermineMoves(player, b, w):
    valid_moves = [] # Set of valid moves that the player can make
    valid_move_dict = {} # Dictionary of valid moves and flipped spaces for valid moves
    if (player == 0):
        player_state = b
        opponent_state = w
    else:
        player_state = w
        opponent_state = b
    # End if
    ps_index = [] # player_state_index
    os_index = [] # opponent_state_index
    for shift in range(64):
        if ((player_state >> shift)%2 == 1):
            ps_index.append(shift)
        # End if
        if ((opponent_state >> shift)%2 == 1):
            os_index.append(shift)
        # End if
    # End for shift
    for spot in os_index: # valid moves will be next to the opponent's piece
        for offset in [-9,-8,-7,1,9,8,7,-1]:
            valid = False # flag to determine if spot_to_check is a valid square
            spot_to_check = spot + offset
            if (spot_to_check in range(64)) and (spot_to_check not in ps_index) and (spot_to_check not in os_index):
                # Bug: Need to check that spot_opposite doesn't wrap around the board
                spot_opposite = spot - offset
                flip_spots = [spot]
                while True:
                    if (spot_opposite in range(64)) and (spot_opposite in os_index):
                        # Need to check next spot over (repeat loop)
                        flip_spots.append(spot_opposite)
                        spot_opposite -= offset
                        continue
                    elif (spot_opposite in range(64)) and (spot_opposite in ps_index):
                        # spot_to_check is valid move for current player to make
                        valid = True
                        break
                        # flip_spots will be switched when move is made
                    else: # spot_opposite is either off the board or is empty
                        break # not a valid spot to check
                    # End if
                # End while
            else:
                continue # not a valid spot to check
            # End if
            if (valid == True):
                # Add spot_to_check to list of valid moves
                valid_moves.append(spot_to_check)
                if (spot_to_check in valid_move_dict.keys()):
                    for x in valid_move_dict[spot_to_check]:
                        flip_spots.append(x)
                    #flip_spots.append([x for x in valid_move_dict[spot_to_check]])
                    # End for x
                # End if
                valid_move_dict[spot_to_check] = flip_spots
            # End if
        # End for offset
    # End for
    #valid_positions = [board_positions[x] for x in valid_move_dict.keys()]
    return valid_move_dict
# End DetermineMoves

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