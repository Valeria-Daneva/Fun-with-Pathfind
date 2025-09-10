import tkinter as tk

from a_star import A_star_pathfind


def app() -> None:
    root = tk.Tk()

    # Setting some window properties
    root.title("Fun with Pathfind")
    root.configure(background="gray")
    root.minsize(500, 500)
    root.maxsize(800, 800)
    root.geometry("300x300+50+50")

    root.mainloop()


if __name__ == "__main__":
    app()
