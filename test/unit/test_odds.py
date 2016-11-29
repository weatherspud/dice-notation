import fractions
import unittest

import dice.odds as odds

odds.probability = odds.probability_fraction


class TestIntegerRandomVariable(unittest.TestCase):
    def test_dice_notation_rv(self) -> None:
        d6_odds = odds.dice_notation_rv('d6')
        for i, pair in enumerate(d6_odds, start=1):
            self.assertEqual(i, pair[0])
            self.assertEqual(fractions.Fraction(1, 6), pair[1])

    def test_dedupe_rv(self) -> None:
        rv = [(1, 0.5), (1, 0.2), (2, 0.3)]
        deduped_rv = odds.dedupe_rv(rv)
        self.assertEqual(2, len(deduped_rv))
        for i, p in deduped_rv:
            if i == 1:
                self.assertAlmostEqual(p, 0.7)
            if i == 2:
                self.assertAlmostEqual(p, 0.3)

    def test_sum_rv(self) -> None:
        d6_odds = odds.dice_notation_rv('d6')
        sum_odds = odds.sum_rv(d6_odds, d6_odds)
        self.assertEqual(11, len(sum_odds))
        for i, p in sum_odds:
            if i == 2:
                self.assertAlmostEqual(p, 1 / 36)
            if i == 3:
                self.assertAlmostEqual(p, 2 / 36)

    def test_die_rv(self) -> None:
        _odds = odds.die_rv(num_dice=3, num_faces=6)
        self.assertEqual(16, len(_odds))
        for i, p in _odds:
            if i == 3:
                self.assertAlmostEqual(p, 1 / 216)
            if i == 4:
                self.assertAlmostEqual(p, 3 / 216)

    def test_keep_high_rv(self) -> None:
        _odds = odds.keep_high_rv(num_dice=4, num_faces=6, num_keep=3)
        self.assertEqual(16, len(_odds))
        for i, p in _odds:
            if i == 3:
                self.assertAlmostEqual(p, 1 / 1296)
            if i == 4:
                self.assertAlmostEqual(p, 4 / 1296)

    def test_dedupe_mrv(self) -> None:
        _odds = [([1, 1, 1], 0.5),
                 ([1, 1, 1], 0.2),
                 ([1, 1, 2], 0.2),
                 ([2, 1, 1], 0.1)]
        deduped_odds = odds.dedupe_mrv(_odds)
        self.assertEqual(3, len(deduped_odds))
        for a, p in deduped_odds:
            if a == [1, 1, 1]:
                self.assertAlmostEqual(p, 0.7)
            if a == [1, 1, 2]:
                self.assertAlmostEqual(p, 0.2)
            if a == [2, 1, 1]:
                self.assertAlmostEqual(p, 0.1)

    def test_tail_mrv(self) -> None:
        _odds = [([1, 2, 3], 0.5),
                 ([1, 1, 3], 0.2),
                 ([1, 2, 2], 0.2),
                 ([1, 2, 2], 0.1)]
        shortened_odds = odds.tail_mrv(_odds, 2)
        self.assertEqual(4, len(shortened_odds))
        deduped_odds = odds.dedupe_mrv(shortened_odds)
        self.assertEqual(3, len(deduped_odds))
        for a, p in deduped_odds:
            if a == [2, 3]:
                self.assertAlmostEqual(p, 0.5)
            if a == [1, 3]:
                self.assertAlmostEqual(p, 0.2)
            if a == [2, 2]:
                self.assertAlmostEqual(p, 0.3)

    def test_sum_mrv_rv(self) -> None:
        mrv = [([1, 1, 1], 0.5),
               ([1, 1, 2], 0.2),
               ([1, 2, 1], 0.2),
               ([1, 2, 2], 0.1)]
        rv = odds.sum_mrv_rv(mrv)
        self.assertEqual(3, len(rv))
        for i, p in rv:
            if i == 3:
                self.assertAlmostEqual(p, 0.5)
            if i == 4:
                self.assertAlmostEqual(p, 0.4)
            if i == 5:
                self.assertAlmostEqual(p, 0.1)

    def test_cartesian_product_mrv(self) -> None:
        mrv = [([1], 0.5),
               ([2], 0.3),
               ([3], 0.2)]
        rv = [(4, 0.6),
              (5, 0.4)]
        prod = odds.cartesian_product_mrv(mrv, rv)
        self.assertEqual(6, len(prod))
        for a, p in prod:
            if a == [1, 4]:
                self.assertAlmostEqual(p, 0.3)
            if a == [2, 5]:
                self.assertAlmostEqual(p, 0.12)

    def test_dice_notation_egf(self) -> None:
        egf = odds.dice_notation_egf('3d6')
        self.assertEqual(16, len(egf))
        for i, p in egf:
            if i == 3:
                self.assertAlmostEqual(p, 1.0)
            if i == 4:
                self.assertAlmostEqual(p, 215 / 216)
            if i == 18:
                self.assertAlmostEqual(p, 1 / 216)

if __name__ == '__main__':
    unittest.main()
