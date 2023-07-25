# ReversiAI.py
# Purpose: To play Reversi optimally
# Last Updated: 7/23/2023
# Author: Timothy Anglea

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
board_coord = [] # possible board coordinates tuples
for i in range(64):
    board_coord.append((i//8, i%8))
# End for i

# Main function for playing game
def main():
    [black_stones, white_stones] = InitializeBoard() # Place starting stones
    print("Starting Position:")
    PrintBoard(black_stones, white_stones)

    # Make move until end of game
    bp = False
    wp = False
    while True:
        # Black's turn
        print("Black (X) to move...")
        [black_stones, white_stones, bp] = Move(black_stones, white_stones)
        PrintBoard(black_stones, white_stones)

        # End conditions
        if (bp & wp):
            break # Neither player can make a move
        elif (white_stones == 0x0): # If white has no more stones
            break # Black will win
        elif (black_stones | white_stones == 0xffffffffffffffff):
            break # Black made final move
        # End if
        wp = False # Reset white pass flag

        # White's turn
        print("White (O) to move...")
        [white_stones, black_stones, wp] = Move(white_stones, black_stones)
        PrintBoard(black_stones, white_stones)

        # End conditions
        if (bp & wp):
            break # Neither player can make a move
        elif (black_stones == 0x0): # If black has no more stones
            break # White will win
        elif (black_stones | white_stones == 0xffffffffffffffff):
            break # White made final move
        # End if
    # End while
    
    # Declare winner
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
# Returns:
#   b = int; bit map of black stones on the board
#   w = int; bit map of white stones on the board
def InitializeBoard():
    # Starting position for game
    w = 0x0000001008000000
    b = 0x0000000810000000
    # basic check for board state
    if (b & w > 0):
        print("ERROR: two stones on same square")
    # End if
    return [b, w]
# End InitializeBoard

#   player = int; state of player's pieces who is next to make a move
#   opponent = int; state of opponent's pieces
def Move(player, opponent):

    [valid_dictionary, valid_positions] = FindMoves(player, opponent)
    if (len(valid_positions) == 0):
        print("No valid moves: Pass")
        return [player, opponent, True] # No valid moves for player, and they must pass
    # End if

    # Have player choose a move
    while True:
        move_choice = input("Select a Move: ").upper()
        if move_choice in valid_positions:
            break # Continue with chosen move
        else: # Not a valid move
            print("Not a valid move. Please try again.")
            message_string = "Valid positions are"
            for v in valid_positions:
                message_string += " "
                message_string += v
                message_string += ";"
            # End for v
            print(message_string)
        # End if
    # End while

    # Update Board state
    move_shift = board_positions.index(move_choice) # Get board position index (0-63) of move choice
    player |= (1 << move_shift) # add player's move to state
    for flips in valid_dictionary[move_shift]:
        # Swap opponents stones to player's stones
        player |= (1 << flips)
        opponent &= ~(1 << flips)
    # End for

    # Return updated state; a valid move was made
    return [player, opponent, False]

# End Move

def FindMoves(p, o):
    #valid_moves = [] # Set of valid moves that the player can make (NEEDED????)
    valid_move_dict = {} # Dictionary of valid moves and flipped spaces for valid moves
    #ps_index = [] # player_state_index
    os_index = [] # opponent_state_index
    for shift in range(64):
        #if ((p >> shift)%2 == 1):
        #    ps_index.append(shift)
        # End if
        if ((o >> shift)%2 == 1):
            os_index.append(shift)
        # End if
    # End for shift

    for spot in os_index: # valid moves will be next to the opponent's piece
        for offset in [-9,-8,-7,-1,1,7,8,9]:
        #for offset in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
            valid = False # flag to determine if spot_to_check is a valid square
            spot_to_check = spot + offset
            
            if (spot_to_check < 0 or spot_to_check > 63): # Is spot_to_check on the board?
                continue # spot_to_check is off the board - not a valid move
            elif (abs((spot_to_check % 8) - (spot % 8)) > 1): # Does spot_to_check wrap around the board?
                continue # spot_to_check wraps around the board - not a valid move
            elif ((1 << spot_to_check) & (p | o) > 0):
                continue # spot_to_check is already occupied by a stone - not a valid move
            else: # spot_to_check is a (potentially) valid move
                spot_opposite = spot - offset
                flip_spots = [spot] # Create list of stones to flip if spot_to_check is chosen
                while True: # potential loop 
                    if (spot_opposite < 0 or spot_opposite > 63): # Is spot_opposite on the board?
                        break # spot_opposite is off the board - spot_to_check is not a valid move
                    elif (abs((spot_opposite % 8) - ((spot_opposite + offset) % 8)) > 6): # Does spot_opposite wrap around the board?
                        break # spot_opposite wraps around the board - spot_to_check is not a valid move
                    #else: # Check for occupying stone color
                    elif ((1 << spot_opposite) & p > 0): # if spot_opposite has a player's stone
                    #elif (spot_opposite in ps_index):
                        valid = True # This is a valid move
                        break # Exit while loop and finish "for offset"
                    elif ((1 << spot_opposite) & o > 0): # if spot_opposite has an opponent's stone
                        pass # Need to check the next spot down the row (start of while loop)
                        flip_spots.append(spot_opposite) # Current spot_opposite will need to flip
                        spot_opposite = spot_opposite - offset # Update spot_opposite to adjacent spot in the row
                        continue # Repeat while loop for new spot_opposite
                    else:
                        break # No stone present - spot_to_check is not a valid move
                    # End if
                # End while
            # End if

            if (valid == True): # Add spot_to_check to list of potential moves and update flip dictionary
                # Add spot_to_check to list of valid moves
                #valid_moves.append(spot_to_check) # NEEDED?????
                if (spot_to_check in valid_move_dict.keys()):
                    for spots_to_flip in valid_move_dict[spot_to_check]:
                        flip_spots.append(spots_to_flip) # Combine previous spots to flip with new spots to flip
                    # End for x
                # End if
                valid_move_dict[spot_to_check] = flip_spots # Update dictionary with spots to flip
            # End if
        # End for
    valid_moves_list = [board_positions[x] for x in valid_move_dict.keys()]
    return [valid_move_dict, valid_moves_list]
# End FindMoves

# Returns the number of pieces for each player
# Parameters
#   b = int; bitmap for "black" stones on game board (X)
#   w = int; bitmap for "white" stones on game board (O)
# Returns
#   black_count = int; Number of bits equal to 1 in b
#   white_count = int; Number of bits equal to 1 in w
def CountStones(b, w):
    black_count = b.bit_count()
    white_count = w.bit_count()
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
            row_string += "   " # Space
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
                row_string += "--" # horizontal lines
            elif (c%2 == 0):
                row_string += " | " # vertical lines
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