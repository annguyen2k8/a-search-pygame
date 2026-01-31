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

Point = Tuple[int, int]


class CellType(Enum):
    EMPTY = 0
    WALL = 1


class Cell:
    x: int
    y: int

    __cell_type: CellType

    def __init__(self, x: int, y: int, cell_type: CellType = CellType.EMPTY):
        self.x = x
        self.y = y

        self.__cell_type = cell_type

    @property
    def pos(self) -> Point:
        return (self.x, self.y)

    @property
    def cell_type(self) -> CellType:
        return self.__cell_type

    def set_type(self, value: CellType):
        self.__cell_type = value


class Board:
    __width: int
    __height: int

    __cells: List[Cell]

    __start_pos: Optional[Point]
    __goal_pos: Optional[Point]

    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height

        self.__cells = []

        self.__start_pos = None
        self.__goal_pos = None

        for x in range(width):
            for y in range(height):
                self.__cells.append(Cell(x, y))

    @property
    def size(self) -> Point:
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

    @property
    def start_pos(self) -> Optional[Point]:
        return self.__start_pos

    @start_pos.setter
    def start_point(self, value: Optional[Point]):
        if value and self.goal_pos == value:
            return

        self.__start_pos = value

    @property
    def goal_pos(self) -> Optional[Point]:
        return self.__goal_pos

    @goal_pos.setter
    def goal_pos(self, value: Optional[Point]):
        if value and self.start_point == value:
            return

        self.__goal_pos = value

    def foreach_cell(self, func: Callable[[Cell, CellType], None]):
        for cell in self.cells:
            func(cell, cell.cell_type)

    def get_cell_at(self, pos: Point) -> Optional[Cell]:
        x, y = pos

        for cell in self.cells:
            if cell.x == x and cell.y == y:
                return cell
        return None

    def set_cell_type_at(self, pos: Point, value: CellType):
        if pos in (self.start_point, self.goal_pos):
            return

        cell = self.get_cell_at(pos)
        if cell is not None:
            cell.set_type(value)


def render_text(text: str, color=WHITE):
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

        self.board = Board(25, 16)

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

            self.screen.fill(BLACK)

            self.draw()

            pygame.display.update()

    def update(self):
        pygame.display.set_caption(f"Tile pos: {self.get_mouse_tile()}")

        mouse_clicked = pygame.mouse.get_pressed()
        mouse_tile = self.get_mouse_tile()

        if mouse_clicked[0] and mouse_tile:
            if not self.board.start_point:
                self.board.start_point = mouse_tile

            elif not self.board.goal_pos:
                self.board.goal_pos = mouse_tile

            else:
                self.board.set_cell_type_at(mouse_tile, CellType.WALL)

        if mouse_clicked[2] and mouse_tile:
            if mouse_tile == self.board.start_point:
                self.board.start_point = None

            elif mouse_tile == self.board.goal_pos:
                self.board.goal_pos = None

            else:
                self.board.set_cell_type_at(mouse_tile, CellType.EMPTY)

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

    def get_mouse_tile(self) -> Optional[Point]:
        mouse_pos = Vector2(pygame.mouse.get_pos())

        if not self.board_rect.collidepoint(mouse_pos):
            return None

        local_pos = mouse_pos - self.board_rect.topleft

        return (
            int(local_pos.x / self.tile_size),
            int(local_pos.y / self.tile_size),
        )

    def rect_tile_at(self, pos: Point) -> Rect:
        x, y = pos

        return Rect(
            self.tile_size * x,
            self.tile_size * y,
            self.tile_size,
            self.tile_size,
        )

    def draw(self):
        self.board_surface.fill(BLACK)

        def draw_cell(cell: Cell, cell_type: CellType):
            width = 1

            if cell_type == CellType.WALL:
                width = 0

            pygame.draw.rect(
                self.board_surface,
                BLUE,
                self.rect_tile_at(cell.pos),
                width,
            )

        if self.board.start_pos:
            pygame.draw.rect(
                self.board_surface, RED, self.rect_tile_at(self.board.start_pos), 5
            )

        if self.board.goal_pos:
            x, y = self.board.goal_pos
            pygame.draw.rect(
                self.board_surface, GREEN, self.rect_tile_at(self.board.goal_pos), 5
            )

        self.board.foreach_cell(draw_cell)

        self.screen.blit(self.board_surface, self.board_rect)


if __name__ == "__main__":
    game = Game()
    try:
        game.mainloop()
    except Exception as error:
        raise error
