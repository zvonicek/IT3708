from tkinter import Tk
from flatland.flatland import Flatland, Turn
from flatland.flatland_ann import FlatlandAnnFactory
from flatland.flatland_ea import FlatlandEA
from gui.gui import GUI

f = Flatland(10, (1/3, 1/3), (2, 2))
ann = FlatlandAnnFactory().create()
ea = FlatlandEA(f, ann)
ea.run()

tk = Tk()
gui = GUI(tk)

gui.draw_flatland(f)

tk.mainloop()