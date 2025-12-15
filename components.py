import numpy as np

def initialise_board(size=8):
    board = np.full((size, size), "None ") # Creates a numpy array full of "None "
    rows = [3, 4, 4, 3]
    columns = [3, 4, 3, 4]
    values = ["Light", "Light", "Dark ", "Dark "]
    board[rows, columns] = values # Assigns "Light" and "Dark " in the othello starting arrangement using the indexes and colours above    
    return board.tolist()

def print_board(board):
    row_text = "  ________________" # Sets first instance of row_text to a border line for the labels
    print("   1 2 3 4 5 6 7 8") # Prints the number labels of the board
    for row_i, row_v in enumerate(board): # Loops through board, or in this case each row, providing a count and a value (column lists)
        print(row_text) # Prints each formed row
        row_text = f"{row_i+1}| " # Sets first part of row to row number
        for column_v in row_v: # Loops through column lists for values
            if column_v == "Light":
                row_text = row_text + "L " # Adds L to row_text
            elif column_v == "Dark ":
                row_text = row_text + "D " # Adds D to row_text
            else:
                row_text = row_text + "X " # Adds X to row_text
    print(row_text) # Prints final row

def legal_move(colour, coord, board):
    row, column = coord # Coord tuple split into rows and columns
    directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)) # All 8 possible directions
    opp = "Dark " if colour == "Light" else "Light" # Reverses current player colour to get opponent
    
    if board[row][column] != "None ": # Checks if chosen coord is filled already
        return False
    for x, y in directions: # Loops through direction tuples
        row_d = row + x # This and the following add direction to chosen row to find the next coordinate in a certain direction
        column_d = column + y
        count = 0
        while 0 <= row_d < len(board) and 0 <= column_d < len(board) and opp == board[row_d][column_d]: # loops while coords are in bounds of board and current coords are an opposing colour
            row_d += x
            column_d += y
            count += 1
        if count >= 1 and 0<= row_d < len(board) and 0 <= column_d < len(board) and board[row_d][column_d] == colour: # If there has been at least one opposing players token between the move and a current player token then return True 
            return True
    return False # If no direction returns True, then return False

def possible_legal_moves(colour, board): # Does the same thing as the legal_move function but does it for every square on the board to check all possible moves
    directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    opp = "Dark " if colour == "Light" else "Light"
    coords = []
    for a in range(len(board)):
        for b in range(len(board[a])):
            coords.append((a, b))
    for row, column in coords:
        for x, y in directions:
            row_d = row + x
            column_d = column + y
            count = 0
            while 0<= row_d < len(board) and 0 <= column_d < len(board) and opp == board[row_d][column_d]:
                row_d += x
                column_d += y
                count += 1
            if count >= 1 and 0<= row_d < len(board) and 0 <= column_d < len(board) and board[row_d][column_d] == colour and board[row][column] == "None ":
                return True
    return False
