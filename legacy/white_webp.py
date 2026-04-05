from PIL import Image, ImageDraw, ImageFont
import os

# --- 配置参数 ---
width, height = 500, 200
bg_color = (255, 255, 255)
text_color = (0, 0, 0)
font_size = 100

# 【关键设置】每帧持续时间（毫秒）
# 16ms ≈ 60帧/秒 (大多数显示器的刷新率上限)
# 10ms = 100帧/秒 (极速，浏览器可能渲染不过来，或者看起来像重影)
duration_ms = 33 

# --- 字体加载逻辑 ---
font_paths = [
    "simhei.ttf",                   
    "C:/Windows/Fonts/simhei.ttf",  
    "C:/Windows/Fonts/msyh.ttc",    
    "C:/Windows/Fonts/simsun.ttc",  
    "/System/Library/Fonts/PingFang.ttc", 
    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf" 
]

font = None
for path in font_paths:
    if os.path.exists(path):
        try:
            font = ImageFont.truetype(path, font_size)
            print(f"成功加载字体: {path}")
            break
        except Exception:
            continue

if font is None:
    print("未找到指定字体，使用默认字体")
    font = ImageFont.load_default()

# --- 格雷码顺序 (00 -> 01 -> 11 -> 10) ---
combinations = [
    ("神", "神"), 
    ("神", "区"), 
    ("区", "区"), 
    ("区", "神")  
]

frames = []
positions = [60, 160, 260, 360] 

# 生成帧
for char2, char3 in combinations:
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    chars = ["白", char2, char3, "了"]
    
    for i, char in enumerate(chars):
        # 居中计算
        bbox = draw.textbbox((0, 0), char, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        x = positions[i]
        y = (height - text_h) // 2 - 10 
        
        draw.text((x, y), char, font=font, fill=text_color)
    
    frames.append(img)

# --- 保存为 WebP ---
output_path = "bai_shen_qu_le_graycode.webp"

# 注意：
# 1. save_all=True 表示保存所有帧
# 2. append_images 放入后续帧
# 3. duration 单位是 毫秒(ms)
# 4. loop=0 表示无限循环
frames[0].save(
    output_path, 
    format='WEBP', 
    save_all=True, 
    append_images=frames[1:], 
    duration=duration_ms, 
    loop=0,
    quality=100, # 无损质量
    method=6     # 压缩方法（6最慢但质量最好，对于这种简单图很快）
)

print(f"WebP 已生成: {output_path} (每帧 {duration_ms}ms)")
