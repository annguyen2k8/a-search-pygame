from enum import Enum

from pygame.typing import IntPoint


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
    def pos(self) -> IntPoint:
        return (self.x, self.y)

    @property
    def cell_type(self) -> CellType:
        return self.__cell_type

    def set_type(self, value: CellType):
        self.__cell_type = value
