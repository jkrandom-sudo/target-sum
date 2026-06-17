import unittest

import target_sum as core


class FixedRng:
    def __init__(self):
        self.ints = [2, 4, 6, 8, 10]

    def randint(self, low, high):
        return self.ints.pop(0)

    def sample(self, seq, count):
        return [0, 2]


class TestCore(unittest.TestCase):
    def test_config_fallback(self):
        self.assertEqual(core.config("bad"), core.config("normal"))

    def test_make_puzzle(self):
        puzzle = core.make_puzzle("easy", FixedRng())
        self.assertEqual(puzzle["numbers"], [2, 4, 6, 8, 10])
        self.assertEqual(puzzle["solution"], [0, 2])
        self.assertEqual(puzzle["target"], 8)

    def test_parse_indices(self):
        self.assertEqual(core.parse_indices("1, 3", 5), [0, 2])
        self.assertEqual(core.parse_indices("2 5", 5), [1, 4])
        self.assertIsNone(core.parse_indices("1 1", 5))
        self.assertIsNone(core.parse_indices("0", 5))
        self.assertIsNone(core.parse_indices("x", 5))

    def test_choice_sum_and_correct(self):
        puzzle = {"numbers": [2, 4, 6], "target": 8, "pick": 2, "solution": [0, 2]}
        self.assertEqual(core.choice_sum(puzzle["numbers"], [0, 2]), 8)
        self.assertTrue(core.is_correct(puzzle, [0, 2]))
        self.assertFalse(core.is_correct(puzzle, [0, 1]))
        self.assertFalse(core.is_correct(puzzle, [0]))

    def test_text_helpers(self):
        puzzle = {"numbers": [2, 4, 6], "target": 8, "pick": 2, "solution": [0, 2]}
        self.assertEqual(core.hint_text(puzzle), "1")
        self.assertEqual(core.numbers_text([2, 4, 6]), "1:2 2:4 3:6")

    def test_score_for(self):
        self.assertEqual(core.score_for("easy", 1), 35)
        self.assertEqual(core.score_for("normal", 1), 70)
        self.assertEqual(core.score_for("easy", 1, used_hint=True), 17)
        self.assertEqual(core.score_for("easy", 1, correct=False), 0)

    def test_final_rating(self):
        self.assertEqual(core.final_rating(6, 6), "perfect")
        self.assertEqual(core.final_rating(4, 6), "solver")
        self.assertEqual(core.final_rating(2, 6), "learner")
        self.assertEqual(core.final_rating(0, 6), "lost")


if __name__ == "__main__":
    unittest.main()
