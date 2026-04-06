# GifMaker

`GifMaker` 是一个用于生成“频闪梗图”的 Python 小工具，当前提供：

- GUI 桌面版
- CLI 命令行版
- GIF / WebP 导出
- GitHub Actions 自动测试与 Windows `.exe` 发布流程

它适合生成这类模板文本：

```text
白{神/区}{神/区}了
今天{吃/喝/玩}{火锅/奶茶/原神}
```

程序会解析花括号中的选项，生成所有组合，并按指定顺序输出为动画图片。

## 功能特性

- 支持 `{选项A/选项B}` 模板语法
- 支持 `graycode` 平滑切换模式
- 支持 `random` 全组合随机播放模式
- 支持导出为 `GIF` 和 `WebP`
- 提供图形界面与控制台两种入口
- 支持 PyInstaller 打包为独立 Windows 可执行文件

## 仓库结构

```text
.
├─ .github/workflows/  # GitHub Actions CI/CD
├─ src/                # 主程序源码
├─ docs/               # 设计与打包说明
├─ packaging/          # PyInstaller spec 与打包脚本
├─ examples/           # 样例输出
├─ legacy/             # 早期原型脚本
├─ tests/              # 自动化测试
├─ build/              # 打包中间产物（已忽略）
└─ dist/               # 打包产物（已忽略）
```

## 快速开始

### 1. 创建虚拟环境

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 2. 运行 GUI 版

```powershell
python .\src\strobe_meme_generator.py
```

### 3. 运行 CLI 版

```powershell
python .\src\strobe_meme_cli.py
```

### 4. 运行测试

```powershell
python -m pytest -q
```

## 打包

本地打包：

- GUI: `.\packaging\build_exe.bat`
- CLI: `.\packaging\build_cli_exe.bat`

更详细的说明见：

- [docs/打包说明.md](docs/打包说明.md)
- [docs/CLI打包说明.md](docs/CLI打包说明.md)

## CI/CD

仓库已预置 GitHub Actions：

- CI: 在推送到 `main/master` 或发起 PR 时自动创建 `.venv`、安装依赖、运行测试，并在 Windows runner 上验证 GUI/CLI 打包
- CD: 在推送形如 `v0.1.0` 的 tag 时自动构建两个 `.exe` 并创建 GitHub Release
- Manual Release: 也可以在 Actions 页面手动触发 `Release` workflow，并填写 `release_tag`

常用发布流程：

```powershell
git tag v0.1.0
git push origin v0.1.0
```

## 当前已知限制

- `graycode` 当前实现对多选项场景可用，但和设计文档里“更广义的格雷码扩展”相比仍有继续打磨空间
- GIF 导出已切换为 Pillow，当前测试覆盖了帧数和时长，但还没有做视觉一致性的 golden-file 回归测试

## 发布到 GitHub 的建议

如果你准备把这个仓库发布到 GitHub 用户 `3aKHP` 名下，推荐的仓库名可以是：

- `GifMaker`
- `strobe-meme-generator`

首次关联远端后可使用：

```powershell
git remote add origin https://github.com/3aKHP/GifMaker.git
git push -u origin main
```

## License

本项目使用 [WTFPL](LICENSE)。
