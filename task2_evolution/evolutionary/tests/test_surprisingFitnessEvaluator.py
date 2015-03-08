from unittest import TestCase

from ea_impl.suprising_sequences import SurprisingFitnessEvaluator


__author__ = 'zvonicek'


class TestSurprisingFitnessEvaluator(TestCase):
    def test_is_surprising(self):
        eval = SurprisingFitnessEvaluator(3, 3)

        self.assertEquals(eval.is_surprising([1, 2, 3, 3, 2, 1], 0), 0)
        self.assertEquals(eval.is_surprising([1, 2, 3, 3, 2, 1], 1), 0)
        self.assertEquals(eval.is_surprising([1, 2, 3, 3, 2, 1], 2), 0)
        self.assertEquals(eval.is_surprising([1, 2, 2, 1, 3, 3, 1], 0), 0)
        self.assertEquals(eval.is_surprising([1, 2, 2, 1, 3, 3, 1], 2), 2)
        self.assertEquals(eval.is_surprising([1, 2, 3, 2, 3], 0), 1)

    def test_get_fitness(self):
        eval = SurprisingFitnessEvaluator(1, 4)

        self.assertEquals(eval.get_fitness([1, 1, 1, 1]), 1/4)
