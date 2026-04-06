import random
import sys
import unittest
from pathlib import Path
import tempfile

from PIL import Image

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

    def test_save_as_gif_uses_pillow_multi_frame_output(self):
        frames = [
            Image.new("RGB", (8, 8), (255, 255, 255)),
            Image.new("RGB", (8, 8), (0, 0, 0)),
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "sample.gif"
            self.generator.save_as_gif(frames, str(output_path), duration=0.01)

            self.assertTrue(output_path.exists())

            with Image.open(output_path) as gif:
                self.assertEqual(gif.n_frames, 2)
                self.assertEqual(gif.info.get("duration"), 20)


if __name__ == "__main__":
    unittest.main()
