import unittest

import dice.roll as roll


class TestRoll(unittest.TestCase):
    def test_roll(self: object) -> None:
        self.assertEqual(roll.roll('8'), 8)

    def test_die(self: object) -> None:
        result = roll.roll('d6')
        self.assertTrue(isinstance(result, int))
        self.assertTrue(1 <= result <= 6)

    def test_dice(self: object) -> None:
        result = roll.roll('3d6')
        self.assertTrue(isinstance(result, int))
        self.assertTrue(3 <= result <= 18)

    def test_add(self: object) -> None:
        self.assertEqual(roll.roll('3+7'), 10)

    def test_subtract(self: object) -> None:
        self.assertEqual(roll.roll('3-7'), -4)

    def test_multiply(self: object) -> None:
        self.assertEqual(roll.roll('3*7'), 21)

    def test_dice_expression(self: object) -> None:
        result = roll.roll('3d6-2')
        self.assertTrue(isinstance(result, int))
        self.assertTrue(1 <= result <= 16)

    def test_keep(self: object) -> None:
        result = roll.roll('4d6k3')
        self.assertTrue(isinstance(result, int))
        self.assertTrue(3 <= result <= 18)

    def test_keep_high(self: object) -> None:
        result = roll.roll('4d6kh3')
        self.assertTrue(isinstance(result, int))
        self.assertTrue(3 <= result <= 18)

    def test_keep_low(self: object) -> None:
        result = roll.roll('4d6kl3')
        self.assertTrue(isinstance(result, int))
        self.assertTrue(3 <= result <= 18)

    def test_drop(self: object) -> None:
        result = roll.roll('4d6d1')
        self.assertTrue(isinstance(result, int))
        self.assertTrue(3 <= result <= 18)

    def test_drop_low(self: object) -> None:
        result = roll.roll('4d6dl1')
        self.assertTrue(isinstance(result, int))
        self.assertTrue(3 <= result <= 18)

    def test_drop_high(self: object) -> None:
        result = roll.roll('4d6dh1')
        self.assertTrue(isinstance(result, int))
        self.assertTrue(3 <= result <= 18)


if __name__ == '__main__':
    unittest.main()
