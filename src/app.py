import random
from enum import Enum

from a_star import A_star_pathfind, Cell_Type
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

Config.set("kivy", "exit_on_escape", "0")
Config.set("graphics", "resizable", False)
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '500')

type Coord = tuple[int, int]


class Colours(Enum):
    PASS = (1.5, 1.5, 1.5, 1.5)
    WALL = (0.7, 0.7, 0.7, 0.7)
    START = (2, 0, 0, 2)
    END = (0, 2, 0, 2)
    PATH = (2, 0, 2, 2)


class ClickType(Enum):
    LEFT = "left"
    RIGHT = "right"

HEIGHT = 550
WIDTH = 910

Window.minimum_width = WIDTH
Window.minimum_height = HEIGHT
Window.system_size = (WIDTH, HEIGHT)
Window.clearcolor = (0.1, 0.1, 0.1, 0.1)


class PathfindApp(App):
    def __init__(self, **kwargs):
        super(PathfindApp, self).__init__(**kwargs)

        self.GRID_HEIGHT = 30
        self.GRID_WIDTH = 30
        self.GRID_MARGIN = 100
        self.CELL_SIZE = 30

        self.GRID_LAYOUT = None
        self.GENERATION_LONG = None

        self.START_COORDS = None
        self.END_COORDS = None
        self.GRID = []
        self.ALL_RECTS = {}
        self.WALLS = []
        self.AMOUNT_OF_WALLS = 400
        self.PATH = None
        self.FIRST_TIME_GRID_INST = True

    def build(self):
        self.createWalls()

        return self.createBox()

    def createBox(self):

        def callback(_):
            global WIDTH, HEIGHT

            self.GRID_WIDTH = int(grid_width.text)
            self.GRID_HEIGHT = int(grid_height.text)
            self.CELL_SIZE = int(grid_cell_size.text)
            self.AMOUNT_OF_WALLS = int(grid_wall_amount.text)
            
            self.FIRST_TIME_GRID_INST = True
            self.START_COORDS = None
            self.END_COORDS = None
            self.GRID = []
            self.ALL_RECTS = {}
            self.WALLS = []

            while len(self.GRID_LAYOUT.children) > 0:
                for child in self.GRID_LAYOUT.children:
                    self.GRID_LAYOUT.remove_widget(child)

            self.GRID_LAYOUT.rows = self.GRID_HEIGHT
            self.GRID_LAYOUT.cols = self.GRID_WIDTH
            self.GRID_LAYOUT.row_default_height=self.CELL_SIZE
            self.GRID_LAYOUT.col_default_width=self.CELL_SIZE

            # HEIGHT = self.GRID_MARGIN * 2 + self.GRID_HEIGHT * self.CELL_SIZE
            # WIDTH = self.GRID_MARGIN * 2 + self.GRID_WIDTH * self.CELL_SIZE
            # Window.system_size = (WIDTH, HEIGHT)

            self.createWalls()
            self.drawGrid(True)

        root_box = BoxLayout(
            orientation="horizontal",
            pos=(self.GRID_MARGIN, -self.GRID_MARGIN),
            size_hint_x=None,
            width=2000,
        )
        input_half = GridLayout(
            rows=3,
            cols=1,
            spacing=20,
            orientation="tb-lr",
        )
        top_input_box = GridLayout(
            rows=4,
            cols=2,
            spacing=20,
            size_hint=(None, None),
            height=250,
            orientation="tb-lr",
        )

        self.GRID_LAYOUT = GridLayout(
            rows=self.GRID_HEIGHT,
            cols=self.GRID_WIDTH,
            row_default_height=self.CELL_SIZE,
            col_default_width=self.CELL_SIZE,
            row_force_default=True,
            col_force_default=True,
        )

        if self.FIRST_TIME_GRID_INST:
            self.drawGrid(True)
            self.FIRST_TIME_GRID_INST = False

        grid_width = TextInput(
            text="30",
            multiline=False,
            size_hint=(None, None),
            height=65,
            width=300,
            padding=15,
            font_name="GillSans",
        )
        grid_height = TextInput(
            text="30",
            multiline=False,
            size_hint=(None, None),
            height=65,
            width=300,
            padding=15,
            font_name="GillSans",
        )
        grid_cell_size = TextInput(
            text="30",
            multiline=False,
            size_hint=(None, None),
            height=65,
            width=300,
            padding=15,
            font_name="GillSans",
        )
        grid_wall_amount = TextInput(
            text="400",
            multiline=False,
            size_hint=(None, None),
            height=65,
            width=300,
            padding=15,
            font_name="GillSans",
        )
        generate_grid_button = Button(
            text="Generate grid",
            size_hint=(None, None),
            height=70,
            width=620,
            font_name="GillSans",
        )
        generate_grid_button.bind(on_press=callback)
        self.GENERATION_LONG = TextInput(
            text="Results will appear here",
            multiline=True,
            readonly=True,
            size_hint=(None, None),
            height=540,
            width=620,
            background_color=(0.3, 0.3, 0.3, 0.3),
            foreground_color=(0.7, 0.7, 0.7, 0.7),
            padding=30,
            font_name="GillSans",
        )

        top_input_box.add_widget(
            Label(
                text="Width:",
                size_hint=(None, None),
                height=20,
                width=90,
                font_name="GillSans",
            )
        )
        top_input_box.add_widget(grid_width)
        top_input_box.add_widget(
            Label(
                text="Height:",
                size_hint=(None, None),
                height=20,
                width=90,
                font_name="GillSans",
            )
        )
        top_input_box.add_widget(grid_height)
        top_input_box.add_widget(
            Label(
                text="Cell size:",
                size_hint=(None, None),
                height=20,
                width=110,
                font_name="GillSans",
            )
        )
        top_input_box.add_widget(grid_cell_size)
        top_input_box.add_widget(
            Label(
                text="Obstacles:",
                size_hint=(None, None),
                height=20,
                width=130,
                font_name="GillSans",
            )
        )
        top_input_box.add_widget(grid_wall_amount)

        input_half.add_widget(top_input_box)
        input_half.add_widget(generate_grid_button)
        input_half.add_widget(self.GENERATION_LONG)

        root_box.add_widget(self.GRID_LAYOUT)
        root_box.add_widget(input_half)


        return root_box

    def on_touch_down(self, _, touch):
        coord = None

        for key, button in self.ALL_RECTS.items():

            if (
                button.pos[0] < touch.pos[0]
                and touch.pos[0] < button.pos[0] + self.CELL_SIZE
            ) and (
                button.pos[1] < touch.pos[1]
                and touch.pos[1] < button.pos[1] + self.CELL_SIZE
            ):

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
        self.GENERATION_LONG.text = err

    def createWalls(self) -> None:
        walls_left = self.AMOUNT_OF_WALLS

        while walls_left > 0:
            coord = (
                random.randint(0, self.GRID_HEIGHT - 1),
                random.randint(0, self.GRID_WIDTH - 1),
            )

            if not coord in self.WALLS:
                self.WALLS.append(coord)
                walls_left -= 1

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
                    width=self.CELL_SIZE,
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

                self.GRID_LAYOUT.add_widget(rect)
                self.ALL_RECTS[(h, w)] = rect


def main():
    PathfindApp().run()


if __name__ == "__main__":
    main()
