# WinGameOptimizer

Windows 10/11 Gaming & Productivity Environment Optimization Tool

适用于 Windows 10 / Windows 11 的游戏与生产力环境一键检查和优化工具。

支持 NVIDIA / AMD / Intel 显卡。

---

## Overview | 项目简介

WinGameOptimizer is a lightweight Windows optimization utility designed to help users quickly diagnose common gaming environment issues and apply recommended performance optimizations.

The project aims to simplify Windows gaming setup by providing an easy-to-use graphical interface that combines diagnostics, performance tuning, and environment preparation into a single application.

WinGameOptimizer 是一个轻量级 Windows 游戏环境优化工具，旨在帮助用户快速发现常见系统问题，并一键应用推荐优化方案。

项目目标是在保持系统稳定性的前提下，为游戏玩家和生产力用户提供简单、高效、可视化的优化体验。

---

## Features | 功能特性

### Diagnose（系统诊断）

* Windows 版本检测
* CPU / Memory 信息检测
* 电源计划状态检测
* GPU 检测（NVIDIA / AMD / Intel）
* HAGS 状态检测
* 磁盘空间检测
* VC++ Runtime 检测
* .NET Runtime 检测
* 系统服务状态检测
* 网络连通性与延迟检测
* 导出诊断报告（TXT）

### Optimize（系统优化）

每项优化均可单独启用或关闭：

| Optimization             | Description       |
| ------------------------ | ----------------- |
| Power Plan               | 启用卓越性能/高性能电源计划    |
| Xbox Game Bar            | 禁用 Xbox Game Bar  |
| HAGS                     | 开启硬件加速 GPU 调度     |
| Fullscreen Optimizations | 禁用全屏优化            |
| Mouse Acceleration       | 关闭鼠标加速            |
| Visual Effects           | 调整为最佳性能           |
| SysMain                  | SSD 环境下禁用 SysMain |
| TCP Network              | 优化网络延迟            |
| Page File                | 固定虚拟内存为 8192MB    |

---

## Download | 下载

Latest stable release:

https://github.com/SautaNOTSanta/WinGameOptimizer/releases

下载最新版：

1. 打开 Releases 页面
2. 下载 `GameEnvSetup.exe`
3. 右键 → 以管理员身份运行

---

## Usage | 使用方法

### For End Users | 普通用户

1. 运行 `GameEnvSetup.exe`
2. 切换到 **Diagnose**
3. 点击 **Run Diagnostics**
4. 查看标记为 `[!!]` 的项目
5. 切换到 **Optimize**
6. 勾选需要应用的优化项
7. 点击 **Apply Selected**
8. 重启 Windows

---

## Development | 开发环境

### Requirements

* Python 3.8+
* tkinter（Python 内置）

### Run from Source

```bash
python main.py
```

---

## Build EXE

Install PyInstaller:

```bash
pip install pyinstaller
```

Build:

```bash
python build.py
```

Output:

```text
dist/GameEnvSetup.exe
```

Single executable file.

Typical size:

```text
10 ~ 15 MB
```

---

## Project Structure

```text
WinGameOptimizer/
│
├── main.py
├── build.py
├── dist/
│   └── GameEnvSetup.exe
│
├── README.md
└── LICENSE
```

### File Description

| File             | Description                  |
| ---------------- | ---------------------------- |
| main.py          | Main application source code |
| build.py         | Build script for PyInstaller |
| GameEnvSetup.exe | Compiled executable          |

---

## Screenshots

You may add screenshots here:

```text
docs/screenshots/
```

Example:

* Main Window
* Diagnostics Page
* Optimization Page
* Generated Report

---

## Release Notes

### v1.0.0

Initial public release.

Features included:

* Hardware diagnostics
* Gaming environment diagnostics
* Windows optimization toolkit
* NVIDIA / AMD / Intel support
* TXT report export
* GUI interface

---

## Important Notes | 注意事项

* 优化操作需要管理员权限
* 诊断功能可在普通权限下运行
* 部分系统项目可能无法读取
* 建议优化完成后重启系统
* HAGS 修改需要重启生效
* Page File 修改需要重启生效

---

## Disclaimer | 免责声明

This software modifies Windows system settings to improve gaming performance and user experience.

Although the project has been tested on multiple Windows systems, users should understand the changes being applied before use.

The author is not responsible for any data loss, system instability, or other issues resulting from improper usage.

本软件会对 Windows 系统配置进行调整以改善游戏体验。

尽管开发过程中已经尽可能保证安全性与稳定性，但用户仍应在了解相关修改内容的前提下使用本工具。

因使用本软件造成的数据丢失、系统异常或其他问题，开发者不承担责任。

---

## License

MIT License

---

Made with Python, Tkinter and a considerable amount of Vibe Coding.
