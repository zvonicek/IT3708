from unittest import TestCase

from ea_impl.lolz import LOLZFitnessEvaluator


__author__ = 'zvonicek'


class TestLOLZFitnessEvaluator(TestCase):
    def test_get_fitness(self):
        ev = LOLZFitnessEvaluator(4)

        self.assertEqual(ev.get_fitness([0, 0, 0, 0, 0, 0]), 4/6)
        self.assertEqual(ev.get_fitness([1, 1, 1, 1, 1, 1]), 1)
        self.assertEqual(ev.get_fitness([1, 1, 0, 1, 0, 1]), 2/6)
        self.assertEqual(ev.get_fitness([0, 0, 1, 0, 1, 1]), 2/6)