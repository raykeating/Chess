import pygame as pg
from game_logic import Game, BoardState

# General Setup
screen = pg.display.set_mode((800,800))
pg.init()
pg.display.set_caption('Chess')
clock = pg.time.Clock()

def load_images():
    piece_imgs = []
    for i in range(12):
        img = pg.image.load(f'Pieces/{(i+1)}.png').convert_alpha()
        img = pg.transform.smoothscale(img, (100,100))
        piece_imgs.append(img)
    return piece_imgs

piece_imgs = load_images()

def draw_board():
    squares = []
    dark_color = "#EDEDD2"
    light_color = "#769459"
    
    black_square = pg.Surface((100,100))
    black_square.fill(pg.Color(dark_color))
    white_square = pg.Surface((100,100))
    white_square.fill(pg.Color(light_color))

    for i in range(8):
        flip = 1
        if i % 2 == 0:
            flip = 0
        for j in range(8):
            # draw the background
            if j % 2 == flip:
                screen.blit(black_square,(j*100,i*100))
                squares.append([black_square, black_square.get_rect(x=j*100, y=i*100)])
            else:
                screen.blit(white_square,(j*100,i*100))
                squares.append([white_square, white_square.get_rect(x=j*100, y=i*100)])
    
    return squares


def draw_pieces(board:BoardState):
    active_pieces = []
    for i in range(8):
        for j in range(8):
            # get the integer value of the piece
            piece = board.board[i][j]
            # draw the piece if it's not empty (0)
            if piece > 0 and piece < 13:
                piece_img = piece_imgs[piece-1] 
                piece_rect = piece_img.get_rect(x=j*100, y=i*100)
                active_pieces.append([piece, piece_img, piece_rect])
                screen.blit(piece_img, piece_rect)  
    # active_pieces is a list of the pieces on the board.
    # Each item in the list contains the pieces int value at [0], the image (surface) at [1], and it's rect at [2] 
    return active_pieces

def run_game():
    game = Game()

    squares = draw_board()
    pieces = draw_pieces(game.board)

    hover_piece = None
    clicked_piece = None
    click_pos = None
    dragging = False

    # main event loop
    while True:
        for event in pg.event.get():
            # enable close button
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                print('mousedown')
                # get the click position
                click_pos = event.pos
                # get any pieces that are at the click position
                clicked_pieces = [p for p in pieces if p[2].collidepoint(click_pos)]
                if len(clicked_pieces) > 0:
                    clicked_piece = clicked_pieces[0]
                    dragging = True
                else:
                    continue

                # if the player clicked their own color's piece, move it.  Otherwise, print error
                if clicked_piece[0] % 2 == game.next_move:
                    print('clicked piece: ', clicked_piece)
                else:
                    print('that is not your piece')
                    clicked_piece = None                 

            # when a player releases the mouse to move a piece
            elif event.type == pg.MOUSEBUTTONUP:
                print('mouseup')
                # if a piece has been clicked beforehand
                print(clicked_piece)
                if clicked_piece:
                    # get the position where the mouse was released
                    release_pos = event.pos
                    # check if there are any pieces where the mouse was released
                    captured_pieces = [p for p in pieces if p[2].collidepoint(release_pos)]
                    if len(captured_pieces) > 0: 
                        captured_piece = captured_pieces[0]
                        if captured_piece[0] % 2 != game.next_move: # if so, check if it is the opponent's piece (modulo because black is even, white is odd)
                            print("a piece was captured!")
                            game.move_piece(click_pos[0],click_pos[1],release_pos[0], release_pos[1], clicked_piece[0]) # move the piece
                            pieces = draw_pieces(game.board) 
                            game.next_move = 1 if game.next_move == 0 else 0 # change to next move
                        else:
                            clicked_piece = None
                            hover_piece = None
                            dragging = False
                            draw_board()
                            draw_pieces(game.board)
                            continue # if the piece has been released on a piece of their own color, don't do anything.
                    else:
                        # if there are no pieces where the mouse was released, just move it to that square.
                        game.move_piece(click_pos[0],click_pos[1],release_pos[0], release_pos[1], clicked_piece[0])
                        pieces = draw_pieces(game.board) 
                        game.next_move = 1 if game.next_move == 0 else 0 # change to next move
                clicked_piece = None
                hover_piece = None
                dragging = False
                draw_board()
                pieces = draw_pieces(game.board)

            elif event.type == pg.MOUSEMOTION:
                if clicked_piece and dragging:
                    hover_piece = clicked_piece[2].copy()
                    mouse_x, mouse_y = event.pos
                    hover_piece.center = (mouse_x, mouse_y)
                    draw_board()
                    draw_pieces(game.board)
                    [screen.blit(s[0],s[1]) for s in squares if pg.Rect.colliderect(s[1], clicked_piece[2])]
                    screen.blit(clicked_piece[1], hover_piece)
                                
        # update display 144 times/sec
        pg.display.update()
        clock.tick(144)