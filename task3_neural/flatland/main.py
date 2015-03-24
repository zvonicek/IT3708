from tkinter import Tk
from flatland.flatland import Flatland, Turn
from gui.gui import GUI

f = Flatland(10, (1/3, 1/3), (2, 2))

tk = Tk()
gui = GUI(tk)

gui.draw_flatland(f)

gui.draw_flatland(f)

tk.mainloop()
