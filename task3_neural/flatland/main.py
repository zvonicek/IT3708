from tkinter import Tk
from flatland.flatland import Flatland, Turn
from flatland.flatland_ann import FlatlandAnnFactory
from gui.gui import GUI

f = Flatland(10, (1/3, 1/3), (2, 2))

tk = Tk()
gui = GUI(tk)

gui.draw_flatland(f)

gui.draw_flatland(f)

ann = FlatlandAnnFactory().create()
ann.set_weights([1, 2, 3, 4, 5, 6])
res = ann.compute([1, 1, 1, 1, 1, 1])
print(res)

#tk.mainloop()