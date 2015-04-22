from tkinter import Tk
from beer_tracker.beer_tracker_ann import BeerTrackerAnnFactory
from beer_tracker.gui import GUI
from beer_tracker.world import World
from collections import namedtuple

__author__ = 'xtesaro2'

ann_weights = [5.0, -4.647058823529412, -4.0588235294117645, -1.2745098039215685, 5.0, 2.019607843137255, 2.2941176470588234, -3.8627450980392157, 0.09803921568627416, 3.980392156862745, -2.9607843137254903, 5.0, 1.3529411764705879, 3.0, 2.1764705882352944, -1.0, 1.0, -3.0, -3.0, 4.294117647058824, 1.0, 5.0, -1.0196078431372548, -0.35294117647058876, -0.7058823529411757, -9.019607843137255, 4.921568627450981, 3.996078431372549, 2.003921568627451, 2.992156862745098, 1.0, 1.2509803921568627, 1.003921568627451, 2.0]
params = namedtuple('Params', 'capture_reward avoidance_reward capture_punishment avoidance_punishment')
def fitness_parameters():
        capture_reward = 4
        avoidance_reward = 3
        capture_punishment = 3
        avoidance_punishment = 3.3

        return params(capture_reward, avoidance_reward, capture_punishment, avoidance_punishment)
# prvni je pull, druhy wrap
ann = BeerTrackerAnnFactory().create(False, True)
ann.set_weights(ann_weights)
world = World(fitness_parameters(), False, True)

# Pro testovani konkretnich vstupu pro ann, vypis na terminal (stavy zacinaji jako 0)
ann_inputs = [[1,1,1,0,0], [1,1,1,0,0],[1,1,1,0,0]]


for i in ann_inputs:
    print(i, ann.compute(i))

print("------------------")

ann.set_state(0)
ann_inputs = [[0,0,1,1,1], [0,0,1,1,1],[0,0,1,1,1]]

for i in ann_inputs:
    print(i, ann.compute(i))

# Pro testovani konkretnich vstupu a konkretnich poc. stavu:
"""ann_inputs = [[1,1,0,0,0]]
states_values = [-3,0,3]

for v in states_values:
    ann.set_state(v)
    for i in ann_inputs:
        print(v, i, ann.compute(i))
"""


# Pro testovani ruznych stavu ann

# Kdyz budeme chtit spustit gui s timto fentoypem
"""
tk = Tk()
gui = GUI(tk)
gui.play(world, ann, ([],[],[]))
tk.mainloop()
"""
