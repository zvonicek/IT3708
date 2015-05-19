import getopt
import sys
from reinforcement_flatland.gui import GUI
from reinforcement_flatland.qlearning import QLearning
from tkinter import Tk

world_file = "1-simple.txt"
iterations = 2000

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        world_file = sys.argv[1]
        iterations = int(sys.argv[2])

q = QLearning("../worlds/"+world_file, iterations)
q.q_learning()

tk = Tk()
tk.wm_title(world_file)
gui = GUI(tk)
gui.replay_scenarios(q)
tk.mainloop()