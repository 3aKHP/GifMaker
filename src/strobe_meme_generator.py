"""
频闪梗图生成器 - GUI版本
支持自定义文本、格雷码/随机闪烁算法、GIF/WebP导出
"""

import tkinter as tk
from tkinter import filedialog, messagebox

from strobe_meme_core import StrobeMemeGenerator

# Windows高DPI适配
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


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
