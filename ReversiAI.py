# ReversiAI.py
# Purpose: To play Reversi (Othello) and develop AI to choose moves optimally
# Last Updated: 8/4/2023
# Author: Timothy Anglea
# List of things to update:
# 1. Should valid_dictionary just be a class variable for Board?
# 2. Improve interface for GenerateStatistics
# 3. Determine way to look ahead at state of board based on move choice

from ReversiClasses import GameBoard
from ReversiClasses import Player
import random
import time

# Top-level function for controlling game settings
def main():
    print("Welcome to Reversi! How would you like to play?")
    print("Mode 1: Two-player game")
    print("Mode 2: Play against CPU")
    print("Mode 3: Generate CPU vs. CPU stats")
    while True:
        try:
            mode_select = int(input("Select mode (1-3): "))
            if (mode_select == 1):
                [_, _] = PlayGame("Human", "Human") # Both players are humans
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
                    [_, _] = PlayGame("Human", opponent_name)
                else: # Player 2 (CPU or human) is black and goes first
                    print("You are white (O) and will go second.")
                    [_, _] = PlayGame(opponent_name, "Human")
                # End if first
                break
            elif (mode_select == 3):
                pass # Not implemented yet
                GenerateStatistics()
                break
            else:
                print("That's not a valid game mode.")
                continue
        except KeyboardInterrupt:
            print("")
            break
        # End try
    # End while
# End main

# Primary function for playing game
def PlayGame(player1_name, player2_name, display_output = True):
    board = GameBoard() # Create game board for Reversi
    cpu = Player()
    Player1 = getattr(cpu, player1_name)
    Player2 = getattr(cpu, player2_name)

    if display_output: print("Starting Position:")
    if display_output: board.PrintBoard() 

    # Make moves until end of game
    bp = False
    wp = False
    while True:
        player = 1 # Black's turn
        bp = False # Reset black pass flag
        if display_output: print("Black (X) to move...")
        [valid_dictionary, valid_positions] = board.ValidMoves(player)
        if (len(valid_positions) == 0): # No valid moves for player, and they must pass
            if display_output: print("No valid moves: Pass")
            bp = True
        else: # Have Black pick a move
            move_choice = Player1(valid_dictionary, valid_positions, board.black, board.white)
            if display_output: print("Move selected: {0}".format(board.board_positions[move_choice]))
            # Update pieces based on move_choice
            board.Update(player, move_choice, valid_dictionary)
        # End if
        if display_output: board.PrintBoard()
        if bp & display_output: time.sleep(0.3)

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
        if display_output: print("White (O) to move...")
        [valid_dictionary, valid_positions] = board.ValidMoves(player)
        if (len(valid_positions) == 0): # No valid moves for player, and they must pass
            if display_output: print("No valid moves: Pass")
            wp = True
        else: # Have White pick a move
            move_choice = Player2(valid_dictionary, valid_positions, board.white, board.black)
            if display_output: print("Move selected: {0}".format(board.board_positions[move_choice]))
        
            # Update pieces based on move_choice
            board.Update(player, move_choice, valid_dictionary)
        # End if
        if display_output: board.PrintBoard()
        if wp & display_output: time.sleep(0.3)

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
    if display_output: board.DeclareWinner()
    return [board.black, board.white]
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

def GenerateStatistics():
    # List of methods in class Player (to allow for choice of CPU opponent)
    method_list = [attribute for attribute in dir(Player) if callable(getattr(Player, attribute)) and attribute.startswith('__') is False]
    playable_opponents = [cpu for cpu in method_list if (cpu == "Human") is False]
    #print(playable_opponents) # Include for testing
    print("Select player 1 CPU:")
    player1 = GetOpponent(playable_opponents)
    if (player1 == None): # May need to adjust this later
        return # User exitted opponent selection
    # End if
    print("Select player 2 CPU:")
    player2 = GetOpponent(playable_opponents)
    if (player2 == None): # May need to adjust this later
        return # User exitted opponent selection
    # End if

    N = 5000
    print("Playing {0} games, {1} vs. {2}...".format(N, player1, player2))
    game_score_list = [] # list of tuples of stone states between player 1 and player 2
    start = time.time()
    for game_number in range(N):
        if (game_number > 0 and game_number % (N/10) < 1):
            time_elapsed = time.time() - start
            total_expected_time = time_elapsed * (N/game_number)
            remaining_time = total_expected_time - time_elapsed
            print("{0:.1f}% complete... (~{1:.2f} seconds remaining)".format(game_number*100/N, remaining_time))
        # End if
        # [black, white] = PlayGame(player1, player2, False)
        # game_score_list.append((black,white)) # (player1 stones, player2 stones)
        # Alternate who starts first in each game
        if (game_number % 2 == 0):
            [black, white] = PlayGame(player1, player2, False)
            game_score_list.append((black,white)) # (player1 stones, player2 stones)
        else:
            [black, white] = PlayGame(player2, player1, False)
            game_score_list.append((white,black)) # (player1 stones, player2 stones)
        # End if
    # End for
    print("Time to play {0} games: {1:.2f} seconds".format(N, time.time()-start))
    print("Generating Statistics...")
    player1_wins = 0
    player2_wins = 0
    player_ties = 0
    short_games = 0
    player1_td = 0
    player2_td = 0
    for score in game_score_list:
        (p1, p2) = score
        winner = ReturnWinner(p1, p2)
        if (winner == 1):
            player1_wins += 1
        elif (winner == 2):
            player2_wins += 1
        else: # winner = 0
            player_ties += 1
        # End if winner
        if (p1 | p2 < 0xffffffffffffffff): # Game board was not filled
            short_games += 1
            # print("Incomplete Board") # Include for debugging
            # board = GameBoard(p1,p2)
            # board.PrintBoard()
        # End if
        if (p2 == 0): # Player2 lost all pieces
            player1_td += 1
            # print("Player 1 Dominates") # Include for debugging
            # board = GameBoard(p1,p2)
            # board.PrintBoard()
        elif (p1 == 0): # Player1 lost all pieces
            player2_td += 1
            # print("Player 2 Dominates") # Include for debugging
            # board = GameBoard(p1,p2)
            # board.PrintBoard()
        # End if
    # End for
    total_domination = player1_td + player2_td
    print("Player 1 Wins % - {0:.2f}%".format(player1_wins*100/N))
    print("Player 2 Wins % - {0:.2f}%".format(player2_wins*100/N))
    print("Total Ties % - {0:.2f}%".format(player_ties*100/N))
    print("% of games with incomplete board - {0:.2f}%".format(short_games*100/N))
    print("% of games with only one stone color - {0:.2f}%".format((total_domination)*100/N))
    if (total_domination > 0):
        print("Domination Ratio: P1:{0:.2f}% - P2:{1:.2f}%".format(player1_td*100/total_domination, player2_td*100/total_domination))
# End GenerateStatistics

# Returns the winner of the game based on the total number of stones for each player
def ReturnWinner(b, w):
    black_total = b.bit_count()
    white_total = w.bit_count()
    #print("Black: {0} - White: {1}".format(black_total, white_total))
    if (black_total == white_total):
        return 0 # Tie
    elif (black_total > white_total):
        return 1 # Black wins
    else:
        return 2 # White wins
    # End if
# End ReturnWinner

## Main Code
main()
print("End")