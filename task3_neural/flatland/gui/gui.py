from tkinter import *
from tkinter import ttk
from flatland.flatnand import Cell


class GUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.sqsize = 50
        self.grid(row=0, column=0)
        pass

    def draw_flatland(self, flatland):
        mainframe = ttk.Frame(self, padding=(5, 5, 5, 5))
        mainframe.grid(column=0, row=0, sticky=(N, S, E, W))

        self.board = Canvas(mainframe, width=self.sqsize*len(flatland.grid), height=self.sqsize*len(flatland.grid), bg='white')
        self.board.grid(row=1,column=0)

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

                rect = self.board.create_rectangle(left, top, right, bottom, outline='gray', fill=fill)

        self.board.focus_set()