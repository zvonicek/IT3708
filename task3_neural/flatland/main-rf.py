import getopt
import sys
from reinforcement_flatland.flatland_ann import FlatlandAnnFactory
from reinforcement_flatland.flatland_ea import FlatlandEA

world_file = "1-simple.txt"

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        world_file = sys.argv[1]

ann = FlatlandAnnFactory().create()
ea = FlatlandEA(ann, "../../task5_q_learning/worlds/"+world_file)
ea.run()