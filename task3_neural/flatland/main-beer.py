from tkinter import Tk
from beer_tracker.world import World
from beer_tracker.gui import GUI
from beer_tracker.beer_tracker_ann import BeerTrackerAnnFactory

beer = World()
ann = BeerTrackerAnnFactory().create()
tk = Tk()
gui = GUI(tk)
gui.play(beer, ann)
tk.mainloop()
