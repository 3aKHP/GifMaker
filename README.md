# GifMaker

一个用于生成“频闪梗图”的 Python 小工具，当前同时提供 GUI 版和 CLI 版入口。

## 仓库结构

```text
.
├─ src/            # 主程序源码
├─ docs/           # 设计与打包说明
├─ packaging/      # PyInstaller spec 与打包脚本
├─ examples/       # 样例输出
├─ legacy/         # 早期原型脚本
├─ build/          # 打包中间产物（已忽略）
└─ dist/           # 打包产物（已忽略）
```

## 快速开始

1. 安装依赖

```powershell
python -m pip install -r requirements.txt
```

2. 运行 GUI 版

```powershell
python .\src\strobe_meme_generator.py
```

3. 运行 CLI 版

```powershell
python .\src\strobe_meme_cli.py
```

## 打包

- GUI: `.\packaging\build_exe.bat`
- CLI: `.\packaging\build_cli_exe.bat`

更详细的说明见 [docs/打包说明.md](docs/打包说明.md) 和 [docs/CLI打包说明.md](docs/CLI打包说明.md)。

## CI/CD

- CI: GitHub Actions 会在推送到 `main/master` 或发起 PR 时自动创建 `.venv`、安装依赖、运行测试，并在 Windows runner 上验证 GUI/CLI 打包。
- CD: 当推送形如 `v0.1.0` 的 tag 时，GitHub Actions 会自动构建两个 `.exe` 并创建对应的 GitHub Release。
- 也可以在 GitHub Actions 页面手动触发 `Release` workflow，并填写一个 `release_tag` 来生成或更新 Release。

常用发布流程：

```powershell
git tag v0.1.0
git push origin v0.1.0
```

## 快速审阅结论

- 项目已经具备完整的 GUI/CLI 主流程、导出 GIF/WebP 和 PyInstaller 打包脚本。
- 原仓库把源码、文档、样例、`build/`、`dist/` 混放在根目录，不利于后续维护；本次已按职责拆分。
- 当前实现还有两个值得后续优先处理的逻辑点：
  - `graycode` 生成逻辑本质上只覆盖了二值位切换，对设计文档里提到的多选项广义格雷码支持还不完整。
  - `random` 模式是“按帧随机抽样”，不是“完整组合集合打乱后逐个播放”，因此不能保证一个周期内等概率且不重复。

## 后续建议

- 给核心生成逻辑补最小化测试，至少覆盖模板解析、随机模式组合数、格雷码相邻汉明距离。
- 如果准备长期维护，建议把 GUI/CLI 共享逻辑再抽到独立模块，减少重复代码。
