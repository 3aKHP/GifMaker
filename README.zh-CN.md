# GifMaker

[English](README.md) | [简体中文](README.zh-CN.md)

GifMaker 是一个用于从文本模板生成“频闪梗图”动画的小型 Python 工具。

它同时提供 GUI 桌面版和 CLI 命令行版，并支持将如下模板导出为 `GIF` 或 `WebP` 动图：

```text
白{神/区}{神/区}了
今天{吃/喝/玩}{火锅/奶茶/原神}
```

其中 `{...}` 表示一个可变槽位，`/` 用于分隔可选项。

## 功能特性

- 基于 `{选项A/选项B/...}` 的模板语法
- `graycode` 模式，用于更平滑的相邻帧切换
- `random` 模式，用于完整组合集合的随机播放
- 支持导出 `GIF` 和 `WebP`
- 提供 GUI 桌面界面
- 提供 CLI 命令行工作流
- 支持通过 PyInstaller 打包为 Windows `.exe`
- 已配置 GitHub Actions CI 与自动发布流程

## 项目结构

```text
.
├─ .github/workflows/  # GitHub Actions CI/CD
├─ src/                # 应用源码
├─ docs/               # 设计与打包说明
├─ packaging/          # PyInstaller spec 与构建脚本
├─ examples/           # 示例输出
├─ legacy/             # 早期原型脚本
└─ tests/              # 自动化测试
```

## 快速开始

### 环境要求

- 推荐使用 Python 3.11
- 如果需要原生打包 `.exe`，建议在 Windows 上执行

### 安装

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 运行 GUI 版

```powershell
python .\src\strobe_meme_generator.py
```

### 运行 CLI 版

```powershell
python .\src\strobe_meme_cli.py
```

### 运行测试

```powershell
python -m pytest -q
```

## 打包

本地构建入口：

- GUI: `.\packaging\build_exe.bat`
- CLI: `.\packaging\build_cli_exe.bat`

更多打包说明可参考：

- [docs/打包说明.md](docs/打包说明.md)
- [docs/CLI打包说明.md](docs/CLI打包说明.md)

## CI/CD

仓库已包含 GitHub Actions 工作流，用于：

- 在 push 和 pull request 时执行 CI
- 在 Windows runner 上验证可执行文件构建
- 通过 `v0.1.0` 这类版本 tag 自动发布 Release
- 在 Actions 页面手动触发发布流程

## 当前限制

- 当前 `graycode` 实现已经可以覆盖常见多选项场景，但在更一般化的混合进制格雷码行为上仍有继续优化空间。
- GIF 导出目前已有结构性测试覆盖，但还没有建立视觉层面的 golden-file 回归测试。

## License

本项目采用 [WTFPL](LICENSE) 开源。
