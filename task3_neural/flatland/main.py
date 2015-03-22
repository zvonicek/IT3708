from tkinter import Tk
from flatland.flatnand import Flatland
from gui.gui import GUI

f = Flatland(10, (1/3, 1/3))
tk = Tk()
gui = GUI(tk)
gui.draw_flatland(f)
tk.mainloop()
