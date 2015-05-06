import getopt
import sys
from reinforcement_flatland.gui import GUI
from reinforcement_flatland.qlearning import QLearning
from tkinter import Tk

world_file = "1-simple.txt"

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        world_file = sys.argv[1]

q = QLearning("../../task5_q_learning/worlds/"+world_file)
q.q_learning()

tk = Tk()
tk.wm_title(world_file)
gui = GUI(tk)
gui.replay_scenarios(q)
tk.mainloop()