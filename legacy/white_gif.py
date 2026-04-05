from PIL import Image, ImageDraw, ImageFont
import imageio

# 配置参数
width, height = 500, 200  # 图片尺寸
bg_color = (255, 255, 255) # 白底
text_color = (0, 0, 0)     # 黑字
font_size = 100
duration = 0.02  # 每帧持续时间(秒)，越小越快

# 尝试加载字体，如果没有SimHei则使用默认
font = None
# 常见中文字体路径列表
font_paths = [
    "simhei.ttf",                   # 尝试直接加载（如果已安装或在当前目录）
    "C:/Windows/Fonts/simhei.ttf",  # Windows 黑体
    "C:/Windows/Fonts/msyh.ttc",    # Windows 微软雅黑
    "C:/Windows/Fonts/simsun.ttc",  # Windows 宋体
    "/System/Library/Fonts/PingFang.ttc", # macOS 苹方
    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf" # Linux
]

for path in font_paths:
    try:
        font = ImageFont.truetype(path, font_size)
        print(f"成功加载字体: {path}")
        break
    except Exception:
        continue

if font is None:
    print("警告：未找到支持的中文字体，将使用默认字体（可能无法显示中文）")
    font = ImageFont.load_default()

# 定义四种组合（使用格雷码顺序：00->01->11->10，确保每次只变一个字）
# 假设：神=0, 区=1
combinations = [
    ("神", "神"), # 00
    ("神", "区"), # 01
    ("区", "区"), # 11
    ("区", "神")  # 10
]

frames = []

# 固定每个字的X轴中心位置，确保"白"和"了"不抖动
# 假设画布宽500，4个字，字号100。
# 为了居中显示，每个字中心点位置：
positions = [100, 200, 300, 400]

for char2, char3 in combinations:
    # 创建白底画布
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # 构建当前帧的字符列表
    chars = ["白", char2, char3, "了"]
    
    # 逐个绘制字符
    for i, char in enumerate(chars):
        # 获取文字大小以精确居中
        bbox = draw.textbbox((0, 0), char, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        # 使用中心位置减去文字宽度的一半来实现居中
        x = positions[i] - text_w // 2
        y = (height - text_h) // 2 - 10 # 微调Y轴
        
        draw.text((x, y), char, font=font, fill=text_color)
    
    frames.append(img)

# 保存为GIF
output_path = "bai_shen_qu_le.gif"
imageio.mimsave(output_path, frames, duration=duration, loop=0)

print(f"GIF已生成: {output_path}")
