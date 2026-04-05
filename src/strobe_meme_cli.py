"""
频闪梗图生成器 - 控制台版本
轻量级命令行工具，支持交互式操作
"""

from PIL import Image, ImageDraw, ImageFont
import os
import re
import random
from typing import List, Tuple
import imageio
import warnings
import subprocess
import sys

# 忽略libpng的sRGB警告
warnings.filterwarnings('ignore', category=UserWarning, module='PIL')


class StrobeMemeGenerator:
    """频闪梗图生成器核心类"""
    
    def __init__(self):
        self.bg_color = (255, 255, 255)
        self.text_color = (0, 0, 0)
        self.font_size = 100
        self.font = self._load_font()
        self.padding = 40  # 边距
        self.line_spacing = 20  # 行间距
        
    def _load_font(self):
        """加载中文字体"""
        font_paths = [
            "simhei.ttf",
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simsun.ttc",
            "/System/Library/Fonts/PingFang.ttc",
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"
        ]
        
        for path in font_paths:
            if os.path.exists(path):
                try:
                    font = ImageFont.truetype(path, self.font_size)
                    return font
                except Exception:
                    continue
        
        return ImageFont.load_default()
    
    def parse_text(self, text: str) -> Tuple[List[str], List[List[str]]]:
        """
        解析文本，支持 {选项A/选项B} 语法
        返回: (固定字符列表, 变化选项列表)
        """
        parts = []
        options = []
        
        pattern = r'\{([^}]+)\}'
        last_end = 0
        
        for match in re.finditer(pattern, text):
            if match.start() > last_end:
                fixed_text = text[last_end:match.start()]
                for char in fixed_text:
                    parts.append(char)
                    options.append(None)
            
            option_text = match.group(1)
            option_list = [opt.strip() for opt in option_text.split('/')]
            parts.append(None)
            options.append(option_list)
            
            last_end = match.end()
        
        if last_end < len(text):
            for char in text[last_end:]:
                parts.append(char)
                options.append(None)
        
        return parts, options
    
    def generate_graycode_combinations(self, options: List[List[str]]) -> List[List[str]]:
        """生成格雷码顺序的组合（汉明距离=1）"""
        if not any(options):
            return [[]]
        
        variable_positions = [opt for opt in options if opt is not None]
        n = len(variable_positions)
        
        if n == 0:
            return [[]]
        
        def gray_code(n):
            """生成n位格雷码"""
            if n == 0:
                return ['']
            
            prev = gray_code(n - 1)
            result = []
            
            for code in prev:
                result.append('0' + code)
            
            for code in reversed(prev):
                result.append('1' + code)
            
            return result
        
        codes = gray_code(n)
        
        combinations = []
        for code in codes:
            combo = []
            for i, bit in enumerate(code):
                idx = int(bit)
                if idx < len(variable_positions[i]):
                    combo.append(variable_positions[i][idx])
                else:
                    combo.append(variable_positions[i][0])
            combinations.append(combo)
        
        return combinations
    
    def generate_random_combinations(self, options: List[List[str]], count: int = 8) -> List[List[str]]:
        """生成完全随机的组合"""
        variable_positions = [opt for opt in options if opt is not None]
        
        if not variable_positions:
            return [[]]
        
        combinations = []
        for _ in range(count):
            combo = [random.choice(opts) for opts in variable_positions]
            combinations.append(combo)
        
        return combinations
    
    def create_frame(self, parts: List[str], options: List[List[str]],
                    combination: List[str]) -> Image.Image:
        """
        创建单帧图像，支持自适应尺寸和多行文本
        """
        # 构建完整的字符列表
        chars = []
        combo_idx = 0
        for i, part in enumerate(parts):
            if part is None:
                chars.append(combination[combo_idx])
                combo_idx += 1
            else:
                chars.append(part)
        
        # 将字符列表按换行符分割成多行
        text = ''.join(chars)
        lines = text.split('\n')
        
        # 创建临时图像用于测量文本尺寸
        temp_img = Image.new('RGB', (1, 1), self.bg_color)
        temp_draw = ImageDraw.Draw(temp_img)
        
        # 计算每行的宽度和高度
        line_dimensions = []
        max_width = 0
        total_height = 0
        
        for line in lines:
            if not line:  # 空行
                line_dimensions.append((0, self.font_size))
                total_height += self.font_size + self.line_spacing
            else:
                bbox = temp_draw.textbbox((0, 0), line, font=self.font)
                line_w = bbox[2] - bbox[0]
                line_h = bbox[3] - bbox[1]
                line_dimensions.append((line_w, line_h))
                max_width = max(max_width, line_w)
                total_height += line_h + self.line_spacing
        
        # 移除最后一行的行间距
        if lines:
            total_height -= self.line_spacing
        
        # 计算图像尺寸（加上边距）
        img_width = max_width + self.padding * 2
        img_height = total_height + self.padding * 2
        
        # 确保最小尺寸
        img_width = max(img_width, 200)
        img_height = max(img_height, 100)
        
        # 创建实际图像
        img = Image.new('RGB', (img_width, img_height), self.bg_color)
        draw = ImageDraw.Draw(img)
        
        # 绘制每一行
        y_offset = self.padding
        for i, line in enumerate(lines):
            if not line:  # 空行
                y_offset += self.font_size + self.line_spacing
                continue
            
            line_w, line_h = line_dimensions[i]
            
            # 水平居中
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
        
        frames = []
        for combo in combinations:
            frame = self.create_frame(parts, options, combo)
            frames.append(frame)
        
        return frames
    
    def save_as_gif(self, frames: List[Image.Image], output_path: str, duration: float = 0.02):
        """保存为GIF"""
        imageio.mimsave(output_path, frames, duration=duration, loop=0)
    
    def save_as_webp(self, frames: List[Image.Image], output_path: str, duration: int = 33):
        """保存为WebP"""
        frames[0].save(
            output_path,
            format='WEBP',
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,
            quality=100,
            method=6
        )


class ConsoleUI:
    """控制台交互界面"""
    
    def __init__(self):
        self.generator = StrobeMemeGenerator()
        self.text = ""
        self.mode = "graycode"
        self.duration_ms = 33
        self.format = "gif"
        
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """打印标题"""
        print("=" * 60)
        print(" " * 18 + "频闪梗图生成器 - 控制台版")
        print("=" * 60)
        print()
    
    def print_menu(self):
        """打印主菜单"""
        print("当前配置:")
        print(f"  [1] 输入文本: {self.text if self.text else '(未设置)'}")
        print(f"  [2] 闪烁模式: {'格雷码（平滑）' if self.mode == 'graycode' else '完全随机'}")
        print(f"  [3] 帧持续时间: {self.duration_ms} ms")
        print(f"  [4] 导出格式: {self.format.upper()}")
        print()
        print("操作:")
        print("  [G] 生成并保存")
        print("  [Q] 退出")
        print()
    
    def get_input(self, prompt: str, options: List[str] = None) -> str:
        """获取用户输入"""
        if options:
            prompt += f" ({'/'.join(options)}): "
        else:
            prompt += ": "
        
        while True:
            user_input = input(prompt).strip()
            if not options or user_input.upper() in [opt.upper() for opt in options]:
                return user_input
            print(f"无效输入，请输入 {'/'.join(options)}")
    
    def set_text(self):
        """设置输入文本"""
        print("\n" + "-" * 60)
        print("输入文本设置")
        print("-" * 60)
        print("提示: 使用 {选项A/选项B} 语法来定义变化的字符")
        print("示例: 白{神/区}{神/区}了")
        print()
        
        text = input("请输入文本: ").strip()
        if text:
            self.text = text
            print(f"✓ 文本已设置: {self.text}")
        else:
            print("✗ 文本不能为空")
        
        input("\n按回车继续...")
    
    def set_mode(self):
        """设置闪烁模式"""
        print("\n" + "-" * 60)
        print("闪烁模式设置")
        print("-" * 60)
        print("  [1] 格雷码（平滑） - 相邻帧只变化一个字符")
        print("  [2] 完全随机 - 每帧随机选择")
        print()
        
        choice = self.get_input("请选择", ["1", "2"])
        
        if choice == "1":
            self.mode = "graycode"
            print("✓ 已设置为格雷码模式")
        else:
            self.mode = "random"
            print("✓ 已设置为随机模式")
        
        input("\n按回车继续...")
    
    def set_duration(self):
        """设置帧持续时间"""
        print("\n" + "-" * 60)
        print("帧持续时间设置")
        print("-" * 60)
        print("建议值:")
        print("  16 ms  ≈ 60 FPS (流畅)")
        print("  33 ms  ≈ 30 FPS (标准)")
        print("  50 ms  ≈ 20 FPS (较慢)")
        print("  100 ms ≈ 10 FPS (很慢)")
        print()
        
        while True:
            try:
                duration = int(input(f"请输入帧持续时间 (10-200 ms，当前 {self.duration_ms}): ").strip())
                if 10 <= duration <= 200:
                    self.duration_ms = duration
                    print(f"✓ 已设置为 {self.duration_ms} ms")
                    break
                else:
                    print("✗ 请输入 10-200 之间的数值")
            except ValueError:
                print("✗ 请输入有效的数字")
        
        input("\n按回车继续...")
    
    def set_format(self):
        """设置导出格式"""
        print("\n" + "-" * 60)
        print("导出格式设置")
        print("-" * 60)
        print("  [1] GIF  - 兼容性好，文件较大")
        print("  [2] WebP - 文件小，质量高，部分软件不支持")
        print()
        
        choice = self.get_input("请选择", ["1", "2"])
        
        if choice == "1":
            self.format = "gif"
            print("✓ 已设置为 GIF 格式")
        else:
            self.format = "webp"
            print("✓ 已设置为 WebP 格式")
        
        input("\n按回车继续...")
    
    def generate_and_save(self):
        """生成并保存"""
        if not self.text:
            print("\n✗ 错误: 请先设置输入文本")
            input("\n按回车继续...")
            return
        
        print("\n" + "-" * 60)
        print("生成梗图")
        print("-" * 60)
        
        # 生成默认文件名
        safe_text = re.sub(r'[^\w\s-]', '', self.text)[:20]
        default_name = f"{safe_text}_{self.mode}.{self.format}"
        
        print(f"默认文件名: {default_name}")
        filename = input("请输入文件名（直接回车使用默认）: ").strip()
        
        if not filename:
            filename = default_name
        
        # 确保有正确的扩展名
        if not filename.endswith(f".{self.format}"):
            filename += f".{self.format}"
        
        print(f"\n正在生成 {len(self.text)} 个字符的梗图...")
        
        try:
            # 生成帧
            frames = self.generator.generate_frames(self.text, self.mode)
            print(f"✓ 已生成 {len(frames)} 帧")
            
            # 保存文件
            print(f"正在保存为 {self.format.upper()}...")
            
            if self.format == "gif":
                duration_s = self.duration_ms / 1000.0
                self.generator.save_as_gif(frames, filename, duration_s)
            else:
                self.generator.save_as_webp(frames, filename, self.duration_ms)
            
            print(f"✓ 文件已保存: {filename}")
            
            # 询问是否打开文件夹
            open_folder = self.get_input("\n是否打开文件所在文件夹？", ["Y", "N"])
            
            if open_folder.upper() == "Y":
                self.open_file_location(filename)
            
        except Exception as e:
            print(f"\n✗ 生成失败: {str(e)}")
        
        input("\n按回车继续...")
    
    def open_file_location(self, filename: str):
        """打开文件所在位置"""
        try:
            abs_path = os.path.abspath(filename)
            
            if sys.platform == 'win32':
                # Windows: 使用 explorer 并选中文件
                subprocess.run(['explorer', '/select,', abs_path])
            elif sys.platform == 'darwin':
                # macOS: 使用 Finder
                subprocess.run(['open', '-R', abs_path])
            else:
                # Linux: 打开文件所在目录
                folder = os.path.dirname(abs_path)
                subprocess.run(['xdg-open', folder])
            
            print("✓ 已打开文件位置")
        except Exception as e:
            print(f"✗ 无法打开文件位置: {str(e)}")
    
    def run(self):
        """运行主循环"""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_menu()
            
            choice = self.get_input("请选择操作", ["1", "2", "3", "4", "G", "Q"]).upper()
            
            if choice == "1":
                self.set_text()
            elif choice == "2":
                self.set_mode()
            elif choice == "3":
                self.set_duration()
            elif choice == "4":
                self.set_format()
            elif choice == "G":
                self.generate_and_save()
            elif choice == "Q":
                print("\n再见！")
                break


def main():
    """主函数"""
    try:
        ui = ConsoleUI()
        ui.run()
    except KeyboardInterrupt:
        print("\n\n程序已中断")
    except Exception as e:
        print(f"\n发生错误: {str(e)}")
        input("\n按回车退出...")


if __name__ == "__main__":
    main()
