import getopt
import sys
from reinforcement_flatland.flatland_ann import FlatlandAnnFactory
from reinforcement_flatland.flatland_ea import FlatlandEA


dynamic = False
scenarios = 1

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ds:", ["dynamic", "scenarios="])
    except getopt.GetoptError as e:
        print('main-f.py -d True -s 5')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-d':
            dynamic = True
        elif opt in ("-s", "--scenarios"):
            scenarios = int(arg)

print("computing dynamic:", dynamic, "with", scenarios, "scenarios")

ann = FlatlandAnnFactory().create()
ea = FlatlandEA(ann, dynamic, scenarios)
ea.run()