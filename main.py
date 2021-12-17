# import pygame

from controller import Game
from model import BoardState
from view import run_game
import ai
# from view import run_game

def main():

    # board = BoardState('rn2k1nr/pppppp1p/8/5p1b/2b1q1P1/3P4/PPP1PP1P/RNBQKBNR w')

    # moves = board.get_all_legal_moves('w')
    run_game()

if __name__ == "__main__":
    main()
 