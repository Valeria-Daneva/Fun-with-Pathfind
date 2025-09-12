import math
from enum import Enum
from queue import PriorityQueue
from typing import Optional

# commonly used values
type Coord = tuple[int, int]
type Grid = tuple[str]


class Cell_Type(Enum):
    START = "S"
    END = "F"
    WALL = "█"
    PASS = "◦"


class Path(Enum):
    S = "↓"
    N = "↑"
    W = "←"
    E = "→"
    SW = "↙"
    SE = "↘"
    NW = "↖"
    NE = "↗"


class A_star_pathfind:
    def __init__(self, grid: Grid) -> None:
        self.__origin_cell: dict[Coord, Optional[Coord]] = {}
        self.__grid: Grid = grid
        self.__start: Coord = None
        self.__end: Coord = None
        self.path: list = []
        self.path_length: int = 0

        try:
            self.set_and_validate_inputs()
            self.pathfind()
        except ValueError as err:
            raise ValueError(err)
        except Exception as err:
            raise Exception(err)

        self.get_path()

    """
        Pathfinding function based on A star algorithm
    """

    def pathfind(self) -> None:
        # add priority queue optimisation to ensure
        # most probable path is always the first one processed
        heap_opt = PriorityQueue()
        heap_opt.put((0, self.__start))

        # dictionary of cell origins and cost of cells being traversed
        current_cost: dict[Coord, int] = {}
        self.__origin_cell[self.__start] = None

        current_cost[self.__start] = 0
        valid_path = False

        while not heap_opt.empty():
            # get foremost priority cell
            current_cell = heap_opt.get()[1]

            # stop the loop if a path has been found
            if current_cell == self.__end:
                valid_path = True
                break

            # get all valid neighbours for processing
            neighbours = self.get_valid_neighbours(current_cell)

            for neighbour_cell in neighbours:
                # get cell's G cost - distance from the start
                new_cost = current_cost[current_cell] + neighbours[neighbour_cell]

                # set the G cost and origin of a cell if it's newly processed
                # or update them both if the G cost is less than the one recorded
                if (
                    neighbour_cell not in current_cost
                    or new_cost < current_cost[neighbour_cell]
                ):
                    current_cost[neighbour_cell] = new_cost
                    # priority is determined by F cost = G cost + H cost
                    priority = new_cost + self.heuristic(neighbour_cell)
                    heap_opt.put((priority, neighbour_cell))
                    self.__origin_cell[neighbour_cell] = current_cell

        if not valid_path:
            raise Exception("There is no valid path.")

    """
        Function for calculating the steps taken for the shortest path
    """

    def get_path(self) -> None:
        cell_to_check = self.__origin_cell[self.__end]

        while cell_to_check:
            self.path.insert(0, cell_to_check)
            self.path_length += 1
            cell_to_check = self.__origin_cell[cell_to_check]

    """
        Function for printing out the grid with the route for the shortest path
    """

    def print_path(self) -> str:
        prev_cell = self.__end
        grid = list(self.__grid)

        for cell in self.path[::-1]:
            x, y = cell
            grid[x] = list(grid[x])

            all_n = self.get_all_neighbours(cell)
            matching_dir = next(
                direction for direction, coords in all_n.items() if coords == prev_cell
            )
            grid[x][y] = Path[matching_dir].value

            prev_cell = cell

        return "\n".join("".join(row) for row in grid)

    """
        Function for retrieving all possible neighbours
    """

    def get_all_neighbours(self, cell: Coord) -> dict[str, Coord]:
        x, y = cell

        east = y + 1
        north = x - 1
        west = y - 1
        south = x + 1

        neighbours = {
            "E": (x, east),
            "N": (north, y),
            "W": (x, west),
            "S": (south, y),
            "NE": (north, east),
            "NW": (north, west),
            "SE": (south, east),
            "SW": (south, west),
        }

        return neighbours

    """
        Function for retrieving all valid neighbours of a cell
    """

    def get_valid_neighbours(self, cell: Coord) -> dict[Coord, int]:
        # the current and max possible values of x and y
        max_x, max_y = len(self.__grid) - 1, len(self.__grid[0]) - 1
        # get coords of all possible neighbours
        all_n = self.get_all_neighbours(cell)
        neighbours = {
            cell: (10 if len(direction) == 1 else 14)
            for (direction, cell) in all_n.items()
        }
        neighbours_copy = neighbours.copy()

        # filter out walls and out-of-bounds indeces
        for cell in neighbours_copy:
            current_x, current_y = cell

            if (
                current_x > max_x
                or current_x < 0
                or current_y > max_y
                or current_y < 0
                or self.__grid[current_x][current_y] == Cell_Type.WALL.value
            ):
                del neighbours[cell]

        return neighbours

    """
        Heuristic function for determining a cell's H cost:
        the approximate distance from the end; uses Euclidean calculation
    """

    def heuristic(self, cell: Coord) -> int:
        x1, y1 = cell
        x2, y2 = self.__end

        return math.sqrt(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2)

    """
        Function for validating the grid, start coordinate and end coordinate values
    """

    def set_and_validate_inputs(self) -> None:
        start_count, end_count, row_len, valid_cells = (
            0,
            0,
            len(self.__grid[0]),
            tuple(e.value for e in Cell_Type),
        )

        for x, row in enumerate(self.__grid):
            if row_len != len(row):
                raise ValueError("Grid row lengths do not match.")

            for y, cell in enumerate(row):
                if cell == Cell_Type.START.value:
                    start_count += 1
                    self.__start = (x, y)
                if cell == Cell_Type.END.value:
                    end_count += 1
                    self.__end = (x, y)
                if not cell in valid_cells:
                    raise ValueError(
                        "Grid has invalid cell. "
                        + "Only cell values (◦ | █ | S | F) allowed."
                    )

        if start_count != 1:
            raise ValueError("Grid must have one and only one start.")

        if end_count != 1:
            raise ValueError("Grid must have one and only one end.")
