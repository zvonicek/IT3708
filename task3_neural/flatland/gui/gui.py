from tkinter import *
from tkinter import ttk
from flatland.flatnand import Cell, Orientation


class GUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.sqsize = 50
        self.grid(row=0, column=0)
        self.board = None

    def draw_flatland(self, flatland):
        mainframe = ttk.Frame(self, padding=(5, 5, 5, 5))
        mainframe.grid(column=0, row=0, sticky=(N, S, E, W))

        self.board = Canvas(mainframe, width=self.sqsize*len(flatland.grid), height=self.sqsize*len(flatland.grid), bg='white')
        self.board.grid(row=1, column=0)

        for row in range(len(flatland.grid)):
            for col in range(len(flatland.grid)):
                top = row * self.sqsize
                left = col * self.sqsize
                bottom = row * self.sqsize + self.sqsize
                right = col * self.sqsize + self.sqsize

                fill = ''
                cell = flatland.grid[row][col]
                if cell == Cell.Food:
                    fill = 'green'
                elif cell == Cell.Poison:
                    fill = 'red'
                elif cell == Cell.Agent:
                    padding = 10
                    if flatland.agent_orientation == Orientation.Up:
                        self.board.create_polygon((left + padding, bottom - padding, left + (right - left) / 2, top + padding, right - padding, bottom - padding), fill="blue")
                    elif flatland.agent_orientation == Orientation.Right:
                        self.board.create_polygon((left + padding, bottom - padding, left + padding, top + padding, right - padding, top + (bottom - top) / 2), fill="blue")
                    elif flatland.agent_orientation == Orientation.Down:
                        self.board.create_polygon((left + padding, top + padding, left + (right - left) / 2, bottom - padding, right - padding, top + padding), fill="blue")
                    elif flatland.agent_orientation == Orientation.Left:
                        self.board.create_polygon((right - padding, bottom - padding, right - padding, top + padding, left + padding, top + (bottom - top) / 2), fill="blue")

                self.board.create_rectangle(left, top, right, bottom, outline='gray', fill=fill)

        self.board.focus_set()
        mainframe.lift()