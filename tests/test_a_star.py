import textwrap

import pytest
from src.a_star import A_star_pathfind


class Test_A_Star:
    """Standard case tests checking for whether the correct result is returned"""

    def test_standard_case_one_5x5(self):
        grid = (
            "◦S◦◦◦",
            "◦███◦",
            "◦◦◦◦◦",
            "◦◦F◦◦",
            "◦◦◦◦◦"
        )

        sol = A_star_pathfind(grid)
        expected_path = textwrap.dedent(
            """\
                                        ◦↙◦◦◦
                                        ↘███◦
                                        ◦↘◦◦◦
                                        ◦◦F◦◦
                                        ◦◦◦◦◦"""
        )

        assert sol.path_length == 3
        assert expected_path == sol.print_path()

    def test_standard_case_two_5x7(self):
        grid = (
            "◦◦◦◦S◦◦",
            "◦██◦███",
            "███◦◦◦◦",
            "◦◦◦◦███",
            "◦F◦█◦◦█"
        )

        sol = A_star_pathfind(grid)
        expected_path = textwrap.dedent(
            """\
                                        ◦◦◦◦↙◦◦
                                        ◦██↓███
                                        ███↙◦◦◦
                                        ◦◦↙◦███
                                        ◦F◦█◦◦█"""
        )

        assert sol.path_length == 4
        assert expected_path == sol.print_path()

    def test_standard_case_three_7x7(self):
        grid = (
            "S◦◦◦◦◦◦",
            "◦██◦███",
            "███◦◦◦◦",
            "◦◦█◦███",
            "◦◦◦◦◦██",
            "◦◦█████",
            "◦◦◦F███",
        )

        sol = A_star_pathfind(grid)
        expected_path = textwrap.dedent(
            """\
                                        →→↘◦◦◦◦
                                        ◦██↓███
                                        ███↓◦◦◦
                                        ◦◦█↙███
                                        ◦◦↙◦◦██
                                        ◦↘█████
                                        ◦◦→F███"""
        )

        assert sol.path_length == 9
        assert expected_path == sol.print_path()

    def test_standard_case_four_10x7(self):
        grid = (
            "◦◦◦◦◦S◦",
            "◦██◦███",
            "███◦◦◦◦",
            "◦◦◦◦███",
            "◦█◦◦◦◦█",
            "◦████◦█",
            "◦█◦██◦█",
            "◦██◦◦◦█",
            "◦◦█◦◦██",
            "◦F◦◦◦██",
        )

        sol = A_star_pathfind(grid)
        expected_path = textwrap.dedent(
            """\
                                        ◦◦◦◦↙←◦
                                        ◦██↓███
                                        ███↙◦◦◦
                                        ◦↙←◦███
                                        ↓█◦◦◦◦█
                                        ↓████◦█
                                        ↓█◦██◦█
                                        ↓██◦◦◦█
                                        ↘◦█◦◦██
                                        ◦F◦◦◦██"""
        )

        assert sol.path_length == 11
        print(sol.print_path)
        assert expected_path == sol.print_path()

    def test_standard_case_five_10x7(self):
        grid = (
            "◦◦S◦◦◦◦",
            "◦███◦██",
            "███◦◦◦◦",
            "◦◦◦◦███",
            "◦█◦◦◦◦█",
            "██◦██◦█",
            "██◦██◦█",
            "◦█◦F◦◦█",
            "◦◦█◦◦██",
            "◦◦◦◦◦██",
        )

        sol = A_star_pathfind(grid)
        expected_path = textwrap.dedent(
            """\
                                        ◦◦→↘◦◦◦
                                        ◦███↓██
                                        ███◦↙◦◦
                                        ◦◦◦↓███
                                        ◦█◦↙◦◦█
                                        ██↓██◦█
                                        ██↘██◦█
                                        ◦█◦F◦◦█
                                        ◦◦█◦◦██
                                        ◦◦◦◦◦██"""
        )

        assert sol.path_length == 8
        assert expected_path == sol.print_path()

    def test_standard_case_six_10x10(self):
        grid = (
            "◦◦██◦◦◦◦S◦",
            "◦███◦██◦◦█",
            "███◦◦◦◦◦██",
            "◦◦◦◦██◦◦◦◦",
            "◦█◦◦◦◦◦◦█◦",
            "██◦██◦█◦██",
            "██◦██◦█◦██",
            "◦█◦F◦◦█◦██",
            "◦◦◦◦◦◦◦◦◦◦",
            "◦██◦◦██◦◦◦",
        )

        sol = A_star_pathfind(grid)
        expected_path = textwrap.dedent(
            """\
                                        ◦◦██◦◦◦◦↓◦
                                        ◦███◦██◦↙█
                                        ███◦◦◦◦↓██
                                        ◦◦◦◦██◦↙◦◦
                                        ◦█◦◦◦◦↙◦█◦
                                        ██◦██↓█◦██
                                        ██◦██↙█◦██
                                        ◦█◦F←◦█◦██
                                        ◦◦◦◦◦◦◦◦◦◦
                                        ◦██◦◦██◦◦◦"""
        )

        assert sol.path_length == 8
        assert expected_path == sol.print_path()

    """ Validation check tests """

    def test_no_valid_path(self):
        grid = (
            "◦◦◦◦S◦◦",
            "◦██◦███",
            "███◦◦◦◦",
            "◦◦█████",
            "◦F◦█◦◦█"
        )

        with pytest.raises(Exception) as exc_info:
            _ = A_star_pathfind(grid)

        assert str(exc_info.value) == "There is no valid path."

    def test_no_start(self):
        grid = ("◦◦◦◦◦", "◦███◦", "◦◦◦◦◦", "◦◦F◦◦", "◦◦◦◦◦")

        with pytest.raises(ValueError) as exc_info:
            _ = A_star_pathfind(grid)

        assert str(exc_info.value) == "Grid must have one and only one start."

    def test_no_end(self):
        grid = ("◦S◦◦◦", "◦███◦", "◦◦◦◦◦", "◦◦◦◦◦", "◦◦◦◦◦")

        with pytest.raises(ValueError) as exc_info:
            _ = A_star_pathfind(grid)

        assert str(exc_info.value) == "Grid must have one and only one end."

    def test_multiple_starts(self):
        grid = ("◦S◦S◦", "◦███◦", "◦◦◦◦◦", "◦◦F◦◦", "◦◦◦◦◦")

        with pytest.raises(ValueError) as exc_info:
            _ = A_star_pathfind(grid)

        assert str(exc_info.value) == "Grid must have one and only one start."

    def test_multiple_ends(self):
        grid = ("◦S◦◦◦", "◦███◦", "◦◦◦◦◦", "◦◦F◦F", "◦◦◦◦◦")

        with pytest.raises(ValueError) as exc_info:
            _ = A_star_pathfind(grid)

        assert str(exc_info.value) == "Grid must have one and only one end."

    def test_invalid_cell(self):
        grid = ("◦S◦◦◦", "◦███◦", "◦◦◦◦◦", "◦◦F◦X", "◦◦◦◦◦")

        with pytest.raises(ValueError) as exc_info:
            _ = A_star_pathfind(grid)

        assert (
            str(exc_info.value)
            == "Grid has invalid cell. Only cell values (◦ | █ | S | F) allowed."
        )

    def test_nonmatching_row_lengths(self):
        grid = (
            "◦S◦◦◦",
            "◦███◦◦",
            "◦◦◦◦◦",
            "◦◦F◦◦",
            "◦◦◦◦◦"
        )

        with pytest.raises(ValueError) as exc_info:
            _ = A_star_pathfind(grid)

        assert str(exc_info.value) == "Grid row lengths do not match."
