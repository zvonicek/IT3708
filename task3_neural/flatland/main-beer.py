from tkinter import Tk
from beer_tracker.world import World
from beer_tracker.gui import GUI

beer = World()

tk = Tk()
gui = GUI(tk)
gui.play(beer, None)
tk.mainloop()
