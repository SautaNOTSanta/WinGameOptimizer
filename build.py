#!/usr/bin/env python3
"""
build.py — 打包 game-env-setup 为单文件 EXE
在 Windows 上运行：python build.py
需要：pip install pyinstaller
"""
import subprocess, sys, os, shutil
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
BUILD = ROOT / "build"
SPEC = ROOT / "game_env_setup.spec"

def run(cmd):
    print(f"  >> {' '.join(cmd)}")
    r = subprocess.run(cmd, capture_output=False)
    if r.returncode != 0:
        print(f"  [!!] Command failed with code {r.returncode}")
        sys.exit(r.returncode)

def main():
    print("=" * 60)
    print("  game-env-setup — PyInstaller build")
    print("=" * 60)

    # 检查 PyInstaller
    try:
        import PyInstaller
        print(f"  [OK] PyInstaller {PyInstaller.__version__}")
    except ImportError:
        print("  [!!] PyInstaller not found. Installing...")
        run([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 清理旧构建
    for d in [DIST, BUILD]:
        if d.exists():
            shutil.rmtree(d)
            print(f"  [--] Cleaned {d}")

    # 构建命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                      # 单文件 EXE
        "--noconsole",                    # 无控制台窗口（GUI 应用）
        "--name", "GameEnvSetup",
        "--distpath", str(DIST),
        "--workpath", str(BUILD),
        "--clean",
        str(ROOT / "main.py"),
    ]

    print("\n  Building EXE...")
    run(cmd)

    exe = DIST / "GameEnvSetup.exe"
    if exe.exists():
        size_mb = round(exe.stat().st_size / 1024 / 1024, 1)
        print(f"\n  [OK] Build successful!")
        print(f"       {exe}")
        print(f"       Size: {size_mb} MB")
        print(f"\n  Right-click GameEnvSetup.exe -> Run as Administrator")
    else:
        print("\n  [!!] EXE not found after build. Check errors above.")

if __name__ == "__main__":
    main()
