from unittest import TestCase
from beer_tracker.beer_tracker_ea import BeerTrackerGenotypeCoder


class TestBeerTrackerGenotypeCoder(TestCase):
    def setUp(self):
        self.coder = BeerTrackerGenotypeCoder(8)
        self.coder.add_parameter(-1, 1, lambda: 0.2)
        self.coder.add_parameter(-1, 1, lambda: 1)
        self.coder.add_parameter(-5, 0, lambda: -2.2)
        self.coder.add_parameter(0, 10, lambda: 8.8888)
        self.coder.add_parameter(-100, 100, lambda: 0)

    def test_generate_init_genotype(self):
        init_gen = self.coder.generate_init_genotype()
        self.assertEqual(init_gen, [1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1])

    def test_decode_genotype(self):
        decoded_val = self.coder.decode_genotype([153, 255, 143, 227, 127])
        self.assertEqual(decoded_val, [0.19999999999999996, 1.0, -2.196078431372549, 8.901960784313726, -0.39215686274509665])