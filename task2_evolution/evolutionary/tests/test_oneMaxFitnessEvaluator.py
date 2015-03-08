from unittest import TestCase

from ea_impl.one_max_problem import OneMaxFitnessEvaluator


__author__ = 'zvonicek'


class TestOneMaxFitnessEvaluator(TestCase):
    def test_get_fitness(self):
        ev = OneMaxFitnessEvaluator()

        self.assertEqual(ev.get_fitness([0, 0, 0]), 0)
        self.assertEqual(ev.get_fitness([0, 1, 0, 1]), 0.5)
        self.assertEqual(ev.get_fitness([1, 1, 1, 1]), 1.0)
