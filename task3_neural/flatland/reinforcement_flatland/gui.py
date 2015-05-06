import queue
import threading
from tkinter import *
from tkinter import ttk

import matplotlib
from matplotlib.font_manager import FontProperties

from time import sleep


matplotlib.use('TkAgg')
from reinforcement_flatland.flatland import Cell, Flatland, Turn


class GUI(Frame):
    def __init__(self, master, arrows=False):
        Frame.__init__(self, master)
        self.sqsize = 30
        self.grid(row=0, column=0, padx=100)
        self.pack(fill=BOTH, expand=1)
        self.board = None
        self.queue = queue.Queue()
        self.fitnes_plot = True
        self.arrows = arrows

        self.mainframe = ttk.Frame(self, padding=(10, 10, 10, 10))
        self.mainframe.pack(side="top", fill="both", expand=True)

        self.bottom_frame = ttk.Frame(self.mainframe, padding=(10, 10, 10, 10))
        self.bottom_frame.grid(row=2, column=1, padx=100)

        self.running_thread = None

    def replay_scenarios(self, qlearning):
        self.draw_grid(qlearning.flatland)
        self.draw_flatland(qlearning, False)

        self.qlearning = qlearning

    def poll_queue(self):
        try:
            msg = self.queue.get(0)
            self.draw_flatland(msg)

        except queue.Empty:
            pass

        self.master.after(100, self.poll_queue)

    def draw_grid(self, flatlands):
        self.play = Button(self.bottom_frame, text="Play", command=self.play)
        self.play.grid(row=0, column=1)

        label2 = Label(self.bottom_frame, text="Speed")
        label2.grid(row=1, column=0)

        self.scale = Scale(self.bottom_frame, from_=1, to=9, orient=HORIZONTAL)
        self.scale.set(9)
        self.scale.grid(row=1, column=1)

    def play(self):
        if self.running_thread is None or not self.running_thread.is_alive():
            self.queue = queue.Queue()
            self.running_thread = ThreadedFlatlandTask(self.queue, 1-self.scale.get()/10, self.qlearning, self)
            self.running_thread.start()
            self.master.after(100, self.poll_queue)

            self.scale.config(state='disabled')
            self.play.config(text="Stop")
        else:
            self.running_thread.stop()

    def did_stop(self):
        self.scale.config(state='normal')
        self.play.config(text="Play")

    def draw_flatland(self, qlearning, content=True):
        self.board = Canvas(self.mainframe, width=self.sqsize*len(qlearning.flatland.grid[0]), height=self.sqsize*len(qlearning.flatland.grid), bg='white')
        self.board.grid(row=1, column=0, columnspan=3)

        for row in range(len(qlearning.flatland.grid)):
            for col in range(len(qlearning.flatland.grid[0])):
                top = row * self.sqsize
                left = col * self.sqsize
                bottom = row * self.sqsize + self.sqsize
                right = col * self.sqsize + self.sqsize

                fill = ''
                cell = qlearning.flatland.grid[row][col]

                if not content:
                    cell = Cell.Empty

                if cell == Cell.Food:
                    fill = 'green'
                elif cell == Cell.Poison:
                    fill = 'red'
                elif cell == Cell.Agent:
                    padding = 5
                    self.board.create_polygon((left + padding, bottom - padding, left + (right - left) / 2, top + padding, right - padding, bottom - padding), fill="blue")

                self.board.create_rectangle(left, top, right, bottom, outline='gray', fill=fill)

                if self.arrows:
                    padding = 5
                    orientation = qlearning.best_action(((row, col), frozenset(qlearning.eaten)))
                    if orientation == Turn.Left:
                        self.board.create_line(left + padding, top + (bottom - top) / 2, right - padding, bottom - (bottom - top) / 2, arrow="first")
                    elif orientation == Turn.Up:
                        self.board.create_line(left + (right - left) / 2, top + padding, right - (right - left) / 2, bottom - padding, arrow="first")
                    elif orientation == Turn.Right:
                        self.board.create_line(left + padding, top + (bottom - top) / 2, right - padding, bottom - (bottom - top) / 2, arrow="last")
                    elif orientation == Turn.Down:
                        self.board.create_line(left + (right - left) / 2, top + padding, right - (right - left) / 2, bottom - padding, arrow="last")


        self.board.focus_set()
        self.mainframe.lift()


class ThreadedFlatlandTask(threading.Thread):
    def __init__(self, queue, delay, qlearning, parent):
        threading.Thread.__init__(self)
        self.qlearning = qlearning
        self.queue = queue
        self.delay = delay
        self.parent = parent
        self.stop_flag = False

    def stop(self):
        self.stop_flag = True

    def run(self):
        self.qlearning.simulate(self.tick_callback)
        self.parent.did_stop()

    def tick_callback(self, flatland):
        if self.stop_flag:
            return

        self.queue.put(flatland)
        sleep(self.delay)