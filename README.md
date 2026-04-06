# GifMaker

[English](README.md) | [简体中文](README.zh-CN.md)

GifMaker is a small Python tool for generating flashing meme animations from text templates.

It supports both a desktop GUI and a CLI, and can export animated `GIF` or `WebP` files from templates such as:

```text
白{神/区}{神/区}了
今天{吃/喝/玩}{火锅/奶茶/原神}
```

Each `{...}` block defines a variable slot, and `/` separates the available options.

## Features

- Template syntax based on `{optionA/optionB/...}`
- `graycode` mode for smooth adjacent-frame transitions
- `random` mode for shuffled full-combination playback
- GIF and WebP export
- GUI desktop app
- CLI workflow for terminal use
- Windows `.exe` packaging via PyInstaller
- GitHub Actions CI and release automation

## Project Structure

```text
.
├─ .github/workflows/  # GitHub Actions CI/CD
├─ src/                # Application source code
├─ docs/               # Design and packaging notes
├─ packaging/          # PyInstaller specs and build scripts
├─ examples/           # Example outputs
├─ legacy/             # Early prototype scripts
└─ tests/              # Automated tests
```

## Quick Start

### Requirements

- Python 3.11 recommended
- Windows for native `.exe` packaging

### Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Run the GUI

```powershell
python .\src\strobe_meme_generator.py
```

### Run the CLI

```powershell
python .\src\strobe_meme_cli.py
```

### Run Tests

```powershell
python -m pytest -q
```

## Packaging

Local build entry points:

- GUI: `.\packaging\build_gui_exe.bat`
- CLI: `.\packaging\build_cli_exe.bat`

Additional packaging notes:

- [docs/打包说明.md](docs/打包说明.md)
- [docs/CLI打包说明.md](docs/CLI打包说明.md)

## CI/CD

This repository includes GitHub Actions workflows for:

- CI on push and pull request
- Windows executable build verification
- Release publishing from version tags such as `v0.1.0`
- Manual release workflow dispatch

## Known Limitations

- The current `graycode` implementation works for practical multi-option cases, but there is still room to improve its more general mixed-radix behavior.
- GIF export is covered by structural tests, but there is not yet a visual golden-file regression suite.

## License

This project is released under the [WTFPL](LICENSE).
