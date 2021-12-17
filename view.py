import pygame as pg
from controller import Game, BoardState
from ai import evaluate

# General Setup
screen = pg.display.set_mode((800,800))
pg.init()
pg.font.init()
default_font = pg.font.get_default_font()
large_font = pg.font.Font(default_font, 40)
small_font = pg.font.Font(default_font, 20)
pg.display.set_caption('Chess')
clock = pg.time.Clock()

def load_images():

    piece_imgs = []
    for i in range(12):
        img = pg.image.load(f'Pieces/{(i+1)}.png').convert_alpha()
        img = pg.transform.smoothscale(img, (100,100))
        piece_imgs.append(img)
    return piece_imgs

# loads pieces
piece_imgs = load_images()

circle_img = pg.image.load("circle.png").convert_alpha()
circle_img = pg.transform.smoothscale(circle_img, (10,10))


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

def highlight(legal_moves:list, board:BoardState):
    highlight_square = pg.Surface((100,100))
    highlight_square.fill(pg.Color(255,255,0))
    highlight_square.set_alpha(80)

    try:
        for move in legal_moves:
            rank = move[1]*100
            file = move[0]*100
            screen.blit(circle_img, circle_img.get_rect(x=rank+45,y=file+45)) if board[move[0]][move[1]] == 0 else screen.blit(highlight_square, (rank, file))
    except TypeError:
        pass

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

def display_gameover_message(player):
    message_surf = pg.Surface((350,160))
    message_surf.fill(pg.Color(255,0,0))
    message_surf.set_alpha(100)
    message_rect = message_surf.get_rect(x=225,y=320)
    screen.blit(message_surf, message_rect)
    text_surface_top = large_font.render('GAME OVER!', True, (0,0,0))
    text_surface_bottom = small_font.render(f'{player} is in Checkmate', True, (0,0,0))
    screen.blit(text_surface_top, (275,360))
    screen.blit(text_surface_bottom, (290,410))

def run_game():
    game = Game()

    squares = draw_board()
    pieces = draw_pieces(game.board)

    hover_piece = None
    clicked_piece = None
    legal_moves = None
    click_pos = None
    dragging = False

    # main event loop
    while True:
        if game.current_move == 0: # if it's black's turn
                game.move_piece_with_ai(depth=3)
                draw_board()
                pieces = draw_pieces(game.board)

        for event in pg.event.get():
            # enable close button
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            elif event.type == pg.MOUSEBUTTONDOWN:

                # --- DRAG AND DROP LOGIC ---

                # get the click position
                click_pos = event.pos
                # get any pieces that are at the click position
                clicked_pieces = [p for p in pieces if p[2].collidepoint(click_pos)]
                if len(clicked_pieces) > 0:
                    clicked_piece = clicked_pieces[0]
                    dragging = True
                    # --- HIGHLIGHT LEGAL MOVES ---
                    if clicked_piece[0] % 2 == game.current_move: 
                        legal_moves = game.get_legal_moves(clicked_piece[2])
                        highlight(legal_moves, game.board.board)
                else:
                    continue

                # if the player clicked their own color's piece, move it.  Otherwise, set clicked_piece to None
                if clicked_piece[0] % 2 == game.current_move:
                    pass
                else:
                    clicked_piece = None         

            # when a player releases the mouse to move a piece
            elif event.type == pg.MOUSEBUTTONUP and clicked_piece:
                # --- DRAG AND DROP LOGIC ---
                # if a piece has been clicked beforehand
                if clicked_piece:
                    # get the position where the mouse was released
                    release_pos = event.pos
                    # check if there are any pieces where the mouse was released
                    captured_pieces = [p for p in pieces if p[2].collidepoint(release_pos)]
                    if len(captured_pieces) > 0: 
                        captured_piece = captured_pieces[0]
                        if captured_piece[0] % 2 != game.current_move: # if so, check if it is the opponent's piece (modulo because black is even, white is odd)
                            game.move_piece(click_pos[1],click_pos[0],release_pos[1], release_pos[0]) # move the piece
                            pieces = draw_pieces(game.board) 
                        else:
                            clicked_piece = None
                            hover_piece = None
                            dragging = False
                            draw_board()
                            draw_pieces(game.board)
                            continue # if the piece has been released on a piece of their own color, don't do anything.
                    else:
                        # if there are no pieces where the mouse was released, just move it to that square.
                        game.move_piece(click_pos[1],click_pos[0],release_pos[1], release_pos[0])
                        pieces = draw_pieces(game.board) 
                clicked_piece = None
                legal_moves = None
                hover_piece = None
                dragging = False
                draw_board()
                pieces = draw_pieces(game.board)
                game.check_for_checkmate()
                if game.board.black_checkmated:
                    display_gameover_message("Black")
                elif game.board.white_checkmated:
                    display_gameover_message("White")

            elif event.type == pg.MOUSEMOTION:
                # --- DRAG AND DROP LOGIC ---
                if clicked_piece and dragging:
                    hover_piece = clicked_piece[2].copy()
                    mouse_x, mouse_y = event.pos
                    hover_piece.center = (mouse_x, mouse_y)
                    draw_board()
                    draw_pieces(game.board)
                    highlight(legal_moves, game.board.board)
                    [screen.blit(s[0],s[1]) for s in squares if pg.Rect.colliderect(s[1], clicked_piece[2])]
                    screen.blit(clicked_piece[1], hover_piece)
                                
        # update display 144 times/sec
        pg.display.update()
        clock.tick(144)