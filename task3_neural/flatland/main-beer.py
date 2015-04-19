from tkinter import Tk
from beer_tracker.beer_tracker_ea import BeerTrackerEA
from beer_tracker.world import World
from beer_tracker.gui import GUI
from beer_tracker.beer_tracker_ann import BeerTrackerAnnFactory

ann = BeerTrackerAnnFactory().create()
ea = BeerTrackerEA(ann)
ea.run()