from flask import Flask, render_template, request, jsonify
import components as cmp
import numpy as np

app = Flask(__name__)

# Global variables allow for consistent use across each route
board = None
mv_count = 60
player = "Dark "

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

@app.route("/index", methods=["GET"]) # Initialised a brand new board using the index.html template 
def index():
    global board, mv_count, player
    board = cmp.initialise_board()
    mv_count = 60
    player = "Dark "
    return render_template("index.html", game_board=board)

@app.route("/move", methods=["GET"])
def move():
    global board, mv_count, player

    if mv_count == 0: # While loop for win conditions is removed in place of a new method due to how flask operations work in this case
        dark = np.count_nonzero(board == "Dark ") # Counts number of player pieces
        light = np.count_nonzero(board == "Light")
        if dark > light: # Win conditions
            win_mess = f"Dark has won with a total of {dark} tokens on the board."
        elif dark < light:
            win_mess = f"Light has won with a total of {light} tokens on the board."
        else:
            win_mess = "There is a draw."
        return jsonify({"status": "finished", "board":board, "finished":win_mess}) # Returns win message and final board in json format to the web server

    row = int(request.args.get("x"))-1 # Gets row position from the player click on the web page and does -1 to bring the value into the range 0 to 7
    column = int(request.args.get("y"))-1 # Gets column position from the player click on the web page and does -1 to bring the value into the range 0 to 7

    coords = (column, row) # Creates a tuple out of column and row for the functions inherited from components

    if cmp.possible_legal_moves(player, board) == True: # Checks for any viable moves for current player
        if cmp.legal_move(player, coords, board) == True: # Checks if move is legal
            row, column = coords
            board[row][column] = player
            token_c = form_flip_line(player, coords, board) # Sets variable to list of tuples of coords that need to be flipped
            for i, j in token_c: # Loops and flips opposition tokens 
                board[i][j] = player             
            mv_count -= 1 # decrements the counter, this acts on the global variable too as they were declared at the top of this function as globals
            player = "Dark " if player == "Light" else "Light" # Swaps player 
            return jsonify({"status":"success", "board":board, "player":player}) # Returns the new board and player in a json format to the web server
        else:
            return jsonify({"status":"fail", "message":"Illegal move. Try another coordinate."}) # Sents an illegal move message to the web server for display
    else:
        player_next = "Dark " if player == "Light" else "Light" # Sets new variable for the next player

        if cmp.possible_legal_moves(player_next, board) == False:
            mv_count = 0 # Reuses logic from the win condition section to register a game over when no player can perform a legal move
            player = player_next # Players are swapped
            return move() # Uses recursion to check that both players do not have a legal move
        player = player_next # Swaps player
        return jsonify({"status":"fail", "board":board, "player":player, "message":"Current player has no legal moves. This turn has been passed."}) # Json message to the web server for no legal moves display

if __name__ == "__main__":
    app.run()

