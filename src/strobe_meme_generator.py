"""
频闪梗图生成器 - GUI版本
支持自定义文本、格雷码/随机闪烁算法、GIF/WebP导出
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont
import os
import re
import random
from typing import List, Tuple
import imageio
import warnings

# 忽略libpng的sRGB警告
warnings.filterwarnings('ignore', category=UserWarning, module='PIL')

# Windows高DPI适配
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


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
                    print(f"成功加载字体: {path}")
                    return font
                except Exception:
                    continue
        
        print("未找到指定字体，使用默认字体")
        return ImageFont.load_default()
    
    def parse_text(self, text: str) -> Tuple[List[str], List[List[str]]]:
        """
        解析文本，支持 {选项A/选项B} 语法
        返回: (固定字符列表, 变化选项列表)
        
        例如: "白{神/区}{神/区}了" -> (["白", None, None, "了"], [["神", "区"], ["神", "区"]])
        """
        parts = []
        options = []
        
        # 使用正则表达式解析
        pattern = r'\{([^}]+)\}'
        last_end = 0
        
        for match in re.finditer(pattern, text):
            # 添加匹配前的固定文本
            if match.start() > last_end:
                fixed_text = text[last_end:match.start()]
                for char in fixed_text:
                    parts.append(char)
                    options.append(None)
            
            # 添加变化选项
            option_text = match.group(1)
            option_list = [opt.strip() for opt in option_text.split('/')]
            parts.append(None)
            options.append(option_list)
            
            last_end = match.end()
        
        # 添加剩余的固定文本
        if last_end < len(text):
            for char in text[last_end:]:
                parts.append(char)
                options.append(None)
        
        return parts, options
    
    def generate_graycode_combinations(self, options: List[List[str]]) -> List[List[str]]:
        """
        生成格雷码顺序的组合（汉明距离=1）
        确保相邻帧之间只有一个位置的字符发生变化
        """
        if not any(options):
            return [[]]
        
        # 计算有多少个变化位置
        variable_positions = [opt for opt in options if opt is not None]
        n = len(variable_positions)
        
        if n == 0:
            return [[]]
        
        # 生成格雷码序列
        def gray_code(n):
            """生成n位格雷码"""
            if n == 0:
                return ['']
            
            # 递归生成
            prev = gray_code(n - 1)
            result = []
            
            # 前半部分：在前面加0
            for code in prev:
                result.append('0' + code)
            
            # 后半部分：在前面加1，并反转顺序
            for code in reversed(prev):
                result.append('1' + code)
            
            return result
        
        # 生成格雷码
        codes = gray_code(n)
        
        # 将格雷码转换为实际的字符组合
        combinations = []
        for code in codes:
            combo = []
            for i, bit in enumerate(code):
                idx = int(bit)
                # 确保索引不越界
                if idx < len(variable_positions[i]):
                    combo.append(variable_positions[i][idx])
                else:
                    combo.append(variable_positions[i][0])
            combinations.append(combo)
        
        return combinations
    
    def generate_random_combinations(self, options: List[List[str]], count: int = 8) -> List[List[str]]:
        """
        生成完全随机的组合
        """
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
        """
        生成所有帧
        mode: "graycode" 或 "random"
        """
        parts, options = self.parse_text(text)
        
        # 生成组合
        if mode == "graycode":
            combinations = self.generate_graycode_combinations(options)
        else:
            combinations = self.generate_random_combinations(options)
        
        # 生成帧
        frames = []
        for combo in combinations:
            frame = self.create_frame(parts, options, combo)
            frames.append(frame)
        
        return frames
    
    def save_as_gif(self, frames: List[Image.Image], output_path: str, duration: float = 0.02):
        """保存为GIF"""
        imageio.mimsave(output_path, frames, duration=duration, loop=0)
        print(f"GIF已生成: {output_path}")
    
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
        print(f"WebP已生成: {output_path}")


class StrobeMemeGUI:
    """GUI界面类"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("频闪梗图生成器")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        self.generator = StrobeMemeGenerator()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """创建GUI组件"""
        # 标题
        title_label = tk.Label(
            self.root,
            text="频闪梗图生成器",
            font=("微软雅黑", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # 说明文本
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=5, padx=20, fill=tk.X)
        
        info_text = tk.Label(
            info_frame,
            text="使用 {选项A/选项B} 语法来定义变化的字符\n例如: 白{神/区}{神/区}了",
            font=("微软雅黑", 9),
            fg="gray",
            justify=tk.LEFT
        )
        info_text.pack(anchor=tk.W)
        
        # 输入文本框
        input_frame = tk.LabelFrame(self.root, text="输入文本", font=("微软雅黑", 10))
        input_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.text_input = tk.Text(input_frame, height=3, font=("微软雅黑", 12))
        self.text_input.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.text_input.insert("1.0", "白{神/区}{神/区}了")
        
        # 参数设置框
        params_frame = tk.LabelFrame(self.root, text="参数设置", font=("微软雅黑", 10))
        params_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # 闪烁模式
        mode_frame = tk.Frame(params_frame)
        mode_frame.pack(pady=5, padx=10, fill=tk.X)
        
        tk.Label(mode_frame, text="闪烁模式:", font=("微软雅黑", 9)).pack(side=tk.LEFT, padx=5)
        
        self.mode_var = tk.StringVar(value="graycode")
        mode_radio1 = tk.Radiobutton(
            mode_frame,
            text="格雷码（平滑）",
            variable=self.mode_var,
            value="graycode",
            font=("微软雅黑", 9)
        )
        mode_radio1.pack(side=tk.LEFT, padx=5)
        
        mode_radio2 = tk.Radiobutton(
            mode_frame,
            text="完全随机",
            variable=self.mode_var,
            value="random",
            font=("微软雅黑", 9)
        )
        mode_radio2.pack(side=tk.LEFT, padx=5)
        
        # 帧持续时间
        duration_frame = tk.Frame(params_frame)
        duration_frame.pack(pady=5, padx=10, fill=tk.X)
        
        tk.Label(duration_frame, text="帧持续时间:", font=("微软雅黑", 9)).pack(side=tk.LEFT, padx=5)
        
        self.duration_var = tk.IntVar(value=33)
        duration_spinbox = tk.Spinbox(
            duration_frame,
            from_=10,
            to=200,
            textvariable=self.duration_var,
            width=10,
            font=("微软雅黑", 9)
        )
        duration_spinbox.pack(side=tk.LEFT, padx=5)
        
        tk.Label(duration_frame, text="毫秒 (ms)", font=("微软雅黑", 9)).pack(side=tk.LEFT, padx=5)
        
        # 按钮框
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20, padx=20, fill=tk.X)
        
        # 预览按钮
        preview_btn = tk.Button(
            button_frame,
            text="预览效果",
            command=self.preview,
            font=("微软雅黑", 10),
            bg="#4CAF50",
            fg="white",
            width=12,
            height=2
        )
        preview_btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        # 导出GIF按钮
        gif_btn = tk.Button(
            button_frame,
            text="导出 GIF",
            command=self.export_gif,
            font=("微软雅黑", 10),
            bg="#2196F3",
            fg="white",
            width=12,
            height=2
        )
        gif_btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        # 导出WebP按钮
        webp_btn = tk.Button(
            button_frame,
            text="导出 WebP",
            command=self.export_webp,
            font=("微软雅黑", 10),
            bg="#FF9800",
            fg="white",
            width=12,
            height=2
        )
        webp_btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        # 状态栏
        self.status_label = tk.Label(
            self.root,
            text="就绪",
            font=("微软雅黑", 9),
            fg="gray",
            anchor=tk.W
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)
    
    def preview(self):
        """预览效果"""
        try:
            text = self.text_input.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("警告", "请输入文本")
                return
            
            mode = self.mode_var.get()
            duration_ms = self.duration_var.get()
            
            self.status_label.config(text="正在生成预览...")
            self.root.update()
            
            frames = self.generator.generate_frames(text, mode)
            
            if not frames:
                messagebox.showerror("错误", "无法生成帧")
                self.status_label.config(text="生成失败")
                return
            
            # 创建动画预览窗口
            preview_window = tk.Toplevel(self.root)
            preview_window.title("预览 - 动画播放中")
            preview_window.geometry("520x280")
            preview_window.resizable(False, False)
            
            # 转换所有帧为PhotoImage
            from PIL import ImageTk
            photo_frames = [ImageTk.PhotoImage(frame) for frame in frames]
            
            # 创建显示标签
            label = tk.Label(preview_window)
            label.pack(pady=10)
            
            # 信息标签
            info = tk.Label(
                preview_window,
                text=f"共生成 {len(frames)} 帧 | 模式: {'格雷码' if mode == 'graycode' else '随机'} | 帧率: {duration_ms}ms",
                font=("微软雅黑", 10)
            )
            info.pack(pady=5)
            
            # 控制按钮
            control_frame = tk.Frame(preview_window)
            control_frame.pack(pady=5)
            
            is_playing = [True]  # 使用列表以便在闭包中修改
            current_frame = [0]
            
            def toggle_play():
                is_playing[0] = not is_playing[0]
                play_btn.config(text="暂停" if is_playing[0] else "播放")
            
            play_btn = tk.Button(
                control_frame,
                text="暂停",
                command=toggle_play,
                font=("微软雅黑", 9),
                width=8
            )
            play_btn.pack(side=tk.LEFT, padx=5)
            
            close_btn = tk.Button(
                control_frame,
                text="关闭",
                command=preview_window.destroy,
                font=("微软雅黑", 9),
                width=8
            )
            close_btn.pack(side=tk.LEFT, padx=5)
            
            # 动画循环
            def animate():
                if not preview_window.winfo_exists():
                    return
                
                if is_playing[0]:
                    label.config(image=photo_frames[current_frame[0]])
                    current_frame[0] = (current_frame[0] + 1) % len(photo_frames)
                
                preview_window.after(duration_ms, animate)
            
            # 开始动画
            animate()
            
            self.status_label.config(text=f"预览完成 - 共 {len(frames)} 帧")
            
        except Exception as e:
            messagebox.showerror("错误", f"预览失败: {str(e)}")
            self.status_label.config(text="预览失败")
    
    def export_gif(self):
        """导出GIF"""
        try:
            text = self.text_input.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("警告", "请输入文本")
                return
            
            # 选择保存路径
            file_path = filedialog.asksaveasfilename(
                defaultextension=".gif",
                filetypes=[("GIF文件", "*.gif"), ("所有文件", "*.*")]
            )
            
            if not file_path:
                return
            
            mode = self.mode_var.get()
            duration_ms = self.duration_var.get()
            duration_s = duration_ms / 1000.0
            
            self.status_label.config(text="正在生成GIF...")
            self.root.update()
            
            frames = self.generator.generate_frames(text, mode)
            self.generator.save_as_gif(frames, file_path, duration_s)
            
            self.status_label.config(text=f"GIF已保存: {file_path}")
            messagebox.showinfo("成功", f"GIF已保存到:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")
            self.status_label.config(text="导出失败")
    
    def export_webp(self):
        """导出WebP"""
        try:
            text = self.text_input.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("警告", "请输入文本")
                return
            
            # 选择保存路径
            file_path = filedialog.asksaveasfilename(
                defaultextension=".webp",
                filetypes=[("WebP文件", "*.webp"), ("所有文件", "*.*")]
            )
            
            if not file_path:
                return
            
            mode = self.mode_var.get()
            duration_ms = self.duration_var.get()
            
            self.status_label.config(text="正在生成WebP...")
            self.root.update()
            
            frames = self.generator.generate_frames(text, mode)
            self.generator.save_as_webp(frames, file_path, duration_ms)
            
            self.status_label.config(text=f"WebP已保存: {file_path}")
            messagebox.showinfo("成功", f"WebP已保存到:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")
            self.status_label.config(text="导出失败")


def main():
    """主函数"""
    root = tk.Tk()
    app = StrobeMemeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
