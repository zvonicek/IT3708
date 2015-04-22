import getopt
import sys
from beer_tracker.beer_tracker_ea import BeerTrackerEA, BeerTrackerPullEA, BeerTrackerNoWrapEA

ea = BeerTrackerEA()

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "pw", ["pull", "wrap"])
    except getopt.GetoptError as e:
        print('main-beer.py -p')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-p':
            ea = BeerTrackerPullEA()
        elif opt == '-w':
            ea = BeerTrackerNoWrapEA()

if type(ea) is BeerTrackerEA:
    print("computing standard")
elif type(ea) is BeerTrackerPullEA:
    print("computing pull")
elif type(ea) is BeerTrackerNoWrapEA:
    print("computing no-wrap")

ea.run()