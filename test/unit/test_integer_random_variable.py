import fractions
import unittest

import dice.integer_random_variable as irv

irv.probability = irv.probability_fraction


class TestIntegerRandomVariable(unittest.TestCase):
    def test_dice_notation_rv(self) -> None:
        d6_odds = irv.dice_notation_rv('d6')
        for i, pair in enumerate(d6_odds, start=1):
            self.assertEqual(i, pair[0])
            self.assertEqual(fractions.Fraction(1, 6), pair[1])

    def test_dedupe_rv(self) -> None:
        rv = [(1, 0.5), (1, 0.2), (2, 0.3)]
        deduped_rv = irv.dedupe_rv(rv)
        self.assertEqual(2, len(deduped_rv))
        for i, p in deduped_rv:
            if i == 1:
                self.assertAlmostEqual(p, 0.7)
            if i == 2:
                self.assertAlmostEqual(p, 0.3)

    def test_sum_rv(self) -> None:
        d6_odds = irv.dice_notation_rv('d6')
        sum_odds = irv.sum_rv(d6_odds, d6_odds)
        self.assertEqual(11, len(sum_odds))
        for i, p in sum_odds:
            if i == 2:
                self.assertAlmostEqual(p, 1 / 36)
            if i == 3:
                self.assertAlmostEqual(p, 2 / 36)

    def test_die_rv(self) -> None:
        odds = irv.die_rv(num_dice=3, num_faces=6)
        self.assertEqual(16, len(odds))
        for i, p in odds:
            if i == 3:
                self.assertAlmostEqual(p, 1 / 216)
            if i == 4:
                self.assertAlmostEqual(p, 3 / 216)

    def test_keep_high_rv(self) -> None:
        odds = irv.keep_high_rv(num_dice=4, num_faces=6, num_keep=3)
        self.assertEqual(16, len(odds))
        for i, p in odds:
            if i == 3:
                self.assertAlmostEqual(p, 1 / 1296)
            if i == 4:
                self.assertAlmostEqual(p, 4 / 1296)

    def test_dedupe_mrv(self) -> None:
        odds = [([1, 1, 1], 0.5),
                ([1, 1, 1], 0.2),
                ([1, 1, 2], 0.2),
                ([2, 1, 1], 0.1)]
        deduped_odds = irv.dedupe_mrv(odds)
        self.assertEqual(3, len(deduped_odds))
        for a, p in deduped_odds:
            if a == [1, 1, 1]:
                self.assertAlmostEqual(p, 0.7)
            if a == [1, 1, 2]:
                self.assertAlmostEqual(p, 0.2)
            if a == [2, 1, 1]:
                self.assertAlmostEqual(p, 0.1)

    def test_tail_mrv(self) -> None:
        odds = [([1, 2, 3], 0.5),
                ([1, 1, 3], 0.2),
                ([1, 2, 2], 0.2),
                ([1, 2, 2], 0.1)]
        shortened_odds = irv.tail_mrv(odds, 2)
        self.assertEqual(4, len(shortened_odds))
        print(shortened_odds)
        deduped_odds = irv.dedupe_mrv(shortened_odds)
        self.assertEqual(3, len(deduped_odds))
        for a, p in deduped_odds:
            if a == [2, 3]:
                self.assertAlmostEqual(p, 0.5)
            if a == [1, 3]:
                self.assertAlmostEqual(p, 0.2)
            if a == [2, 2]:
                self.assertAlmostEqual(p, 0.3)

    def test_sum_mrv_rv(self) -> None:
        pass

    def test_cartesian_product_mrv(self) -> None:
        pass

    def test_dice_notation_egf(self) -> None:
        pass

if __name__ == '__main__':
    unittest.main()
