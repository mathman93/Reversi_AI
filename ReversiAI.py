# ReversiAI.py
# Purpose: To play Reversi optimally
# Last Updated: 7/23/2023
# Author: Timothy Anglea

from ReversiClasses import GameBoard

# Main function for playing game
def main():
    board = GameBoard() # Create game board for Reversi
    print("Starting Position:")
    board.PrintBoard()

    # Make move until end of game
    bp = False
    wp = False
    while True:
        # Black's turn
        print("Black (X) to move...")
        [board.black, board.white, bp] = Move(board.black, board.white, board.board_positions)
        board.PrintBoard()

        # End conditions
        if (bp & wp): # If both players recently passed
            break # Neither player can make a move
        elif (board.white == 0x0): # If white has no more stones
            break # Black will win
        elif (board.black | board.white == 0xffffffffffffffff): # If board is filled
            break # Black made final move
        # End if
        wp = False # Reset white pass flag

        # White's turn
        print("White (O) to move...")
        [board.white, board.black, wp] = Move(board.white, board.black, board.board_positions)
        board.PrintBoard()

        # End conditions
        if (bp & wp): # If both players recently passed
            break # Neither player can make a move
        elif (board.black == 0x0): # If black has no more stones
            break # White will win
        elif (board.black | board.white == 0xffffffffffffffff): # If board is filled
            break # White made final move
        # End if
    # End while
    
    # Declare winner
    board.DeclareWinner()
# End main

# Have player choose a move and update the state of the board
# Parameters:
#   player = int; current state of stones of player who is next to make a move
#   opponent = int; current state of opponent's stones
#   board_positions = list; all names of spaces on board
# Returns:
#   player = int; updated state of player's stones
#   opponent = int; updated state of opponent's stones
#   boolean; whether the player had to pass due to no possible valid moves (True = pass)
def Move(player, opponent, board_positions):

    [valid_dictionary, valid_positions] = FindMoves(player, opponent, board_positions)
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

def FindMoves(p, o, board_positions):
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

## Main Code
main()
print("End")