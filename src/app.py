import random
import sys
from enum import Enum

import pygame
from a_star import A_star_pathfind, Cell_Type

type Coord = tuple[int, int]


class Colours(Enum):
    PASS = (50, 50, 50)
    WALL = (200, 200, 200)
    START = (222, 49, 99)
    END = (127, 255, 212)
    PATH = (108, 59, 170)


class ClickType(Enum):
    LEFT = 1
    RIGHT = 3


class Pathfind_UI_App:
    def __init__(self):
        self.SCREEN = None
        self.GRID_HEIGHT = 15
        self.GRID_WIDTH = 15
        self.GRID_MARGIN = 100
        self.BLOCK_SIZE = 15
        self.WINDOW_HEIGHT = self.GRID_MARGIN * 2 + self.GRID_HEIGHT * self.BLOCK_SIZE
        self.WINDOW_WIDTH = self.GRID_MARGIN * 2 + self.GRID_WIDTH * self.BLOCK_SIZE

        self.START_COORDS = None
        self.END_COORDS = None
        self.GRID = []
        self.ALL_RECTS = {}
        self.WALLS = []
        self.AMOUNT_OF_WALLS = 100
        self.PATH = None

    def run_app(self):
        pygame.init()
        self.SCREEN = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.SCREEN.fill(Colours.PASS.value)
        pygame.display.set_caption("Fun with Pathfind")

        self.createWalls()
        self.drawGrid(True)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    coord = next(
                        (
                            key
                            for (key, val) in self.ALL_RECTS.items()
                            if val.collidepoint(event.pos)
                        ),
                        None,
                    )

                    if coord and not coord in self.WALLS:
                        if event.button == ClickType.LEFT.value:

                            if not self.START_COORDS and self.END_COORDS != coord:
                                self.START_COORDS = coord
                                self.updateGridCell(self.START_COORDS, Cell_Type.START)

                            elif not self.END_COORDS and self.START_COORDS != coord:
                                self.END_COORDS = coord
                                self.updateGridCell(self.END_COORDS, Cell_Type.END)

                            elif self.END_COORDS and self.START_COORDS != coord:
                                self.updateGridCell(self.END_COORDS, Cell_Type.PASS)
                                self.END_COORDS = coord
                                self.updateGridCell(self.END_COORDS, Cell_Type.END)
                                self.resetPath()

                        elif event.button == ClickType.RIGHT.value:
                            self.updateGridCell(coord, Cell_Type.PASS)

                            if self.END_COORDS == coord:
                                self.END_COORDS = None
                                self.resetPath()

                            elif self.START_COORDS == coord:
                                self.START_COORDS = None
                                self.resetPath()

                        if self.START_COORDS and self.END_COORDS:
                            self.updateGridCell(self.START_COORDS, Cell_Type.START)
                            self.updateGridCell(self.END_COORDS, Cell_Type.END)

                            try:
                                pathfind = A_star_pathfind(tuple(self.GRID))
                            except ValueError as err:
                                self.displayLog(err)
                                continue
                            except Exception as err:
                                self.displayLog(err)
                                continue

                            self.PATH = pathfind.path[1:]

                            for coord in self.PATH:
                                self.updateGridCell(coord, Colours.PATH)

            pygame.display.update()

    
    def displayLog(self, err: str) -> None:
        print(err)
    
    def createWalls(self) -> None:
        self.WALLS = [
            (
                random.randint(0, self.BLOCK_SIZE - 1),
                random.randint(0, self.BLOCK_SIZE - 1),
            )
            for _ in range(self.AMOUNT_OF_WALLS)
        ]

    def resetPath(self) -> None:
        if self.PATH:
            for coord in self.PATH:
                self.updateGridCell(coord, Cell_Type.PASS)
            self.PATH = None

        self.drawGrid(False)

    def updateGridCell(self, coord: Coord, new_value: Enum) -> None:
        if new_value in Cell_Type:
            x, y = coord
            self.GRID[x] = self.GRID[x][:y] + new_value.value + self.GRID[x][y + 1 :]
        pygame.draw.rect(
            self.SCREEN, Colours[new_value.name].value, self.ALL_RECTS[coord], 0
        )

        self.drawGrid(False)

    def drawGrid(self, new_string_grid: bool) -> None:
        if new_string_grid:
            self.GRID = [
                (Cell_Type.PASS.value * self.GRID_WIDTH)
                for _ in range(self.GRID_HEIGHT)
            ]

        for w in range(self.GRID_WIDTH):
            for h in range(self.GRID_HEIGHT):

                x = self.GRID_MARGIN + h * self.GRID_HEIGHT
                y = self.GRID_MARGIN + w * self.GRID_WIDTH
                rect = pygame.Rect(y, x, self.BLOCK_SIZE, self.BLOCK_SIZE)
                self.ALL_RECTS[(h, w)] = rect

                if (h, w) in self.WALLS:
                    pygame.draw.rect(self.SCREEN, Colours.WALL.value, rect, 0)
                    if new_string_grid:
                        self.GRID[h] = (
                            self.GRID[h][:w]
                            + Cell_Type.WALL.value
                            + self.GRID[h][w + 1 :]
                        )
                else:
                    pygame.draw.rect(self.SCREEN, Colours.WALL.value, rect, 1)


def main():
    ui = Pathfind_UI_App()
    ui.run_app()


if __name__ == "__main__":
    main()
