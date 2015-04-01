from flatland.flatland_ann import FlatlandAnnFactory
from flatland.flatland_ea import FlatlandEA

ann = FlatlandAnnFactory().create()
ea = FlatlandEA(ann, True, 5)
ea.run()