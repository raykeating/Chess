import numpy as np
import copy

# SAN_to_int - SAN is standard algebraic notation, the way pieces are represented in FEN strings.  
# this method converts the SAN character to the integer representation as used here. (used in parse_board in board.py)
def SAN_to_int(piece:str):
    pieces = [(1,'K'),(2,'k'),(3,'Q'),(4,'q'),(5,'B'),(6,'b'),(7,'N'),(8,'n'),(9,'R'),(10,'r'),(11,'P'),(12,'p')]
    for p in pieces:
        if piece == p[1]:
            return p[0]
    return 0

def get_symbol(piece:int, invert_colors:bool):
    if piece == 0:
        return ' '
    pieces = [(1,'\u2654'),(2,'\u265A'),(3,'\u2655'),(4,'\u265B'),(5,'\u2657'),(6,'\u265D'),
    (7,'\u2658'),(8,'\u265E'),(9,'\u2656'),(10,'\u265C'),(11,'\u2659'),(12,'\u265F')]
    if invert_colors:
        pieces = [(1,'\u265A'),(2,'\u2654'),(3,'\u265B'),(4,'\u2655'),(5,'\u265D'),(6,'\u2657'),
    (7,'\u265E'),(8,'\u2658'),(9,'\u265C'),(10,'\u2656'),(11,'\u265F'),(12,'\u2659')]
    for p in pieces:
        if piece == p[0]:
            return p[1]
    return ValueError("That is an invalid piece")

class BoardState:
    # board - an 8x8 numpy array representing the actual pieces on the board.  Pieces are represented as integers. 
    board = None
    current_move = None # nextMove - 0 or 1.  Indicates who's move it is.  (0 for black, 1 for white)

    # castling = boolean array, index 0,1 indicate if white can castle kingside or queenside (respectively), 
    # index 2,3 indicate if black can castle kingside, queenside (respectively)
    castling = None

    # enPassant - an integer tuple with value (r,f): r is the rank, f is the integer value of the file
    en_passant = None
    
    # hm_clock, fm_clock - integers representing the halfmove clock and fullmove clock.  
    # halfmove is used for the fifty-move rule.
    hm_clock = None
    fm_clock = None

    white_in_check = False
    white_checkmated = False
    black_in_check = False
    black_checkmated = False

    # initialize a board state with a fen string
    def __init__(self, fen):
        self.fen_to_board_state(fen)

    def printb(self, invert_colors):
        print("  ---------------------------------")
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if j == 0: print(f'{(8-i)} |', end=" ") 
                print(get_symbol(self.board[i][j], invert_colors), end=" | ")
            print("\n  ---------------------------------")
        print("    A   B   C   D   E   F   G   H ")

    def fen_to_board_state(self, fen:str):

        # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 -> fen for starting position

        board = fen.split(' ')[0]
        self.board = self.parse_board(board)
        self.current_move = 1 if fen.split(' ')[1] == 'w' else 0

    def parse_board(self, board:str):
        fen_ranks = board.split('/')
        int_ranks = []
        for rank in fen_ranks:
            # This for loop basically says "if the piece is a piece", convert to its integer representation.
            # otherwise, fill the empty tiles indicated by the int value in the FEN
            int_rank = []
            for piece in rank:
                if piece in "PRNBKQprnbkq":
                    int_rank.append(SAN_to_int(piece))
                elif piece in "12345678" and int(piece) > 0 and int(piece) < 9:
                    for i in range(int(piece)):
                        int_rank.append(0)
                else:
                    return ValueError("The FEN string may be invalid")

            int_ranks.append(int_rank)
            int_rank = []
            
        # return numpy array of the ranks.
        return np.array(int_ranks)

    def move_piece(self, r1, f1, r2, f2):   
        if (r2,f2) in self.get_legal_moves(r1,f1):
            piece = self.board[r1][f1]
            self.board[r1][f1] = 0
            self.board[r2][f2] = piece
            self.current_move = 1 if self.current_move == 0 else 0 # change to next move

    def legal_pawn_moves(self, color, rank, file):
        legal_moves = []
        
        # LEGAL MOVES FOR WHITE
        if color == 'w':
            # allows pawns to move 2 squares on their first move.
            if rank == 6 and self.board[4][file] == 0:
                legal_moves.append((4, file))
        
            # if the square infront of a pawn is empty, it can move there
            if rank-1 > -1:
                if self.board[rank-1][file] == 0:
                    legal_moves.append(((rank-1), file))


            # check if left or right diagonal captures are possible
            if rank-1 > -1 and rank-1 < 8 and file+1 > -1 and file+1 < 8:
                if self.board[rank-1][file+1] != 0 and self.board[rank-1][file+1] % 2 == 0:
                    legal_moves.append(((rank-1),(file+1)))

            if rank-1 > -1 and rank-1 < 8 and file-1 > -1 and file-1 < 8:
                if self.board[rank-1][file-1] != 0 and self.board[rank-1][file-1] % 2 == 0:
                    legal_moves.append(((rank-1),(file-1)))
        
        # LEGAL MOVES FOR BLACK
        elif color == 'b':
            # allows pawns to move 2 squares on their first move.
            if rank == 1 and self.board[3][file] == 0: #check if indexing is right here
                legal_moves.append((3, file))
            
            # if the square infront of a pawn is empty, it can move there
            if rank+1 < 8:
                if self.board[rank+1][file] == 0:
                    legal_moves.append(((rank+1), file))

            # check if left or right diagonal captures are possible
            if rank+1 > -1 and rank+1 < 8 and file+1 > -1 and file+1 < 8:
                if self.board[rank+1][file+1] != 0 and self.board[rank+1][file+1] % 2 == 1:
                    legal_moves.append(((rank+1),(file+1)))


            if rank+1 > -1 and rank+1 < 8 and file-1 > -1 and file-1 < 8:
                if self.board[rank+1][file-1] != 0 and self.board[rank+1][file-1] % 2 == 1:
                    legal_moves.append(((rank+1),(file-1)))

        else:
            return ValueError("wrong color argument")
        return legal_moves

    def legal_rook_moves(self, color, rank, file):
        
        legal_moves = []
        # downwards
        counter = 1
        while rank+counter < 8:
            if self.board[rank + counter][file] == 0:
                legal_moves.append((rank+counter,file))
            elif color == 'w' and self.board[rank + counter][file] % 2 == 0:
                legal_moves.append((rank+counter,file))
                break
            elif color == 'b' and self.board[rank + counter][file] % 2 == 1:
                legal_moves.append((rank+counter,file))
                break
            else:
                break
            counter += 1

        # upwards
        counter = 1
        while rank-counter > -1:
            if self.board[rank - counter][file] == 0:
                legal_moves.append((rank-counter,file))
            elif color == 'w' and self.board[rank - counter][file] % 2 == 0:
                legal_moves.append((rank-counter,file))
                break
            elif color == 'b' and self.board[rank - counter][file] % 2 == 1:
                legal_moves.append((rank-counter,file))
                break
            else:
                break
            counter += 1
        
        # right
        counter = 1
        while file+counter < 8:
            if self.board[rank][file + counter] == 0:
                legal_moves.append((rank,(file+counter)))
            elif color == 'w' and self.board[rank][file + counter] % 2 == 0:
                legal_moves.append((rank,(file+counter)))
                break
            elif color == 'b' and self.board[rank][file + counter] % 2 == 1:
                legal_moves.append((rank,(file+counter)))
                break
            else:
                break
            counter += 1

        # left
        counter = 1
        while file-counter > -1:
            if self.board[rank][file - counter] == 0:
                legal_moves.append((rank,(file-counter)))
            elif color == 'w' and self.board[rank][file - counter] % 2 == 0:
                legal_moves.append((rank,(file-counter)))
                break
            elif color == 'b' and self.board[rank][file - counter] % 2 == 1:
                legal_moves.append((rank,(file-counter)))
                break
            else:
                break
            counter += 1
            
        return legal_moves

    def legal_bishop_moves(self, color, rank, file):
        
        legal_moves = []

        # diagonal from piece to top-left
        counter = 1
        while rank-counter > -1 and rank-counter < 8 and file-counter > -1 and file-counter < 8:
            if self.board[rank - counter][file - counter] == 0:
                legal_moves.append((rank-counter,file-counter))
            elif color == 'w' and self.board[rank - counter][file - counter] % 2 == 0:
                legal_moves.append((rank-counter,file-counter))
                break
            elif color == 'b' and self.board[rank - counter][file - counter] % 2 == 1:
                legal_moves.append((rank-counter,file-counter))
                break
            else:
                break
            counter += 1
        
        # diagonal from piece to top-right
        counter = 1
        while rank-counter > -1 and rank-counter < 8 and file+counter > -1 and file+counter < 8:
            if self.board[rank - counter][file + counter] == 0:
                legal_moves.append((rank-counter,file+counter))
            elif color == 'w' and self.board[rank - counter][file + counter] % 2 == 0:
                legal_moves.append((rank-counter,file+counter))
                break
            elif color == 'b' and self.board[rank - counter][file + counter] % 2 == 1:
                legal_moves.append((rank-counter,file+counter))
                break
            else:
                break
            counter += 1
        
        # diagonal from piece to bottom-left
        counter = 1
        while rank+counter > -1 and rank+counter < 8 and file+counter > -1 and file+counter < 8:
            if self.board[rank + counter][file + counter] == 0:
                legal_moves.append((rank+counter,file+counter))
            elif color == 'w' and self.board[rank + counter][file + counter] % 2 == 0:
                legal_moves.append((rank+counter,file+counter))
                break
            elif color == 'b' and self.board[rank + counter][file + counter] % 2 == 1:
                legal_moves.append((rank+counter,file+counter))
                break
            else:
                break
            counter += 1
        
        # diagonal from piece to bottom-right
        counter = 1
        while rank+counter > -1 and rank+counter < 8 and file-counter > -1 and file-counter < 8:
            if self.board[rank + counter][file - counter] == 0:
                legal_moves.append((rank+counter,file-counter))
            elif color == 'w' and self.board[rank + counter][file - counter] % 2 == 0:
                legal_moves.append((rank+counter,file-counter))
                break
            elif color == 'b' and self.board[rank + counter][file - counter] % 2 == 1:
                legal_moves.append((rank+counter,file-counter))
                break
            else:
                break
            counter += 1

        return legal_moves

    def legal_knight_moves(self, color, rank, file):
        legal_moves = []
        offsets = [(2,1),(2,-1),(1,-2),(1,2),(-1,2),(-1,-2),(-2,1),(-2,-1)]
        for x, y in offsets:
            if rank+x > -1 and rank+x < 8 and file+y > -1 and file+y < 8:
                if self.board[rank+x][file+y] == 0:
                    legal_moves.append((rank+x,file+y))
                elif color == 'w' and self.board[rank+x][file+y] % 2 == 0:
                    legal_moves.append((rank+x,file+y))
                elif color == 'b' and self.board[rank+x][file+y] % 2 == 1:
                    legal_moves.append((rank+x,file+y))
                else:
                    continue
        
        return legal_moves

    def legal_king_moves(self, color, rank, file):
        # get the legal king moves.  Note, this doesn't check whether the king will be in check from a move.
        legal_moves = []
        offsets = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
        for x, y in offsets:
            if (rank+x > -1 and rank+x < 8) and (file+y > -1 and file+y < 8):
                if self.board[rank+x][file+y] == 0: 
                    legal_moves.append((rank+x,file+y))
                elif color == 'w' and self.board[rank+x][file+y] % 2 == 0:
                    legal_moves.append((rank+x,file+y))
                elif color == 'b' and self.board[rank+x][file+y] % 2 == 1:
                    legal_moves.append((rank+x,file+y))
                else:
                    continue
        
        return legal_moves

    def verify_move(self, r1, f1, r2, f2):
        # given a psuedolegal move, go through every psuedolegal move of the opponent to see if it results in a capture of the king.
        # If it does, the move is not a legal move.
        color = self.board[r1][f1] % 2
        opponent_responses = []
        resulting_board = get_board_from_move(self, r1, f1, r2, f2) # get the board resulting from a psuedolegal move
        # check every opponent response in the resulting board.  If any of the results end up with the king being captured, return false.
        for rank in range(8):
            for file in range(8):
                if resulting_board.board[rank][file] != 0 and resulting_board.board[rank][file] % 2 != color:
                    opponent_responses += resulting_board.get_psuedolegal_moves(rank, file)

        try:
            king_rank, king_file = resulting_board.find_king(color)
        except IndexError:
            return True

        return False if (king_rank, king_file) in opponent_responses else True

    def in_check(self, color):
        try:
            king_rank, king_file = self.find_king(color)
        except IndexError:
            return True
        return not self.verify_move(king_rank, king_file, king_rank, king_file)

    def in_checkmate(self, color):
        # although this is a brute force approach, I will just loop through each possible move, for each piece of the current_move player, 
        # and determine whether that BoardState object resulting from the move is in check or not.
        moves = []
        color = 1 if color == 'w' else 0
        moves = self.get_all_legal_moves(color) # check whether it's ok that this calls get_legal_moves vs get_psuedolegal_moves

        for move in moves:
            new_board = get_board_from_move(self, move[0][0], move[0][1], move[1][0], move[1][1])
            if not new_board.in_check(color):
                return False
        
        return True
                    
    def find_king(self, color):
        if color == 'w' or color == 1:
            king_pos = np.where(self.board==1)
            return king_pos[0][0], king_pos[1][0]
        elif color == 'b' or color == 0:
            king_pos = np.where(self.board==2)
            return king_pos[0][0], king_pos[1][0]

    def get_psuedolegal_moves(self, rank, file):
        # this function gets all the legal moves for a SINGLE PIECE indicated with rank, file.
        # this function doesn't check whether the move will result in the king being in check.
        # This is handled in the get_legal_moves function

        # save the piece's integer representation (0 to 12) in piece
        piece = self.board[rank][file]
        color = 'b' if piece % 2 == 0 else 'w'
        
        # all of the legal_piece_moves() functions are psuedolegal, meaning they don't check 
        # whether the move will result in a check of their own king.
        if piece == 11 or piece == 12:
            psuedolegal_moves = self.legal_pawn_moves(color, rank, file)
            return psuedolegal_moves
        
        elif piece == 9 or piece == 10:
            psuedolegal_moves = self.legal_rook_moves(color, rank, file)
            return psuedolegal_moves

        elif piece == 7 or piece == 8:
            psuedolegal_moves = self.legal_knight_moves(color, rank, file)
            return psuedolegal_moves

        elif piece == 5 or piece == 6:
            psuedolegal_moves = self.legal_bishop_moves(color, rank, file)
            return psuedolegal_moves
        
        elif piece == 3 or piece == 4:
            # legal queen moves are combination of rook moves and bishop moves
            psuedolegal_moves = self.legal_rook_moves(color, rank, file)
            psuedolegal_moves += self.legal_bishop_moves(color, rank, file)
            return psuedolegal_moves

        elif piece == 1 or piece == 2:
            psuedolegal_moves = self.legal_king_moves(color, rank, file)
            return psuedolegal_moves

        return [] # return empty if the piece is invalid
    
    def get_legal_moves(self, rank, file):
        psuedolegal_moves = self.get_psuedolegal_moves(rank, file)
        legal_moves = []
        for move in psuedolegal_moves:
            if self.verify_move(rank, file, move[0], move[1]):
                legal_moves.append((move[0], move[1]))
        return legal_moves

    def get_all_legal_moves(self, color):
        # I will just loop through each possible move, for each piece of the current_move player, 
        # and call get_legal_moves.  Returns moves as double tuple of start (rank, file) and end (rank, file)
        all_legal_moves = []
        color = 1 if color == 'w' else 0
        for rank in range(8):
            for file in range(8):
                if self.board[rank][file] != 0 and self.board[rank][file] % 2 == color:
                    psl_moves = self.get_legal_moves(rank, file)
                    psl_moves_with_start_pos = [((rank, file),(psl_move_rank,psl_move_file)) for (psl_move_rank,psl_move_file) in psl_moves]
                    all_legal_moves += (psl_moves_with_start_pos)

        return all_legal_moves

# this method doesn't alter the game state.  It just returns a board given the board in the parameter.
# make sure this doesn't alter the game state.
def get_board_from_move(board:BoardState, r1, f1, r2, f2):
    board_copy = copy.deepcopy(board)
    piece = board_copy.board[r1][f1]
    board_copy.board[r1][f1] = 0
    board_copy.board[r2][f2] = piece
    return board_copy