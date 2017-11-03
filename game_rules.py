#Author: Dustin Ngo

import tkinter
import RunGUI

NONE = 0
BLACK = 1
WHITE = 2

_DEFAULT_FONT = ('Helvetica', 9)

class Game_Logic:
    #Initialize the Console Board
    def __init__(self, num_rows, num_columns, turn, corner_color, winner_type) -> None:
        board = []

        self._num_rows = num_rows
        self._num_columns = num_columns
        self._turn = turn

        for col in range(self._num_columns):
            board.append([])
            for row in range(self._num_rows):
                board[-1].append(0)
                    
        if corner_color == 'B':
            board[int(self._num_columns/2-1)][int(self._num_rows/2)-1] = BLACK
            board[round(self._num_columns/2)][round(self._num_rows/2)] = BLACK
            board[int(self._num_columns/2-1)][round(self._num_rows/2)] = WHITE
            board[round(self._num_rows/2)][int(self._num_rows/2)-1] = WHITE
        if corner_color == 'W':
            board[int(self._num_columns/2-1)][int(self._num_rows/2)-1] = WHITE
            board[round(self._num_columns/2)][round(self._num_rows/2)] = WHITE
            board[int(self._num_columns/2-1)][round(self._num_rows/2)] = BLACK
            board[round(self._num_rows/2)][int(self._num_rows/2-1)] = BLACK

        self._board = board
        self._corner_color = corner_color
        self._winning_type = winner_type
        

    #Counts the black and white pieces on the console board.
    def _count_pieces(self, GameBoard) -> int:
        B = 0
        W = 0
        for row in range(self._num_rows):
            for column in range(self._num_columns):
                if self._board[row][column] == BLACK:
                    B += 1
                if self._board[row][column] == WHITE:
                    W += 1
        GameBoard._update_color_total(B, W)
        return B,W

    #Checks if the user's move is within the boundaries of the board
    def _check_on_board(self,x,y):
        if x >= self._num_rows or x < 0 or y < 0 or y >= self._num_columns:
            return False
        else:
            return True
        
    #Switches Turn as well as Updates the Label on the GUI
    def _switch_turns(self, GameBoard) -> int:
        if self._turn == BLACK:
            self._turn = WHITE
        else:
            self._turn = BLACK
        GameBoard._printing_turn(self._turn)

    #Updates the GUI Board by using the filled spaces of the console board
    def _place_on_board(self, GameBoard) -> bool:
        for i in range(self._num_rows):
            for j in range(self._num_columns):
                if self._board[i][j] != 0:
                    GameBoard._update_pieces(i,j, self._board[i][j])
        
    #Checks if the input coordinates are empty,which is 0 or NONE.
    def _is_space_empty(self, x,y) -> bool:
        if self._board[x][y] == 0:
            return True
        else:
            return False

    #Checks the Board, Returning a List of Possible Flips            
    def _check_apply_move(self, GameBoard, x,y) -> bool or list:
        
        direction_to_check=[[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1]]

        self._tiles_to_flip = []

        if self._turn == BLACK:
            color = BLACK
            other_color = WHITE
        if self._turn == WHITE:
            color = WHITE
            other_color = BLACK

        if self._is_space_empty(x,y) == True: 
            for x_check, y_check in direction_to_check:
                new_x = x
                new_y = y
                new_x += x_check
                new_y += y_check
                if self._check_on_board(new_x, new_y) and self._board[new_x][new_y] == other_color:
                    new_x += x_check
                    new_y += y_check
                    if self._check_on_board(new_x, new_y) != True:
                        continue
                    while self._board[new_x][new_y] == other_color:
                        new_x += x_check
                        new_y += y_check
                        if self._check_on_board(new_x, new_y) != True:
                            break
                    if self._check_on_board(new_x, new_y) != True:
                        continue 
                    if self._board[new_x][new_y] == color:
                        while True:
                            new_x -= x_check
                            new_y -= y_check
                            if new_x == x and new_y == y:
                                break
                            else:
                                self._tiles_to_flip.append([new_x, new_y])
        else:
            return False
        if len(self._tiles_to_flip) == 0:
                return False
        return True

            
    #Applies the Flip to the GUI
    def _apply_flip(self,GameBoard, x,y,tiles_to_flip, color) -> None:
        self._board[x][y] = color
        for x,y in self._tiles_to_flip:
            self._board[x][y] = color
        self._switch_turns(GameBoard)

    #Gets the total amount of moves left by both players
    def _get_Valid_Moves(self, GameBoard) -> list:

        self._valid_move_list = []
        
        for i in range(self._num_rows):
            for j in range(self._num_columns):
                if self._is_space_empty(i,j) == True:
                    if self._check_apply_move(GameBoard, i, j) == True:
                        self._valid_move_list.append([i,j])
                else:
                    continue
        return self._valid_move_list
                    
    #Function to check whether or not the game is over or not through various conditions
    def _game_over_checking(self, GameBoard, B_count, W_count) -> bool:
        Valid_Move_List = self._get_Valid_Moves(GameBoard)
        if B_count + W_count == (self._num_rows * self._num_columns) or B_count == 0 or W_count == 0 or len(Valid_Move_List) == 0:
            return True  
        else:
            return False


    def _check_most_disc_win(self, GameBoard, B_count, W_count) -> None:
        self._winner_text = tkinter.StringVar()
        self._winner_text.set('')
        self._winner_label = tkinter.Label(master = GameBoard._game_window,
                                      textvariable = self._winner_text,
                                      font = _DEFAULT_FONT)
        self._winner_label.grid(row = 2, column = 0,
                              padx = 10, pady = 10,
                              sticky = tkinter.E )
        if B_count > W_count:
            self._winner_text.set('Winner:  BLACK')
        if W_count > B_count:
            self._winner_text.set('Winner:  WHITE')
        if B_count == W_count:
            self._winner_text.set('Winner:  NONE')

    
    def _check_least_disc_win(self, GameBoard, B_count, W_count) -> None:
        self._winner_text = tkinter.StringVar()
        self._winner_text.set('')
        self._winner_label = tkinter.Label(master = GameBoard._game_window,
                                      textvariable = self._winner_text,
                                      font = _DEFAULT_FONT)
        self._winner_label.grid(row = 2, column = 0,
                              padx = 10, pady = 10,
                              sticky = tkinter.E )
        if B_count < W_count:
            self._winner_text.set('Winner:  BLACK')
        if W_count < B_count:
            self._winner_text.set('Winner:  WHITE')
        if B_count == W_count:
            self._winner_text.set('Winner:  BLACK')


   
