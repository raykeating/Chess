class Pieces:
    # pieces are simply integers.  
    # note: white pieces are odd, black pieces are even.
    empty = 0
    white_king = 1
    black_king = 2
    white_queen = 3
    black_queen = 4
    white_bishop = 5
    black_bishop = 6
    white_knight = 7
    black_knight = 8
    white_rook = 9
    black_rook = 10
    white_pawn = 11
    black_pawn = 12

    # SAN_to_int - SAN is standard algebraic notation, the way pieces are represented in FEN strings.  
    # this method converts the SAN character to the integer representation as used here.
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