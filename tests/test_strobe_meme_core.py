import random
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from strobe_meme_core import StrobeMemeGenerator  # noqa: E402


class SequenceTests(unittest.TestCase):
    def setUp(self):
        self.generator = StrobeMemeGenerator()

    def test_graycode_supports_mixed_radix(self):
        options = [["吃", "喝", "玩"], ["火锅", "奶茶", "原神"]]
        combinations = self.generator.generate_graycode_combinations(options)

        self.assertEqual(len(combinations), 9)
        self.assertEqual(combinations[0], ["吃", "火锅"])
        self.assertEqual(combinations[1], ["吃", "奶茶"])
        self.assertEqual(combinations[2], ["吃", "原神"])
        self.assertEqual(combinations[3], ["喝", "原神"])

        for left, right in zip(combinations, combinations[1:]):
            diff_count = sum(1 for l_value, r_value in zip(left, right) if l_value != r_value)
            self.assertEqual(diff_count, 1)

    def test_random_mode_is_full_permutation_of_combinations(self):
        random.seed(42)
        options = [["神", "区"], ["神", "区"], ["了", "啦"]]
        combinations = self.generator.generate_random_combinations(options)

        expected = {
            ("神", "神", "了"),
            ("神", "神", "啦"),
            ("神", "区", "了"),
            ("神", "区", "啦"),
            ("区", "神", "了"),
            ("区", "神", "啦"),
            ("区", "区", "了"),
            ("区", "区", "啦"),
        }

        self.assertEqual(len(combinations), len(expected))
        self.assertEqual({tuple(combo) for combo in combinations}, expected)


if __name__ == "__main__":
    unittest.main()
