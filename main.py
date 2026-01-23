import numpy as np
import pygame
from pygame.locals import QUIT

from typing import Callable, Tuple

pygame.init()

FONT = pygame.Font("./assets/font.otf")

BLACK = (20, 20, 20)
WHITE = (255, 255, 255)


class Block:
    EMPTY = 0
    WALL = 1


class Board:
    def __init__(self, width: int, height: int):
        # 2D array
        self.arr = np.zeros((width, height), dtype=np.int64)

    def foreach_block(self, func: Callable[[Tuple[int, int], int], None]):
        for pos, block in np.ndenumerate(self.arr):
            func(pos, int(block))


def render_text(text, color=WHITE):
    return FONT.render(text, True, color)


def main():
    screen = pygame.display.set_mode((640, 480))

    clock = pygame.Clock()
    running = True

    board = Board(16, 16)

    pygame.display.set_icon(pygame.image.load("./assets/icon.png"))
    pygame.display.set_caption("A* Search Pygame")

    def render_blocks(board: Board):
        def render_block(pos: Tuple[int, int], block: int): ...

        board.foreach_block(render_block)

    while running:
        # handle event and update
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # draw
        screen.fill(BLACK)

        render_blocks(board)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        raise error
