# ReversiClasses.py
# Purpose: File for holding python classes related to ReversiAI.py
# Author: Timothy Anglea
# Last Modified: 7/26/23

class GameBoard:
    # Create game board variables and state
    def __init__(self):
        self.__board_size = 8 # Size of board (size x size)
        self.board_positions = [] # possible board selections
        self.__row_names = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.__column_names = ["1", "2", "3", "4", "5", "6", "7", "8"]
        for row in self.__row_names:
            for column in self.__column_names:
                self.board_positions.append(row+column)
            # End for column
        # End for row
        # Initialize state of board
        [self.black, self.white] = self.__InitializeBoard()

    # End __init__

    # Sets initial configuration for the game board
    # Returns:
    #   b = int; bit map of black stones on the board
    #   w = int; bit map of white stones on the board
    def __InitializeBoard(self):
        # Starting position for game
        w = 0x0000001008000000
        b = 0x0000000810000000
        # basic check for board state
        if (b & w > 0):
            print("ERROR: two stones on same square")
        # End if
        return [b, w]
    # End InitializeBoard

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
# End class Board