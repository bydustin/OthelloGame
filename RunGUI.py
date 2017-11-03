#Dustin Ngo ID: 77035127

import tkinter
import game_rules

NONE = 0
BLACK = 1
WHITE = 2



_DEFAULT_FONT = ('Helvetica', 9)

class GameBoard:
    #Initializes the GUI Board
    def __init__(self, GameLogic) -> None:

        self._game_window = tkinter.Toplevel()

        self.Game = GameLogic

        self._row_number = self.Game._num_rows
        self._column_number = self.Game._num_columns
        self._corner_color = self.Game._corner_color
        self._winner_type = self.Game._winning_type

        self._B_count = 0
        self._W_count = 0

        self.Game._count_pieces(self)
        self._turn = self.Game._turn
        self._printing_turn(self._turn)


        self._canvas = tkinter.Canvas(master = self._game_window,
                                width = 500, height = 400,
                                background = 'green')
        self._canvas.grid(row = 1, column = 0,
                          padx = 10, pady = 10,
                          sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)

        self._Valid_or_Invalid_Label()

        self._canvas.bind('<Configure>', self._draw_lines)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)

        
        self._game_window.rowconfigure(0, weight = 1)
        self._game_window.columnconfigure(0, weight = 1)
        
    #Draws the lines on the canvas based on user input of number of row/column 
    def _draw_lines(self,event: tkinter.Event) -> None:
        self._canvas.delete(tkinter.ALL)
        
        self._canvas_width = self._canvas.winfo_width()
        self._canvas_height = self._canvas.winfo_height()

        self._row_width = (self._canvas_height/self._row_number)
        self._column_width = (self._canvas_width/self._column_number)

        for x in range(self._column_number):
            which_column = x * self._column_width
            x_coord = which_column + self._column_width
            self._canvas.create_line(x_coord, 0,
                                     x_coord, self._canvas_height)
        for y in range(self._row_number):
            which_row = y * self._row_width
            y_coord = which_row + self._row_width
            self._canvas.create_line(0, y_coord,
                                     self._canvas_width, y_coord)

        self.Game._place_on_board(self)
        self.Game._count_pieces(self)

    #When Canvas is clicked, Do these following actions (aka. Begin the Game)
    def _on_canvas_clicked(self,event: tkinter.Event) -> None:
        x = int(event.x/self._column_width)
        y = int(event.y/self._row_width)
        if self.Game._check_apply_move(self,x,y) != False:
            self._move_valid_text.set("Move: VALID")
            self.Game._apply_flip(self, x,y,self.Game._tiles_to_flip, self.Game._turn)
            self.Game._place_on_board(self)
            B_count, W_count = self.Game._count_pieces(self)
            if self.Game._game_over_checking(self, B_count, W_count) == True:
                if self._winner_type == ">":
                      self.Game._check_most_disc_win(self, B_count,W_count)
              
                if self._winner_type == "<":
                      self.Game._check_least_disc_win(self, B_count,W_count) 
        else:
            self._move_valid_text.set("Move: INVALID")

        
    #Update the Pieces on the GUI Board by going through the Console Board
    #and checking whether they are filled or not.
    def _update_pieces(self, i, j,color_at_coord) -> None:
        if color_at_coord == BLACK:
            color = 'black'
        elif color_at_coord  == WHITE:
            color = 'white'
        oval = self._canvas.create_oval(self._column_width * i, self._row_width * j,
                                               self._column_width * (i+1), self._row_width * (j+1),
                                               fill = color)
    #Updates GUI label regarding move is invalid or valid
    def _Valid_or_Invalid_Label(self) -> None:
        self._move_valid_text = tkinter.StringVar()
        self._move_valid_text.set('')
        self.Move_Status_Label = tkinter.Label(master = self._game_window,
                                      textvariable = self._move_valid_text,
                                      font = _DEFAULT_FONT)
        self.Move_Status_Label.grid(row = 2, column = 0,
                              padx = 10, pady = 10,
                              sticky = tkinter.W)
    #Updates the GUI regarding Total Disc of Each Color
    def _update_color_total(self, B_count,W_count) -> None:
        self.count_label = tkinter.Label(master = self._game_window,
                                      text = 'B: {}  W: {}'.format(B_count,W_count),
                                      font = _DEFAULT_FONT)
        self.count_label.grid(row = 0, column = 0,
                              padx = 10, pady = 10,
                              sticky = tkinter.E)

    #Updates the GUI regarding Turns
    def _printing_turn(self,turn) -> int:
        if turn == BLACK:
            color = "BLACK"
        if turn == WHITE:
            color = "WHITE"
        self._turn_label = tkinter.Label(master = self._game_window,
                                         text = 'Current Turn: {}'.format(color),
                                         font = _DEFAULT_FONT)
        self._turn_label.grid(row = 0, column = 0,
                              padx = 10, pady = 10,
                              sticky = tkinter.W)

    
         
class GUI_board:
    def __init__(self):
        self._root_window = tkinter.Tk()

        intro_label = tkinter.Label(master = self._root_window,
                                    text = "Welcome to Othello!",
                                    font = _DEFAULT_FONT)
        intro_label.grid(row = 0, column = 0,
                         padx = 10, pady = 10,
                         sticky = tkinter.W)

###
        row_number_label = tkinter.Label(master = self._root_window,
                                         text = 'Row Number (>= 4, Even Numbers Only):',
                                         font = _DEFAULT_FONT)
        row_number_label.grid(row = 1, column = 0,
                              padx = 10, pady = 10,
                              sticky = tkinter.W)

###
        
        self._row_number_entry = tkinter.Entry(master = self._root_window,
                                               width = 20,
                                               font = _DEFAULT_FONT)
        self._row_number_entry.grid(row = 1, column = 1,
                                    padx = 10, pady = 10,
                                    sticky = tkinter.W)
        
###
        
        column_number_label = tkinter.Label(master = self._root_window,
                                         text = 'Column Number (>= 4, Even Numbers Only):',
                                         font = _DEFAULT_FONT)
        column_number_label.grid(row = 2, column = 0,
                              padx = 10, pady = 10,
                              sticky = tkinter.W)

###
        self._column_number_entry = tkinter.Entry(master = self._root_window,
                                               width = 20,
                                               font = _DEFAULT_FONT)
        self._column_number_entry.grid(row = 2, column = 1,
                                    padx = 10, pady = 10,
                                    sticky = tkinter.W)

###
        
        black_or_white_move_label = tkinter.Label(master = self._root_window,
                                         text = 'Black or White First Move (B or W):',
                                         font = _DEFAULT_FONT)
        black_or_white_move_label.grid(row = 3, column = 0,
                              padx = 10, pady = 10,
                              sticky = tkinter.W)

###
        self._black_or_white_move_entry = tkinter.Entry(master = self._root_window,
                                               width = 20,
                                               font = _DEFAULT_FONT)
        self._black_or_white_move_entry.grid(row = 3, column = 1,
                                    padx = 10, pady = 10,
                                    sticky = tkinter.W)

###
        
        top_left_color_label = tkinter.Label(master = self._root_window,
                                         text = 'Top Left Corner Color? (B or W):',
                                         font = _DEFAULT_FONT)
        top_left_color_label.grid(row = 4, column = 0,
                              padx = 10, pady = 10,
                              sticky = tkinter.W)

###
        self._top_left_color_entry = tkinter.Entry(master = self._root_window,
                                               width = 20,
                                               font = _DEFAULT_FONT)
        self._top_left_color_entry.grid(row = 4, column = 1,
                                    padx = 10, pady = 10,
                                    sticky = tkinter.W)
        
###

        less_or_more_disc_label = tkinter.Label(master = self._root_window,
                                         text = 'Least or Most Disc Winner (< or >):',
                                         font = _DEFAULT_FONT)
        less_or_more_disc_label.grid(row = 5, column = 0,
                              padx = 10, pady = 10,
                              sticky = tkinter.W)

###
        self._less_or_more_disc_entry = tkinter.Entry(master = self._root_window,
                                               width = 20,
                                               font = _DEFAULT_FONT)
        self._less_or_more_disc_entry.grid(row = 5, column = 1,
                                    padx = 10, pady = 10,
                                    sticky = tkinter.W)
###
        new_game_button = tkinter.Button(master = self._root_window,
                                  text = "Create New Game",
                                  font = _DEFAULT_FONT,
                                  command = self._new_game_button_pressed)
        new_game_button.grid(row = 0, column = 1,
                             padx = 10, pady = 10,
                             sticky = tkinter.S)

    def start(self):
        self._root_window.mainloop()

    def _new_game_button_pressed(self):
        row_number = int(self._row_number_entry.get())
        column_number = int(self._column_number_entry.get())
        turn = self._black_or_white_move_entry.get().upper()
        corner_color = self._top_left_color_entry.get().upper()
        winner_type = self._less_or_more_disc_entry.get()
        if turn == "B":
            turn = BLACK
        if turn == "W":
            turn = WHITE
        GameLogic = game_rules.Game_Logic(row_number, column_number, turn, corner_color, winner_type)
        Game_Board = GameBoard(GameLogic)
        
            
    
if __name__ == '__main__':
    GUI_board().start()
