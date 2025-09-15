import random
from enum import Enum

from a_star import A_star_pathfind, Cell_Type
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

Config.set("kivy", "exit_on_escape", "0")

type Coord = tuple[int, int]


class Colours(Enum):
    PASS = (1.5, 1.5, 1.5, 1.5)
    WALL = (0.7, 0.7, 0.7, 0.7)
    START = (1, 0, 0, 1)
    END = (0, 1, 0, 1)
    PATH = (1, 0, 1, 1)


class ClickType(Enum):
    LEFT = "left"
    RIGHT = "right"


Window.system_size = (725, 725)
Window.clearcolor = (0.1, 0.1, 0.1, 0.1)


class Pathfind_UI_App(App):
    def __init__(self, **kwargs):
        super(Pathfind_UI_App, self).__init__(**kwargs)

        self.GRID_HEIGHT = 30
        self.GRID_WIDTH = 30
        self.GRID_MARGIN = 200
        self.BLOCK_SIZE = 30
        self.WINDOW_HEIGHT = self.GRID_MARGIN * 2 + self.GRID_HEIGHT * self.BLOCK_SIZE
        self.WINDOW_WIDTH = self.GRID_MARGIN * 2 + self.GRID_WIDTH * self.BLOCK_SIZE

        self.LAYOUT = GridLayout(
            rows=self.GRID_HEIGHT,
            cols=self.GRID_WIDTH,
            row_default_height=self.BLOCK_SIZE,
            col_default_width=self.BLOCK_SIZE,
            row_force_default=True,
            col_force_default=True,
            pos=(self.GRID_MARGIN, -self.GRID_MARGIN),
            orientation="lr-tb",
        )

        self.START_COORDS = None
        self.END_COORDS = None
        self.GRID = []
        self.ALL_RECTS = {}
        self.WALLS = []
        self.AMOUNT_OF_WALLS = 500
        self.PATH = None
        self.FIRST_TIME_GRID_INST = True

    def build(self):
        self.createWalls()
        if self.FIRST_TIME_GRID_INST:
            self.drawGrid(True)
            self.FIRST_TIME_GRID_INST = False
        return self.LAYOUT

    def on_touch_down(self, _, touch):
        coord = None

        for key, button in self.ALL_RECTS.items():

            if (button.pos[0] < touch.pos[0] and \
                touch.pos[0] < button.pos[0] + self.BLOCK_SIZE) \
                and (button.pos[1] < touch.pos[1] and \
                     touch.pos[1] < button.pos[1] + self.BLOCK_SIZE):
    
                coord = key
                break

        if coord and not coord in self.WALLS:
            if touch.button == ClickType.LEFT.value:

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

            elif touch.button == ClickType.RIGHT.value:
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
                    self.PATH = pathfind.path[1:]

                    for coord in self.PATH:
                        self.updateGridCell(coord, Colours.PATH)
                except ValueError as err:
                    self.displayLog(err)
                except Exception as err:
                    self.displayLog(err)

    def displayLog(self, err: str) -> None:
        print(err)

    def createWalls(self) -> None:
        self.WALLS = [
            (
                random.randint(0, self.GRID_WIDTH - 1),
                random.randint(0, self.GRID_HEIGHT - 1),
            )
            for _ in range(self.AMOUNT_OF_WALLS)
        ]

    def resetPath(self) -> None:
        if self.PATH:
            for coord in self.PATH:
                self.updateGridCell(coord, Cell_Type.PASS)
            self.PATH = None

    def updateGridCell(self, coord: Coord, new_value: Enum) -> None:
        if new_value in Cell_Type:
            x, y = coord
            self.GRID[x] = self.GRID[x][:y] + new_value.value + self.GRID[x][y + 1 :]

        self.ALL_RECTS[coord].background_color = Colours[new_value.name].value

    def drawGrid(self, new_string_grid: bool) -> None:
        if new_string_grid:
            self.GRID = [
                (Cell_Type.PASS.value * self.GRID_WIDTH)
                for _ in range(self.GRID_HEIGHT)
            ]

        for w in range(self.GRID_WIDTH):
            for h in range(self.GRID_HEIGHT):
                rect = Button(
                    width=self.BLOCK_SIZE,
                )
                rect.bind(on_touch_down=self.on_touch_down)

                if (h, w) in self.WALLS:
                    rect.background_color = Colours.WALL.value

                    if new_string_grid:
                        self.GRID[h] = (
                            self.GRID[h][:w]
                            + Cell_Type.WALL.value
                            + self.GRID[h][w + 1 :]
                        )
                else:
                    rect.background_color = Colours.PASS.value

                self.LAYOUT.add_widget(rect)
                self.ALL_RECTS[(h, w)] = rect


def main():
    Pathfind_UI_App().run()


if __name__ == "__main__":
    main()
