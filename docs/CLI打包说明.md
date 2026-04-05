# 频闪梗图生成器（控制台版）- 打包说明

## 控制台版本特点

- ✅ 轻量级，无GUI依赖
- ✅ 纯命令行交互
- ✅ 选项式菜单操作
- ✅ 支持保存后打开文件夹
- ✅ 文件体积更小
- ✅ 适合服务器环境或批处理

## 方法一：使用批处理脚本（推荐）

直接双击运行 `build_cli_exe.bat`，脚本会自动完成所有步骤。
当前仓库结构下，脚本路径为 `packaging/build_cli_exe.bat`。

## 方法二：手动打包

### 1. 安装PyInstaller

```bash
pip install pyinstaller
```

### 2. 基础打包命令

```bash
pyinstaller --onefile --console --name "频闪梗图生成器-CLI" src/strobe_meme_cli.py
```

### 3. 高级打包命令（包含字体）

```bash
pyinstaller --noconfirm ^
    --onefile ^
    --console ^
    --name "频闪梗图生成器-CLI" ^
    --add-data "C:/Windows/Fonts/simhei.ttf;." ^
    --hidden-import=PIL._tkinter_finder ^
    src/strobe_meme_cli.py
```

### 4. 参数说明

- `--onefile`: 打包成单个exe文件
- `--console`: 显示控制台窗口（控制台程序必需）
- `--name`: 指定exe文件名
- `--add-data`: 添加额外文件（字体）
- `--hidden-import`: 添加隐藏导入

### 5. 输出位置

打包完成后，exe文件位于 `dist` 目录下。

## GUI版本 vs 控制台版本对比

| 特性 | GUI版本 | 控制台版本 |
|------|---------|-----------|
| 界面 | 图形界面 | 命令行界面 |
| 依赖 | Tkinter | 无GUI依赖 |
| 文件大小 | 较大 | 较小 |
| 预览功能 | ✅ 动画预览 | ❌ 无预览 |
| 交互方式 | 鼠标点击 | 键盘输入 |
| 适用场景 | 桌面使用 | 服务器/批处理 |
| 启动参数 | `--windowed` | `--console` |

## 使用方法

### 运行Python脚本

```bash
python src/strobe_meme_cli.py
```

### 运行打包后的exe

```bash
频闪梗图生成器-CLI.exe
```

或直接双击exe文件。

## 操作流程

1. **设置文本** - 输入要生成的文本，支持 `{选项A/选项B}` 语法
2. **选择模式** - 格雷码（平滑）或完全随机
3. **设置参数** - 帧持续时间和导出格式
4. **生成保存** - 生成梗图并保存到文件
5. **打开文件夹** - 可选择自动打开文件所在位置

## 示例操作

```
============================================================
                  频闪梗图生成器 - 控制台版
============================================================

当前配置:
  [1] 输入文本: 白{神/区}{神/区}了
  [2] 闪烁模式: 格雷码（平滑）
  [3] 帧持续时间: 33 ms
  [4] 导出格式: GIF

操作:
  [G] 生成并保存
  [Q] 退出

请选择操作 (1/2/3/4/G/Q): G
```

## 常见问题

### Q1: 控制台窗口一闪而过

**原因**: 程序执行完毕后自动关闭

**解决方案**: 
1. 在命令提示符中运行exe
2. 或者在打包时确保使用了 `--console` 参数
3. 程序内部已添加 `input()` 等待用户输入

### Q2: 中文显示乱码

**原因**: 控制台编码问题

**解决方案**:
```bash
# 在运行前执行
chcp 65001
```

或在代码中添加：
```python
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

### Q3: 无法打开文件夹

**原因**: 系统权限或路径问题

**解决方案**: 
- 确保文件已成功保存
- 检查文件路径是否正确
- 手动导航到文件位置

### Q4: 打包后文件太大

**解决方案**:
1. 使用虚拟环境，只安装必要的包：
```bash
conda create -n cli_meme python=3.10
conda activate cli_meme
pip install pillow imageio
```

2. 排除不需要的模块：
```bash
--exclude-module tkinter
--exclude-module matplotlib
```

## 批处理脚本示例

创建 `generate.bat` 用于批量生成：

```batch
@echo off
echo 正在生成梗图...
频闪梗图生成器-CLI.exe
echo 完成！
pause
```

## 高级用法：命令行参数（可扩展）

如果需要支持命令行参数，可以修改 `src/strobe_meme_cli.py` 添加 `argparse`：

```python
import argparse

parser = argparse.ArgumentParser(description='频闪梗图生成器')
parser.add_argument('--text', help='输入文本')
parser.add_argument('--mode', choices=['graycode', 'random'], help='闪烁模式')
parser.add_argument('--duration', type=int, help='帧持续时间(ms)')
parser.add_argument('--format', choices=['gif', 'webp'], help='导出格式')
parser.add_argument('--output', help='输出文件名')
args = parser.parse_args()
```

然后可以这样使用：

```bash
频闪梗图生成器-CLI.exe --text "白{神/区}{神/区}了" --mode graycode --format gif --output output.gif
```

## 性能优化

### 1. 减小文件大小

```bash
# 使用UPX压缩
pip install pyinstaller[encryption]
pyinstaller --upx-dir=upx路径 ...
```

### 2. 加快启动速度

控制台版本已经比GUI版本快很多，因为：
- 无需加载Tkinter
- 无需初始化GUI组件
- 启动时间更短

### 3. 内存优化

控制台版本内存占用更小：
- 无GUI组件占用
- 无图像预览缓存
- 按需生成帧

## 部署建议

### 1. 单文件部署

使用 `--onefile` 模式，只需分发一个exe文件。

### 2. 服务器部署

控制台版本特别适合服务器环境：
```bash
# Linux服务器上运行
python strobe_meme_cli.py
```

### 3. 批处理任务

可以集成到批处理脚本中：
```batch
@echo off
for %%f in (*.txt) do (
    频闪梗图生成器-CLI.exe --text "%%f"
)
```

## 系统要求

- Windows 7 及以上（Windows）
- Python 3.7+ 或打包后的exe
- 无需安装Python环境（使用exe时）
- 无需GUI环境

## 对比总结

**选择GUI版本** (`src/strobe_meme_generator.py`) 如果你需要：
- 图形界面操作
- 实时预览效果
- 更直观的交互

**选择控制台版本** (`src/strobe_meme_cli.py`) 如果你需要：
- 轻量级工具
- 服务器环境运行
- 批处理集成
- 更小的文件体积
- 更快的启动速度

## 许可证

根据你的项目需求添加相应的许可证信息。
