# ReversiClasses.py
# Purpose: File for holding python classes related to ReversiAI.py
# Author: Timothy Anglea
# Last Modified: 7/31/23

import random

class GameBoard:
    # Create game board variables and state
    def __init__(self, b = None, w = None):
        self.__board_size = 8 # Size of board (size x size)
        self.board_positions = [] # possible board selections
        self.__row_names = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.__column_names = ["1", "2", "3", "4", "5", "6", "7", "8"]
        for row in self.__row_names:
            for column in self.__column_names:
                self.board_positions.append(row+column)
            # End for column
        # End for row
        self.black = 0x0
        self.white = 0x0
        # Initialize state of board
        self.InitializeBoard(b, w)

    # End __init__

    # Sets initial configuration for the game board
    # Parameters:
    #   b = int; bit map of black stones on the board
    #   w = int; bit map of white stones on the board
    def InitializeBoard(self, b = None, w = None):
        if (b == None or w == None):
            # Starting position for game
            self.black = 0x0000000810000000
            self.white = 0x0000001008000000
        else:
            self.black = b
            self.white = w
        # End if

        # basic check for board state (NEEDED HERE?)
        if (self.black & self.white > 0):
            print("ERROR: two stones on same square")
        # End if
    # End InitializeBoard

    # Finds valid moves for player given state of board
    # Parameters:
    #   player = int; player who is making the next (valid) move
    # Returns:
    #   valid_move_dict = dictionary; dictionary of stones that would be flipped for a given valid move
    #   valid_moves_list = list; list of valid moves in the form of board position labels
    def ValidMoves(self, player):
        if (player == 1): # Black's turn to make a move
            p = self.black
            o = self.white
        elif (player == 2): # White's turn to make a move
            p = self.white
            o = self.black
        else:
            return None # A bad error has occured (should make this better)
        # End if

        valid_move_dict = {} # Dictionary of valid moves and flipped spaces for valid moves
        for spot in [shift for shift in range(64) if (o >> shift)%2 == 1]: # valid moves will be next to the opponent's piece
            for offset in [-9,-8,-7,-1,1,7,8,9]:
                valid = False # Flag to determine if spot_to_check is a valid square
                spot_to_check = spot + offset # board number of potential move
                
                if (spot_to_check < 0 or spot_to_check > 63): # Is spot_to_check not on the board?
                    continue # spot_to_check is off the board - not a valid move
                elif (abs((spot_to_check % 8) - (spot % 8)) > 1): # Does spot_to_check wrap around the board?
                    continue # spot_to_check wraps around the board - not a valid move
                elif ((1 << spot_to_check) & (p | o) > 0): # Is spot_to_check already occupied?
                    continue # spot_to_check is already occupied by a stone - not a valid move
                else: # spot_to_check is a (potentially) valid move
                    spot_opposite = spot - offset # board number opposite of spot_to_check
                    flip_spots = [spot] # Create list of stones to flip if spot_to_check is chosen
                    while True: # potential loop 
                        if (spot_opposite < 0 or spot_opposite > 63): # Is spot_opposite on the board?
                            break # spot_opposite is off the board - spot_to_check is not a valid move
                        elif (abs((spot_opposite % 8) - ((spot_opposite + offset) % 8)) > 6): # Does spot_opposite wrap around the board?
                            break # spot_opposite wraps around the board - spot_to_check is not a valid move
                        # Now, check for occupying stone color
                        elif (((1 << spot_opposite) & p) > 0): # if spot_opposite has a player's stone
                            valid = True # This is a valid move
                            break # Exit while loop and finish "for offset"
                        elif (((1 << spot_opposite) & o) > 0): # if spot_opposite has an opponent's stone
                            pass # Need to check the next spot down the row (start of while loop)
                            flip_spots.append(spot_opposite) # Current spot_opposite will need to flip
                            spot_opposite = spot_opposite - offset # Update spot_opposite to adjacent spot in the row
                            continue # Repeat while loop for new spot_opposite
                        else: # spot_opposite is vacant
                            break # No stone present - spot_to_check is not a valid move
                        # End if
                    # End while
                # End if

                if (valid == True): # Add spot_to_check to list of potential moves and update flip dictionary
                    # Add spot_to_check to list of valid moves
                    if (spot_to_check in valid_move_dict.keys()):
                        for spots_to_flip in valid_move_dict[spot_to_check]:
                            flip_spots.append(spots_to_flip) # Combine previous spots to flip with new spots to flip
                        # End for
                    # End if
                    valid_move_dict[spot_to_check] = flip_spots # Update dictionary with spots to flip
                # Else, spot_to_check was not a valid move; return to top of for loop and try next candidate
                # End if
            # End for
        # End for
        # Construct list of valid moves based on the board position names
        valid_moves_list = [self.board_positions[x] for x in valid_move_dict.keys()]
        return [valid_move_dict, valid_moves_list]
    # End FindMoves

    # Update state of board based on chosen move by player (p)
    def Update(self, player, move_choice, valid_dictionary):
        if (player == 1): # Black just made a move
            self.black |= (1 << move_choice)
            for flips in valid_dictionary[move_choice]:
                # Swap opponents stones to player's stones
                self.black |= (1 << flips)
                self.white &= ~(1 << flips)
            # End for
        elif (player == 2): # White just made a move
            self.white |= (1 << move_choice)
            for flips in valid_dictionary[move_choice]:
                # Swap opponents stones to player's stones
                self.white |= (1 << flips)
                self.black &= ~(1 << flips)
            # End for
        else:
            return None # A bad error has occured (should make this better)
        # End if
    # End Update

    # Displays current state of game board
    def PrintBoard(self):
        # Column Header
        row_string = " "
        for c in range(2*self.__board_size + 1):
            if (c%2 == 1):
                row_string += self.__column_names[c >> 1]
            else:
                row_string += "   " # Space
            # End if
        # End for c
        print(row_string)
        # Board layout
        square = 0
        for r in range(2*self.__board_size + 1): # Row counter
            row_string = ""
            if (r%2 == 1):
                row_string += self.__row_names[r >> 1]
            else:
                row_string += " " # Space
            # End if
            for c in range(2*self.__board_size + 1): # Column counter
                if (r%2 == 0):
                    row_string += "--" # horizontal lines
                elif (c%2 == 0):
                    row_string += " | " # vertical lines
                else: # game pieces
                    if ((self.black >> square) % 2== 1):
                        row_string += "X" # black stone
                    elif ((self.white >> square) % 2 == 1):
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

    # Declares the winner of the game based on the total number of stones for each player
    def DeclareWinner(self):
        # Declare winner
        [black_total, white_total] = self.CountStones()
        print("Black: {0} - White: {1}".format(black_total, white_total))
        if (black_total == white_total):
            print("It's a tie! Good game.")
        elif (black_total > white_total):
            print("Black wins! Good game.")
        else:
            print("White wins! Good game.")
        # End if
    # End DeclareWinner

    # Returns the number of pieces for each player
    # Returns
    #   black_count = int; Number of bits equal to 1 in self.black
    #   white_count = int; Number of bits equal to 1 in self.white
    def CountStones(self):
        black_count = self.black.bit_count()
        white_count = self.white.bit_count()
        return [black_count, white_count]
    # End CountStones
# End class GameBoard

# Player/AI class that chooses a (valid) move to make on their turn
class Player(): # Does not need to be a child of GameBoard (I think)
    def __init__(self):
        pass
    # End __init__

    # Have player choose a (valid) move
    # Parameters:
    #   valid_dictionary = dictionary;
    #   valid_positions = list;
    # Returns:
    #   move_choice = element from valid_positions;
    def Move(self, valid_dictionary, valid_positions):
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

    # Select a random (valid) move
    # Parameters:
    #   valid_dictionary = dictionary;
    #   valid_positions = list;
    # Returns:
    #   move_choice = element from valid_positions;
    def Randal(self, valid_dictionary, valid_positions):
        move_numbers = [x for x in valid_dictionary.keys()]
        # Select random move from valid_positions
        move_choice = random.choice(move_numbers)

        print("Move selected: {0}".format(valid_positions[move_numbers.index(move_choice)]))
        return move_choice
    # End Randal

    # Select move with most possible flips (choose randomly if multiple)
    # Parameters:
    #   valid_dictionary = dictionary;
    #   valid_positions = list;
    # Returns:
    #   move_choice = element from valid_positions;
    def Maxine(self, valid_dictionary, valid_positions):
        move_numbers = [x for x in valid_dictionary.keys()]
        
        # Select move with most possible flips (choose randomly if multiple)
        move_choices = [] # list of reduced move choices
        max_length = 0 # Start low to increase later
        for move in valid_dictionary.keys():
            current_length = len(valid_dictionary[move])
            if (current_length > max_length):
                max_length = len(valid_dictionary[move])
                move_choices = [] # reset move_choices
                move_choices.append(move) # reset move choices
            elif (current_length < max_length):
                continue # skip this move
            else: # move has same legnth as previous maximum
                move_choices.append(move) # add extra move to list
                # max_length remains unchanged
            # End if
        # End for
        move_choice = random.choice(move_choices)

        print("Move selected: {0}".format(valid_positions[move_numbers.index(move_choice)]))
        return move_choice
    # End Maxine

    # Select move with least possible flips (choose randomly if multiple)
    # Parameters:
    #   valid_dictionary = dictionary;
    #   valid_positions = list;
    # Returns:
    #   move_choice = element from valid_positions;
    def Minnie(self, valid_dictionary, valid_positions):
        move_numbers = [x for x in valid_dictionary.keys()]

        # Select move with least possible flips (choose randomly if multiple)
        move_choices = [] # list of reduced move choices
        min_length = 30 # Start high to decrease later
        for move in valid_dictionary.keys():
            current_length = len(valid_dictionary[move])
            if (current_length < min_length):
                min_length = len(valid_dictionary[move])
                move_choices = [] # reset move_choices
                move_choices.append(move) # reset move choices
            elif (current_length > min_length):
                continue # skip this move
            else: # move has same legnth as previous maximum
                move_choices.append(move) # add extra move to list
                # max_length remains unchanged
            # End if
        # End for
        move_choice = random.choice(move_choices)

        print("Move selected: {0}".format(valid_positions[move_numbers.index(move_choice)]))
        return move_choice
    # End Minnie
# End class CPU