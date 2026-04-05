"""
频闪梗图生成器核心逻辑
"""

from itertools import product
from pathlib import Path
from typing import List, Optional, Sequence, Tuple
import os
import random
import re
import warnings

import imageio
from PIL import Image, ImageDraw, ImageFont


warnings.filterwarnings("ignore", category=UserWarning, module="PIL")


Parts = List[Optional[str]]
Options = List[Optional[List[str]]]
Combination = List[str]


class StrobeMemeGenerator:
    """频闪梗图生成器核心类"""

    def __init__(self):
        self.bg_color = (255, 255, 255)
        self.text_color = (0, 0, 0)
        self.font_size = 100
        self.font = self._load_font()
        self.padding = 40
        self.line_spacing = 20

    def _load_font(self):
        """加载中文字体"""
        font_paths = [
            "simhei.ttf",
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simsun.ttc",
            "/System/Library/Fonts/PingFang.ttc",
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        ]

        for path in font_paths:
            if os.path.exists(path):
                try:
                    font = ImageFont.truetype(path, self.font_size)
                    print(f"成功加载字体: {path}")
                    return font
                except Exception:
                    continue

        print("未找到指定字体，使用默认字体")
        return ImageFont.load_default()

    def parse_text(self, text: str) -> Tuple[Parts, Options]:
        """解析文本，支持 {选项A/选项B} 语法"""
        parts: Parts = []
        options: Options = []

        pattern = r"\{([^}]+)\}"
        last_end = 0

        for match in re.finditer(pattern, text):
            if match.start() > last_end:
                fixed_text = text[last_end:match.start()]
                for char in fixed_text:
                    parts.append(char)
                    options.append(None)

            option_text = match.group(1)
            option_list = [opt.strip() for opt in option_text.split("/")]
            parts.append(None)
            options.append(option_list)
            last_end = match.end()

        if last_end < len(text):
            for char in text[last_end:]:
                parts.append(char)
                options.append(None)

        return parts, options

    def _variable_positions(self, options: Options) -> List[List[str]]:
        return [opt for opt in options if opt is not None]

    def generate_graycode_combinations(self, options: Options) -> List[Combination]:
        """
        生成混合进制格雷码顺序的组合。
        相邻组合只会有一个位置发生变化。
        """
        variable_positions = self._variable_positions(options)
        if not variable_positions:
            return [[]]

        radices = [len(position) for position in variable_positions]
        index_sequences = self._generate_mixed_radix_gray_indices(radices)

        return [
            [variable_positions[pos][choice_index] for pos, choice_index in enumerate(indices)]
            for indices in index_sequences
        ]

    def _generate_mixed_radix_gray_indices(self, radices: Sequence[int]) -> List[List[int]]:
        if not radices:
            return [[]]

        suffixes = self._generate_mixed_radix_gray_indices(radices[1:])
        sequences: List[List[int]] = []

        for prefix_value in range(radices[0]):
            ordered_suffixes = suffixes if prefix_value % 2 == 0 else list(reversed(suffixes))
            for suffix in ordered_suffixes:
                sequences.append([prefix_value, *suffix])

        return sequences

    def generate_random_combinations(self, options: Options) -> List[Combination]:
        """
        生成完整组合集合并完全打乱。
        保证一个循环内每种组合恰好出现一次。
        """
        variable_positions = self._variable_positions(options)
        if not variable_positions:
            return [[]]

        combinations = [list(combo) for combo in product(*variable_positions)]
        random.shuffle(combinations)
        return combinations

    def create_frame(self, parts: Parts, combination: Combination) -> Image.Image:
        """创建单帧图像，支持自适应尺寸和多行文本"""
        chars = []
        combo_idx = 0
        for part in parts:
            if part is None:
                chars.append(combination[combo_idx])
                combo_idx += 1
            else:
                chars.append(part)

        text = "".join(chars)
        lines = text.split("\n")

        temp_img = Image.new("RGB", (1, 1), self.bg_color)
        temp_draw = ImageDraw.Draw(temp_img)

        line_dimensions = []
        max_width = 0
        total_height = 0

        for line in lines:
            if not line:
                line_dimensions.append((0, self.font_size))
                total_height += self.font_size + self.line_spacing
            else:
                bbox = temp_draw.textbbox((0, 0), line, font=self.font)
                line_w = bbox[2] - bbox[0]
                line_h = bbox[3] - bbox[1]
                line_dimensions.append((line_w, line_h))
                max_width = max(max_width, line_w)
                total_height += line_h + self.line_spacing

        if lines:
            total_height -= self.line_spacing

        img_width = max(max_width + self.padding * 2, 200)
        img_height = max(total_height + self.padding * 2, 100)

        img = Image.new("RGB", (img_width, img_height), self.bg_color)
        draw = ImageDraw.Draw(img)

        y_offset = self.padding
        for i, line in enumerate(lines):
            if not line:
                y_offset += self.font_size + self.line_spacing
                continue

            line_w, line_h = line_dimensions[i]
            x = (img_width - line_w) // 2
            y = y_offset
            draw.text((x, y), line, font=self.font, fill=self.text_color)
            y_offset += line_h + self.line_spacing

        return img

    def generate_frames(self, text: str, mode: str = "graycode") -> List[Image.Image]:
        """生成所有帧"""
        parts, options = self.parse_text(text)

        if mode == "graycode":
            combinations = self.generate_graycode_combinations(options)
        else:
            combinations = self.generate_random_combinations(options)

        return [self.create_frame(parts, combo) for combo in combinations]

    def save_as_gif(self, frames: List[Image.Image], output_path: str, duration: float = 0.02):
        """保存为 GIF"""
        imageio.mimsave(output_path, frames, duration=duration, loop=0)
        print(f"GIF已生成: {Path(output_path)}")

    def save_as_webp(self, frames: List[Image.Image], output_path: str, duration: int = 33):
        """保存为 WebP"""
        frames[0].save(
            output_path,
            format="WEBP",
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,
            quality=100,
            method=6,
        )
        print(f"WebP已生成: {Path(output_path)}")
