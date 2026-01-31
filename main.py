from enum import Enum
from typing import Callable, List, Optional, Tuple

import pygame
from pygame import Clock, Rect, Surface, Vector2
from pygame.locals import QUIT, VIDEORESIZE

pygame.init()

FONT = pygame.Font("./assets/font.otf")

BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class CellType(Enum):
    EMPTY = 0
    WALL = 1


class Cell:
    x: int
    y: int
    cell_type: CellType

    def __init__(self, x: int, y: int, cell_type: CellType = CellType.EMPTY):
        super().__init__()

        self.x = x
        self.y = y
        self.cell_type = cell_type


class Board:
    __width: int
    __height: int

    __cells: List[Cell] = []

    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height

        for x in range(width):
            for y in range(height):
                self.__cells.append(Cell(x, y))

    @property
    def size(self) -> Tuple[int, int]:
        return (self.width, self.height)

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def cells(self) -> List[Cell]:
        return self.__cells

    def foreach_cell(self, func: Callable[[Cell], None]):
        for cell in self.cells:
            func(cell)

    def is_inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        for cell in self.cells:
            if cell.x == x and cell.y == y:
                return cell
        return None


def render_text(text, color=WHITE):
    return FONT.render(text, True, color)


class Game:
    board_padding: int = 8

    screen: Surface
    clock: Clock
    running: bool

    board_surface: Surface
    board_rect: Rect
    board: Board

    cell_size: float

    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

        self.clock = Clock()
        self.running = True

        self.board = Board(16, 10)

        pygame.display.set_icon(pygame.image.load("./assets/icon.png"))
        pygame.display.set_caption("A* Search Pygame")

        self.update_render()

    @property
    def screen_rect(self) -> Rect:
        return self.screen.get_rect()

    def mainloop(self):
        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                if event.type == VIDEORESIZE:
                    self.update_render()

            self.update()

            self.draw()

            pygame.display.update()

    def update(self):
        pygame.display.set_caption(f"Tile pos: {self.get_mouse_tile()}")
        pass

    def update_render(self):
        viewport = self.screen_rect
        padding = self.board_padding

        usable_width = viewport.width - padding * 2
        usable_height = viewport.height - padding * 2

        self.tile_size = min(
            usable_width / self.board.width,
            usable_height / self.board.height,
        )

        board_width = self.tile_size * self.board.width
        board_height = self.tile_size * self.board.height

        self.board_rect = Rect(
            padding + (usable_width - board_width) / 2,
            padding + (usable_height - board_height) / 2,
            board_width,
            board_height,
        )

        self.board_surface = Surface((self.board_rect.width, self.board_rect.height))

    def get_mouse_tile(self) -> Optional[Tuple[int, int]]:
        mouse_pos = Vector2(pygame.mouse.get_pos())

        if not self.board_rect.collidepoint(mouse_pos):
            return None

        local_pos = mouse_pos - self.board_rect.topleft

        return (
            int(local_pos.x / self.tile_size),
            int(local_pos.y / self.tile_size),
        )

    def rect_tile_at(self, x: int, y: int) -> Rect:
        return Rect(
            self.tile_size * x,
            self.tile_size * y,
            self.tile_size,
            self.tile_size,
        )

    def draw(self):
        self.screen.fill(BLACK)

        def draw_cell(cell: Cell):
            pygame.draw.rect(
                self.board_surface,
                BLUE,
                self.rect_tile_at(cell.x, cell.y),
                1,
            )

        self.board.foreach_cell(draw_cell)

        self.screen.blit(self.board_surface, self.board_rect)


if __name__ == "__main__":
    game = Game()
    try:
        game.mainloop()
    except Exception as error:
        raise error
