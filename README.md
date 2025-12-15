# Coursework2
Othello/Reversi using a flask web server and html

# Module 1 - components.py
This module is where some the critical functions are for use in both of the game engines. It contains four different functions:
- initialise_board
- print_board
- legal_move
- possible_legal_moves

These functions can be called and re-used so long as the format remains the same.

## initialise_board
This function is used to create a brand new board array with the tokens in the correct place for a default setup of othello. The board is returned as an object. A numpy array is used because it makes it very efficient to broadcast a value across all list values without using a loop.

## print_board
This function is used to print a board that has been passed to it onto the command line using ASCII values. It does this by iterating through and printing row by row based on the contents of the board. This can be used again each time the board is updated to show new player moves. It is printed line by line for each row as just displaying a raw matrix can be confusing and it clutters the command line.
![e087c0d3639611a6de78af8e86d9ed3b.png](../_resources/e087c0d3639611a6de78af8e86d9ed3b.png)

## legal_move
This function is used to check the legality of a particular move that the player has chosen. It takes the board, the players colour and also a tuple of coordinates to make sure the move trying to be made is actually allowed. It returns a True or False boolean value.
![83f51d7326f7bac33f6118ecf9778d9d.png](../_resources/83f51d7326f7bac33f6118ecf9778d9d.png)

## possible_legal_moves
This funtion behaves in a similar way to legal_move but it does it for each value on the board depending on player colour to check if the player has any possible moves available left. Though there are possibly more efficient ways of doing this, it covers the entire board meaning players can be sure that there are no missed legal moves that they could perform.

# Module 2 - game_engine.py
This module is used when playing the game on the command line. It makes use of the functions in components to check if the move is legal, to print the board and update it and also to check the whole board for legal moves. This module contains three different functions:
- cli_coords_input
- form_flip_line
- simple_game_loop

These functions make use of the functions already defined in components.py

## cli_coords_input
This function asks for user input on which row and column they want to pick. The function is a continuous loop that is only broken when a value is returned. It only returns a value if it is within the range of the board. It is returned as a tuple with 1 subtracted from row and column in order to bring both into the proper range of 0 to 7 for indexing. It is used by legal move to make sure the input is actually viable in the main game loop.

# form_flip_line
This function's purpose is to find the coordinates of all opposing tokens that are in a line for a valid move. This works in every direction that is possible. It returns a list with coordinate tuples that can be flipped later. It has a similar functionality to the legal_move function but it will append the coordinates of the whole direction of opponent pieces that are to be flipped rather than just finding pieces. 

## simple_game_loop
This function brings the rest of the functions together and is the main body of the program. It has variables to store current player, number of moves left and the board itself. It has multiple selection statements encompassed in a loop that counts down each move until there are no more moves left. If a move is valid after calling legal_move, it will call form_flip_line and use the output in order to flip each piecs that is part of the valid move. Once this is done the player will change and the new board will be printed. At the end of this function are the win conditions where it will count up the number of each colour on the final board and the player with the highest number will recieve a win message.

# Module 3 - flask_game_engine.py
This module contains the code required to interface with the web server using the html template. It contains a few functions but mostly relies on routes and functions from other files. It has three different functions:
- form_flip_line
- index
- move

  Two of these are the components of a route and the other is the same as in the regular game_engine.py.

## form_flip_line
This function's purpose is to find the coordinates of all opposing tokens that are in a line for a valid move. This works in every direction that is possible. It returns a list with coordinate tuples that can be flipped later. It has a similar functionality to the legal_move function but it will append the coordinates of the whole direction of opponent pieces that are to be flipped rather than just finding pieces. It behaves the same way as the other instance but is not nested in any routes and can be called any time in this file.

## index
This function is there to load the html template onto the flask web server and allows the game board to be sent along with the template. This will render a game board on the webpage in whatever state that gameboard variable was passed to it in. It also sets the board, move count and player colour to the defaults when called to start a new game.

## move
This function behaves in a similar way to the simple_game_loop. It is not quite the same as the while loop is removed due to the fact that a click on the webpage is one loop of the code in this function. It calls the same function as the simple_game_loop and has mostly the same logic but will run based on the coordinates of a click on the board rather than a text input. Information is sent to the web server in json format often to be used on the game log at the bottom of the screen for things like invalid input and win conditions.
