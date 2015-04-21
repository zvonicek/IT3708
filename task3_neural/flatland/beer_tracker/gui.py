from time import sleep
import queue
import threading
from tkinter import Frame, BOTH, ttk, Canvas, N, S, E, W


class GUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.sqsize = 20
        self.grid(row=0, column=0, padx=100)
        self.pack(fill=BOTH, expand=1)
        self.board = None
        self.queue = queue.Queue()

        self.mainframe = ttk.Frame(self, padding=(10, 10, 10, 10))
        self.mainframe.pack(side="top", fill="both", expand=True)

        self.bottom_frame = ttk.Frame(self.mainframe, padding=(10, 10, 10, 10))
        self.bottom_frame.grid(row=2, column=1, padx=100)

    def play(self, world, ann):
        self.queue = queue.Queue()
        self.running_thread = ThreadedBeerTask(self.queue, 0.4, world, ann, self)
        self.running_thread.start()
        self.master.after(100, self.poll_queue)

    def poll_queue(self):
        try:
            msg = self.queue.get(0)
            self.draw_world(msg)

        except queue.Empty:
            pass

        self.master.after(100, self.poll_queue)

    def draw_world(self, world):
        self.board = Canvas(self.mainframe, width=self.sqsize*30, height=self.sqsize*15, bg='white')
        self.board.grid(row=1, column=0, columnspan=3, sticky=(N, S, E, W))

        for row in range(15):
            for col in range(30):
                top = row * self.sqsize
                left = col * self.sqsize
                bottom = row * self.sqsize + self.sqsize
                right = col * self.sqsize + self.sqsize

                fill = ''

                if world.contains_tracker(row, col):
                    if world.object_captured:
                        fill = '#F4B589'
                    elif world.object_pulled:
                        fill = '#FEF59E'
                    elif world.large_object_hit:
                        fill = '#EF9FA4'
                    else:
                        fill = '#91B0DB'
                elif world.contains_object(row, col):
                    if len(world.object_position) > 4:
                        fill = '#F19C7E'
                    else:
                        fill = '#97CC9E'

                self.board.create_rectangle(left, top, right, bottom, outline='#F3EFF0', width=1, fill=fill)

        world.object_captured = False
        world.large_object_hit = False
        self.board.focus_set()
        self.mainframe.lift()


class ThreadedBeerTask(threading.Thread):
    def __init__(self, queue, delay, world, ann, parent):
        threading.Thread.__init__(self)
        self.world = world
        self.ann = ann
        self.queue = queue
        self.delay = delay
        self.parent = parent
        self.stop_flag = False

    def stop(self):
        self.stop_flag = True

    def run(self):
        self.world.simulate(self.ann, self.tick_callback, True)

    def tick_callback(self, flatland):
        if self.stop_flag:
            return

        self.queue.put(flatland)
        sleep(self.delay)