from enum import Enum
from typing import Callable, Optional

import pygame
from pygame import Clock, Rect, Surface, Vector2
from pygame.locals import K_SPACE, QUIT, VIDEORESIZE
from pygame.typing import IntPoint

from constants import Colors
from core import Board, Cell, CellType, Scheduler
from render import Render


DebugCallable = Callable[["Game"], str]


class GameState(Enum):
    EDITING = 0
    SEARCHING = 1
    FINISHED = 2


class Game:

    screen: Surface
    clock: Clock
    running: bool

    scheduler: Scheduler

    board_padding: int = 8

    board_surface: Surface
    board_rect: Rect
    board: Board

    cell_size: float

    state: GameState

    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

        self.clock = Clock()
        self.running = True

        self.scheduler = Scheduler(self.clock)

        self.board = Board(25, 16)

        pygame.display.set_icon(pygame.image.load("./assets/icon.png"))
        pygame.display.set_caption("A* Search Pygame")

        self.update_render()

        self.state = GameState.EDITING

    @property
    def screen_rect(self) -> Rect:
        return self.screen.get_rect()

    def mainloop(self):
        while self.running:
            self.clock.tick(0)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                if event.type == VIDEORESIZE:
                    self.update_render()

            self.update()

            self.screen.fill(Colors.BLACK)

            self.draw()

            pygame.display.update()

    def update(self):
        self.scheduler.update()

        if self.state == GameState.EDITING:
            self.update_editing()

        if self.state == GameState.SEARCHING:
            self.update_searching()

        if self.state == GameState.FINISHED:
            ...

    def update_searching(self): ...

    def update_editing(self):
        keys = pygame.key.get_just_pressed()
        mouse_clicked = pygame.mouse.get_pressed()
        mouse_tile = self.get_mouse_tile()

        if keys[K_SPACE]:
            if self.board.start_point and self.board.goal_pos:
                self.state = GameState.SEARCHING

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

    def get_mouse_tile(self) -> Optional[IntPoint]:
        mouse_pos = Vector2(pygame.mouse.get_pos())

        if not self.board_rect.collidepoint(mouse_pos):
            return None

        local_pos = mouse_pos - self.board_rect.topleft

        return (
            int(local_pos.x / self.tile_size),
            int(local_pos.y / self.tile_size),
        )

    def rect_tile_at(self, pos: IntPoint) -> Rect:
        x, y = pos

        return Rect(
            self.tile_size * x,
            self.tile_size * y,
            self.tile_size,
            self.tile_size,
        )

    def draw(self):
        self.board_surface.fill(Colors.BLACK)

        def draw_cell(cell: Cell, cell_type: CellType):
            width = 1

            if cell_type == CellType.WALL:
                width = 0

            pygame.draw.rect(
                self.board_surface,
                Colors.BLUE,
                self.rect_tile_at(cell.pos),
                width,
            )

        if self.board.start_pos:
            pygame.draw.rect(
                self.board_surface,
                Colors.RED,
                self.rect_tile_at(self.board.start_pos),
                5,
            )

        if self.board.goal_pos:
            pygame.draw.rect(
                self.board_surface,
                Colors.GREEN,
                self.rect_tile_at(self.board.goal_pos),
                5,
            )

        self.board.foreach_cell(draw_cell)
        self.screen.blit(self.board_surface, self.board_rect)

        mouse_pos = Vector2(pygame.mouse.get_pos())

        Render.text(
            self.screen,
            Colors.WHITE,
            f"{self.state.name.upper()}",
            (mouse_pos.x + 16, mouse_pos.y + 16),
        )
