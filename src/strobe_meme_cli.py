"""
频闪梗图生成器 - 控制台版本
轻量级命令行工具，支持交互式操作
"""

import os
import re
import subprocess
import sys
from typing import List

from strobe_meme_core import StrobeMemeGenerator


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
