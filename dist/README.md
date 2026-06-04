<div align="center">

# WinGameOptimizer

**Windows 10/11 游戏与生产力环境 一键检测 + 优化工具**

**One-click Game & Productivity Environment Checker + Optimizer for Windows 10/11**

![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-blue?style=flat-square)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![GUI](https://img.shields.io/badge/GUI-tkinter-lightgrey?style=flat-square)

</div>

---

## 简介 / Introduction

**WinGameOptimizer** 是一个面向 Windows 10/11 用户的系统环境诊断与优化工具。  
无需手动翻设置，一键扫描系统状态，逐项勾选应用优化，打包为单文件 EXE，任何人开箱即用。

**WinGameOptimizer** is a system diagnostics and optimization tool for Windows 10/11 gamers and power users.  
No manual registry digging — scan your system, pick your tweaks, apply with one click. Ships as a single portable EXE.

---

## 功能 / Features

### 🔍 Diagnose（诊断）

| 检测项 / Check | 说明 / Detail |
|---|---|
| 系统版本 / OS Version | Windows 版本与构建号 |
| 内存 / RAM | 总量与可用量 |
| CPU | 型号、核心数、当前电源计划 |
| GPU | 自动识别 NVIDIA / AMD / Intel，驱动版本，HAGS 状态 |
| 存储 / Storage | 各分区空余空间，低于 15% 警告，低于 10% 严重警告 |
| 运行库 / Runtimes | VC++ 2015-2022、.NET Framework、DirectX |
| 系统服务 / Services | Windows Audio、防火墙等关键服务 |
| 网络 / Network | 活跃网卡、外网延迟 |

### ⚙️ Optimize（优化）

每项可单独勾选，不强制全选。

| # | 优化项 / Tweak | 效果 / Effect |
|---|---|---|
| 1 | 电源计划 Power Plan | 激活卓越性能 / Ultimate Performance |
| 2 | Xbox Game Bar | 禁用，释放后台资源 |
| 3 | HAGS | 硬件加速 GPU 调度，降低输入延迟 |
| 4 | 全屏优化 Fullscreen Opt. | 全局禁用，减少帧率抖动 |
| 5 | 鼠标加速 Mouse Accel. | 关闭 Enhance Pointer Precision |
| 6 | 视觉效果 Visual Effects | 调整为最佳性能 |
| 7 | SysMain | SSD 环境禁用，减少后台磁盘读写 |
| 8 | TCP 网络 Network | 降低游戏网络延迟 |
| 9 | 页面文件 Page File | 固定 8192 MB，减少碎片 |

---

## 快速开始 / Quick Start

### 方式一：直接使用 EXE（推荐 / Recommended）

1. 前往 [Releases](../../releases) 页面下载最新 `GameEnvSetup.exe`
2. 右键 → **以管理员身份运行** / Right-click → **Run as Administrator**
3. 完成 / Done

> 无需安装 Python，无需任何依赖。  
> No Python required. No dependencies. Fully portable.

---

### 方式二：从源码运行 / Run from Source

**环境要求 / Requirements**
- Python 3.8+
- Windows 10 / 11

```bash
# 克隆仓库 / Clone
git clone https://github.com/YOUR_USERNAME/WinGameOptimizer.git
cd WinGameOptimizer

# 直接运行 / Run directly
python main.py
```

---

### 方式三：自行打包 EXE / Build EXE yourself

```bash
pip install pyinstaller
python build.py
# 输出 / Output: dist\GameEnvSetup.exe
```

---

## 使用说明 / Usage

```
启动程序后 / After launching:

  [Diagnose 标签]
    点击 ▶ Run Diagnostics
    查看 [!!] 标记的问题项
    点击 💾 Save Report 保存报告

  [Optimize 标签]
    勾选需要的优化项（默认全选）
    点击 ▶ Apply Selected
    完成后重启 Windows

  [About 标签]
    功能说明与注意事项
```

> ⚠️ 优化功能需要管理员权限。诊断功能无管理员也可运行，但部分项目可能无法读取。  
> ⚠️ Optimization requires Administrator. Diagnostics can run without admin but some checks may be limited.

---

## 兼容性 / Compatibility

| 项目 | 支持 |
|---|---|
| Windows 10 22H2 | ✅ |
| Windows 11 | ✅ |
| NVIDIA GPU | ✅ |
| AMD GPU | ✅ |
| Intel GPU | ✅ |
| 无独显 / iGPU only | ✅ |

---

## 项目结构 / Project Structure

```
WinGameOptimizer/
├── main.py          # 主程序 GUI / Main GUI application
├── build.py         # PyInstaller 打包脚本 / Build script
├── README.md        # 本文件 / This file
└── dist/
    └── GameEnvSetup.exe   # 打包输出 / Packaged output
```

---

## 发布新版本 / Creating a Release

```bash
# 打包
python build.py

# 在 GitHub 创建 Release，上传 dist\GameEnvSetup.exe
# Go to GitHub → Releases → New Release → Upload GameEnvSetup.exe
```

---

## 免责声明 / Disclaimer

本工具修改的均为 Windows 标准可调参数（注册表游戏优化项、电源计划、系统服务）。  
所有操作均可手动还原。使用前建议创建系统还原点。

This tool only modifies standard Windows tunable parameters (registry game tweaks, power plans, services).  
All changes can be manually reverted. Creating a system restore point before use is recommended.

---

## License

MIT
