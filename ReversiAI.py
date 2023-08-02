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

# Main function for playing game
def main(cpu_opponent_name):
    board = GameBoard() # Create game board for Reversi
    cpu = Player()
    cpu_opponent = getattr(cpu, cpu_opponent_name)

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
            move_choice = cpu.Move(valid_dictionary, valid_positions)
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
            move_choice = cpu_opponent(valid_dictionary, valid_positions)
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

## Main Code
# List of methods in class Player (to allow for choice of CPU opponent)
method_list = [attribute for attribute in dir(Player) if callable(getattr(Player, attribute)) and attribute.startswith('__') is False]
playable_opponents = [cpu for cpu in method_list if (cpu == "Move") is False]
print(playable_opponents)

main("Minnie")
print("End")