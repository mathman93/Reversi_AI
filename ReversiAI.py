# ReversiAI.py
# Purpose: To play Reversi (Othello) and develop AI to choose moves optimally
# Last Updated: 7/31/2023
# Author: Timothy Anglea
# List of things to update:
# 1. Should valid_dictionary just be a class variable for Board?
# 2. Create way to choose type of play (vs. CPU; CPUvCPU; etc.)
# 3. Determine way to look ahead at state of board based on move choice

from ReversiClasses import GameBoard
from ReversiClasses import Player
import random

# Main function for playing game
def PlayGame(player1_name, player2_name):
    board = GameBoard() # Create game board for Reversi
    cpu = Player()
    Player1 = getattr(cpu, player1_name)
    Player2 = getattr(cpu, player2_name)

    print("Starting Position:")
    board.PrintBoard()

    # Make moves until end of game
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
            move_choice = Player1(valid_dictionary, valid_positions, board.black, board.white)
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
            move_choice = Player2(valid_dictionary, valid_positions, board.black, board.white)
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
# End PlayGame

def GetOpponent(opponent_list):
    list_length = len(opponent_list)
    while True:
        try:
            print("Select an opponent from the following list:")
            count = 0
            for name in opponent_list:
                count += 1
                print("{0}: {1}".format(count, name))
            # End for name
            cpu_select = int(input("Which opponent? (1-{0}): ".format(list_length)))
            if (cpu_select < 1 or cpu_select > list_length):
                print("Selection is not in range. Try again.")
                continue
            else:
                print("You have selected {0} as your opponent.".format(opponent_list[cpu_select-1]))
                break
            # End if
        except ValueError:
            print("Not a valid selection. Try again.")
            continue
        except KeyboardInterrupt:
            print("")
            return None # Error code
    return opponent_list[cpu_select-1]
# End GetOpponent

## Main Code
print("Welcome to Reversi! How would you like to play?")
print("Mode 1: Two-player game")
print("Mode 2: Play against CPU")
print("Mode 3: Generate CPU vs. CPU stats")
while True:
    try:
        mode_select = int(input("Select mode (1-3): "))
        if (mode_select == 1):
            PlayGame("Human", "Human") # Both players are humans
            break
        elif (mode_select == 2):
            # List of methods in class Player (to allow for choice of CPU opponent)
            method_list = [attribute for attribute in dir(Player) if callable(getattr(Player, attribute)) and attribute.startswith('__') is False]
            playable_opponents = [cpu for cpu in method_list if (cpu == "Human") is False]
            #print(playable_opponents) # Include for testing

            opponent_name = GetOpponent(playable_opponents)
            if (opponent_name == None):
                break # User exitted opponent selection
            # End if
            first = random.randint(1,2)
            if (first == 1): # Player 1 (human) is black and goes first
                print("You are black (X) and will go first.")
                PlayGame("Human", opponent_name)
            else: # Player 2 (CPU or human) is black and goes first
                print("You are white (O) and will go second.")
                PlayGame(opponent_name, "Human")
            # End if first
            break
        elif (mode_select == 3):
            pass # Not implemented yet
            break
        else:
            print("That's not a valid game mode.")
            continue
    except KeyboardInterrupt:
        print("")
        break
    # End try
# End while

print("End")