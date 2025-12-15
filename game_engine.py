import components as cmp
import numpy as np

def cli_coords_input():
    while True: # Loops until the input is valid
        row = int(input("Enter the desired row: ")) # Requests row
        column = int(input("Enter the desired column: ")) # Requests column
        if not(1 <= row <= 8) or not(1 <= column <= 8): # Checks if input is in range of the board
            print("Please enter numbers within the range of the board!") # Failure message
        else:
            return (row-1, column-1) # -1 from the input values to bring it into array index range of 0 to 7
        
def form_flip_line(player, coords, board): # Behaves similarly to the legal_move and possible_legal_move functions but appends coordinates of opponent pieces to flip in each viable direction as tuples and returns them
    directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    opp = "Dark " if player == "Light" else "Light"
    row, column = coords
    all_direction_tokens = [] # Coord tuples of opposing player tokens in each direction between players tokens to be flipped
    for x, y in directions:
        row_d = row + x
        column_d = column + y
        count = 0
        token_c = [] # Temp list for one direction
        while 0<= row_d < len(board) and 0 <= column_d < len(board) and opp == board[row_d][column_d]:
            token_c.append((row_d, column_d)) # Adds to temp list at each new position
            row_d += x
            column_d += y
            count += 1                    
        if count >= 1 and 0<= row_d < len(board) and 0 <= column_d < len(board) and board[row_d][column_d] == player:
            all_direction_tokens.extend(token_c) # Adds whole temp list to main list
    return all_direction_tokens

def simple_game_loop():
    print("Welcome to the game of Othello/Reversi!")
    board = cmp.initialise_board() # Initialised board with default setup 
    cmp.print_board(board) # Uses set up board and prints
    mv_count = 60 # Move counter
    player = "Dark " # Sets first player to dark
    while mv_count != 0: # Loops until the players have used up all their moves
        print(f"Current player is {player}")
        if cmp.possible_legal_moves(player, board) == True: # Does the player have any legal moves available
            legal_check = False
            coords = (-1, -1) # Sets impossible coordinates to begin with that will not throw an index error
            while legal_check == False: # Loops until a legal move has been selected
                coords = cli_coords_input() # Calls cli_coords_input to get a new set of coords
                legal_check = cmp.legal_move(player, coords, board) # Sets legal_check to the result of legal_move, True or False
                if legal_check == False: # If a bad coord is input a message will also be sent to console
                    print("Illegal move. Try another coordinate.")
            row, column = coords # Splits coord tuple
            board[row][column] = player # Sets chosen coord to the player colour
            token_c = form_flip_line(player, coords, board) # Gets a list of all tokens that need to be flipped in all directions
            for i, j in token_c: # Loops through provided coords
                board[i][j] = player # Sets opposing players tokens in the move to player colour             
            mv_count -= 1 #  Decrements the move count
            cmp.print_board(board) # Prints the new updated board
            player = "Dark " if player == "Light" else "Light" # Swaps player
        else:
            print("Current player has no legal moves. This turn has been passed.")
            player_next = "Dark " if player == "Light" else "Light" # Sets new variable to next player for possible game end logic

            if cmp.possible_legal_moves(player_next, board) == False:
                mv_count = 0 # Reuses while loop logic in order to end the game when both players no longer have legal moves
            player = player_next # Switches player colour

    dark = np.count_nonzero(board == "Dark ") # Counts number of colours on the board
    light = np.count_nonzero(board == "Light")
    if dark > light:
        print(f"Dark has won with a total of {dark} tokens on the board.") # Win conditions
    elif dark < light:
        print(f"Dark has won with a total of {light} tokens on the board.")
    else:
        print("There is a draw.")

if __name__ == "__main__": 
    simple_game_loop()
