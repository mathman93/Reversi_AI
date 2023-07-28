# ReversiAI.py
# Purpose: To play Reversi optimally
# Last Updated: 7/26/2023
# Author: Timothy Anglea
# List of things to update:
# 1. Simplify Move() functions by moving redundant parts to a class
# 2. Create way to choose type of play (vs. CPU; CPUvCPU; etc.)
# 3. Determine way to look ahead at state of board based on move choice

from ReversiClasses import GameBoard
import random

# Main function for playing game
def main():
    board = GameBoard() # Create game board for Reversi
    print("Starting Position:")
    board.PrintBoard()

    # Make move until end of game
    bp = False
    wp = False
    while True:
        player = 1 # Black's turn
        bp = False # Reset black pass flag
        print("Black (X) to move...")
        #[board.black, board.white, bp] = Move(board, board.black, board.white)
        [valid_dictionary, valid_positions] = board.ValidMoves(player)
        if (len(valid_positions) == 0): # No valid moves for player, and they must pass
            print("No valid moves: Pass")
            bp = True
        else: # Have person pick a move
            move_choice = Move(valid_dictionary, valid_positions)
            # Update pieces based on move_choice
            board.Update(player, move_choice, valid_dictionary)
        # End if
                
        board.PrintBoard()

        # End conditions
        if (bp & wp): # If both players recently passed
            break # Neither player can make a move
        elif (board.white == 0x0): # If white has no more stones
            break # Black will win
        elif (board.black | board.white == 0xffffffffffffffff): # If board is filled
            break # Black made final move
        # End if
        
        player = 2 # White's turn
        wp = False # Reset white pass flag
        print("White (O) to move...")
        #[board.white, board.black, wp] = RandomMove(board.white, board.black, board.board_positions)
        [valid_dictionary, valid_positions] = board.ValidMoves(player)
        if (len(valid_positions) == 0): # No valid moves for player, and they must pass
            print("No valid moves: Pass")
            wp = True
        else: # Have person pick a move
            move_choice = RandomMove(valid_dictionary, valid_positions)
            # Update pieces based on move_choice
            board.Update(player, move_choice, valid_dictionary)
        # End if
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
#   valid_dictionary = dictionary;
#   valid_positions = list;
# Returns:
#   move_choice = element from valid_positions;
def Move(valid_dictionary, valid_positions):
    move_numbers = [x for x in valid_dictionary.keys()]
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
    move_index = valid_positions.index(move_choice)
    return move_numbers[move_index]
# End Move

# Select a random move and update the state of the board (dumbAI)
# Parameters:
#   valid_dictionary = dictionary;
#   valid_positions = list;
# Returns:
#   move_choice = element from valid_positions;
def RandomMove(valid_dictionary, valid_positions):
    move_numbers = [x for x in valid_dictionary.keys()]
    # Select random move from valid_positions
    move_choice = random.choice(move_numbers)
    
    # Select move with most possible flips (choose randomly if multiple)
    # move_choices = [] # list of reduced move choices
    # max_length = 0 # Start low to increase later
    # for move in valid_dictionary.keys():
    #     current_length = len(valid_dictionary[move])
    #     if (current_length > max_length):
    #         max_length = len(valid_dictionary[move])
    #         move_choices = [] # reset move_choices
    #         move_choices.append(move) # reset move choices
    #     elif (current_length < max_length):
    #         continue # skip this move
    #     else: # move has same legnth as previous maximum
    #         move_choices.append(move) # add extra move to list
    #         # max_length remains unchanged
    #     # End if
    # # End for
    # move_choice = random.choice(move_choices)

    # Select move with least possible flips (choose randomly if multiple)
    # move_choices = [] # list of reduced move choices
    # min_length = 30 # Start high to decrease later
    # for move in valid_dictionary.keys():
    #     current_length = len(valid_dictionary[move])
    #     if (current_length < min_length):
    #         min_length = len(valid_dictionary[move])
    #         move_choices = [] # reset move_choices
    #         move_choices.append(move) # reset move choices
    #     elif (current_length > min_length):
    #         continue # skip this move
    #     else: # move has same legnth as previous maximum
    #         move_choices.append(move) # add extra move to list
    #         # max_length remains unchanged
    #     # End if
    # # End for
    # move_choice = random.choice(move_choices)

    print("Move selected: {0}".format(valid_positions[move_numbers.index(move_choice)]))
    return move_choice

# End Move

## Main Code
main()
print("End")