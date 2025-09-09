from a_star import A_star_pathfind


def main():
    grid = (
        "◦◦██◦◦◦◦◦◦",
        "◦███◦██◦◦█",
        "███◦◦◦◦S██",
        "◦◦◦◦██◦◦◦◦",
        "◦█◦◦◦◦◦◦█◦",
        "██F██◦█◦██",
        "██◦██◦█◦██",
        "◦█◦◦◦◦█◦██",
        "◦◦◦◦◦◦◦◦◦◦",
        "◦██◦◦██◦◦◦",
    )
    sol = A_star_pathfind(grid)

    print("Shortest path length: " + str(sol.shortest_path))
    print("Path:")
    print()
    print(sol.print_path())


if __name__ == "__main__":
    main()
