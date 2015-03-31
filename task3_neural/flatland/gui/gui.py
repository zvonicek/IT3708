import queue
import threading
from time import sleep, time
from tkinter import *
from tkinter import ttk
from flatland.flatland import Cell, Orientation


class GUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.sqsize = 50
        self.grid(row=0, column=0)
        self.board = None
        self.queue = queue.Queue()

    def replay_scenario(self, flatland, ann):
        self.draw_grid(flatland)

        self.queue = queue.Queue()
        ThreadedFlatlandTask(self.queue, 0.3, flatland, ann).start()
        self.master.after(100, self.poll_queue)

    def poll_queue(self):
        try:
            msg = self.queue.get(0)
            self.draw_flatland(msg)

        except queue.Empty:
            pass

        self.master.after(100, self.poll_queue)

    def draw_grid(self, flatland):
        self.mainframe = ttk.Frame(self, padding=(5, 5, 5, 5))
        self.mainframe.grid(column=0, row=0, sticky=(N, S, E, W))

    def draw_flatland(self, flatland):
        self.board = Canvas(self.mainframe, width=self.sqsize*len(flatland.grid), height=self.sqsize*len(flatland.grid), bg='white')
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
        self.mainframe.lift()


class ThreadedFlatlandTask(threading.Thread):
    def __init__(self, queue, delay, flatland, ann):
        threading.Thread.__init__(self)
        self.flatland = flatland
        self.ann = ann
        self.queue = queue
        self.delay = delay

    def run(self):
        self.flatland.simulate(self.ann, self.tick_callback)

    def tick_callback(self, flatland):
        self.queue.put(flatland)
        sleep(self.delay)