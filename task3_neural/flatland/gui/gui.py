from cmath import pi
import queue
import threading
from time import sleep, time
from tkinter import *
from tkinter import ttk
from math import sin
import matplotlib
from matplotlib.font_manager import FontProperties

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from numpy import arange
from flatland.flatland import Cell, Orientation, Flatland


class GUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.sqsize = 50
        self.grid(row=0, column=0, padx=100)
        self.pack(fill=BOTH, expand=1)
        self.board = None
        self.queue = queue.Queue()


        self.mainframe = ttk.Frame(self, padding=(10, 10, 10, 10), bg="white")
        self.mainframe.pack(side="top", fill="both", expand=True)

        self.bottom_frame = ttk.Frame(self.mainframe, padding=(10, 10, 10, 10))
        self.bottom_frame.grid(row=2, column=1, padx=100)

        self.flatlands = None
        self.ann = None
        self.running_thread = None

    def replay_scenarios(self, flatlands, ann, statistics):
        self.draw_grid(flatlands)
        self.draw_stats(statistics)
        self.draw_flatland(flatlands[0], False)

        self.flatlands = flatlands
        self.ann = ann

    def poll_queue(self):
        try:
            msg = self.queue.get(0)
            self.draw_flatland(msg)

        except queue.Empty:
            pass

        self.master.after(100, self.poll_queue)

    def draw_grid(self, flatlands):
        label = Label(self.bottom_frame, text="Scenario")
        label.grid(row=0, column=0)

        self.options = []
        for i in range(len(flatlands)):
            self.options.append("Scenario " + str(i+1))
        self.options.append("Random scenario")

        self.option_variable = StringVar(self.bottom_frame)
        self.option_variable.set(self.options[0])
        self.option = OptionMenu(self.bottom_frame, self.option_variable, *tuple(self.options))
        self.option.grid(row=0, column=1)

        self.play = Button(self.bottom_frame, text="Play", command=self.play)
        self.play.grid(row=0, column=2)

        label2 = Label(self.bottom_frame, text="Speed")
        label2.grid(row=1, column=0)

        self.scale = Scale(self.bottom_frame, from_=1, to=9, orient=HORIZONTAL)
        self.scale.set(7)
        self.scale.grid(row=1, column=1)

    def play(self):
        selected_index = self.options.index(self.option_variable.get())
        if selected_index < len(self.flatlands):
            selected_flatland = self.flatlands[selected_index]
        else:
            selected_flatland = Flatland(10, (1/3, 1/3), (2, 2))

        if self.running_thread is None or not self.running_thread.is_alive():
            self.queue = queue.Queue()
            self.running_thread = ThreadedFlatlandTask(self.queue, 1-self.scale.get()/10, selected_flatland, self.ann, self)
            self.running_thread.start()
            self.master.after(100, self.poll_queue)

            self.option.config(state='disabled')
            self.scale.config(state='disabled')
            self.play.config(text="Stop")
        else:
            self.running_thread.stop()

    def did_stop(self):
        self.option.config(state='normal')
        self.scale.config(state='normal')
        self.play.config(text="Play")

    def draw_stats(self, data):
        f = Figure(figsize=(5, 5), dpi=70)
        a = f.add_subplot(111)

        canvas = FigureCanvasTkAgg(f, master=self.mainframe)
        canvas.show()
        canvas.get_tk_widget().grid(row=1, column=4, padx=100)

        a.plot(data[0])
        a.plot(data[1])
        a.plot(data[2])
        prop = FontProperties()
        prop.set_size('small')
        a.legend(['best', 'average', 'std'], loc='lower right', prop=prop)

    def draw_flatland(self, flatland, content=True):
        self.board = Canvas(self.mainframe, width=self.sqsize*len(flatland.grid), height=self.sqsize*len(flatland.grid), bg='white')
        self.board.grid(row=1, column=0, columnspan=3, sticky=(N, S, E, W))

        for row in range(len(flatland.grid)):
            for col in range(len(flatland.grid)):
                top = row * self.sqsize
                left = col * self.sqsize
                bottom = row * self.sqsize + self.sqsize
                right = col * self.sqsize + self.sqsize

                fill = ''
                cell = flatland.grid[row][col]

                if not content:
                    cell = Cell.Empty

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
    def __init__(self, queue, delay, flatland, ann, parent):
        threading.Thread.__init__(self)
        self.flatland = flatland
        self.ann = ann
        self.queue = queue
        self.delay = delay
        self.parent = parent
        self.stop_flag = False

    def stop(self):
        self.stop_flag = True

    def run(self):
        self.flatland.simulate(self.ann, self.tick_callback)
        self.parent.did_stop()

    def tick_callback(self, flatland):
        if self.stop_flag:
            return

        self.queue.put(flatland)
        sleep(self.delay)