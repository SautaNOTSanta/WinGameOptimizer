#!/usr/bin/env python3
"""
game-env-setup GUI
Universal Windows 10/11 game environment checker + optimizer
Packages into a single EXE via PyInstaller
"""
import subprocess, sys, os, threading, ctypes, platform, winreg
from datetime import datetime

# ── GUI (tkinter, stdlib) ────────────────────────────────────
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

TITLE   = "Game Env Setup v1.0"
VERSION = "1.0.0"
BG      = "#0f0f0f"
FG      = "#e8e8e8"
ACCENT  = "#00d4ff"
WARN    = "#ffaa00"
ERR     = "#ff4444"
OK      = "#00cc66"
GRAY    = "#555555"
FONT_M  = ("Consolas", 11)
FONT_L  = ("Consolas", 13, "bold")
FONT_S  = ("Consolas", 9)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_ps(cmd, timeout=30):
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd],
            capture_output=True, text=True, timeout=timeout
        )
        return (r.stdout + r.stderr).strip()
    except Exception as e:
        return str(e)

def reg_get(hive, path, name):
    try:
        key = winreg.OpenKey(hive, path)
        val, _ = winreg.QueryValueEx(key, name)
        return val
    except:
        return None

# ══════════════════════════════════════════════════════════════
#  DIAGNOSE
# ══════════════════════════════════════════════════════════════
def run_diagnose(log):
    results = []
    warnings = []

    def ok(label, detail=""):
        results.append(("OK",   label, detail))
        log(f"  [OK]  {label}" + (f" — {detail}" if detail else ""), OK)

    def warn(label, detail=""):
        results.append(("WARN", label, detail))
        warnings.append(label)
        log(f"  [!!]  {label}" + (f" — {detail}" if detail else ""), WARN)

    def info(label, detail=""):
        results.append(("INFO", label, detail))
        log(f"  [--]  {label}" + (f" — {detail}" if detail else ""), FG)

    log("\n── System ──────────────────────────────────────", ACCENT)
    os_name  = run_ps("(Get-CimInstance Win32_OperatingSystem).Caption")
    os_build = run_ps("(Get-CimInstance Win32_OperatingSystem).BuildNumber")
    arch     = run_ps("(Get-CimInstance Win32_OperatingSystem).OSArchitecture")
    ram_gb   = run_ps("[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory/1GB,1)")
    free_gb  = run_ps("[math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB/1024,1)")
    info("OS",       f"{os_name} Build {os_build} {arch}")
    info("RAM",      f"{ram_gb} GB total / {free_gb} GB free")
    try:
        free_f = float(free_gb)
        if free_f < 2:
            warn("Low RAM", f"Only {free_gb} GB free")
        else:
            ok("RAM free", f"{free_gb} GB")
    except:
        pass

    log("\n── CPU ─────────────────────────────────────────", ACCENT)
    cpu_name  = run_ps("(Get-CimInstance Win32_Processor).Name.Trim()")
    cpu_cores = run_ps("(Get-CimInstance Win32_Processor).NumberOfCores")
    cpu_threads = run_ps("(Get-CimInstance Win32_Processor).NumberOfLogicalProcessors")
    power_plan  = run_ps("(powercfg /getactivescheme)")
    info("CPU",      cpu_name)
    info("Cores",    f"{cpu_cores} cores / {cpu_threads} threads")
    info("Power",    power_plan.split("(")[-1].replace(")","").strip() if "(" in power_plan else power_plan)
    if any(x in power_plan for x in ["Ultimate","卓越","High","高性能"]):
        ok("Power plan", "performance mode active")
    else:
        warn("Power plan", "not set to High/Ultimate Performance")

    log("\n── GPU ─────────────────────────────────────────", ACCENT)
    gpus = run_ps("Get-CimInstance Win32_VideoController | Select-Object Name,DriverVersion,DriverDate,AdapterRAM | ConvertTo-Json")
    import json
    try:
        gpu_list = json.loads(gpus)
        if isinstance(gpu_list, dict):
            gpu_list = [gpu_list]
        for g in gpu_list:
            name    = g.get("Name","?")
            driver  = g.get("DriverVersion","?")
            vram    = round((g.get("AdapterRAM") or 0)/1024/1024)
            info(f"GPU", f"{name} | Driver {driver} | {vram} MB VRAM")
            if "NVIDIA" in name or "AMD" in name or "Intel" in name:
                ok(f"GPU detected", name)
    except:
        info("GPU", gpus[:120])

    hags = reg_get(winreg.HKEY_LOCAL_MACHINE,
        r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers", "HwSchMode")
    if hags == 2:
        ok("HAGS", "Hardware Accelerated GPU Scheduling enabled")
    else:
        warn("HAGS", "not enabled (recommended for modern GPUs)")

    log("\n── Storage ─────────────────────────────────────", ACCENT)
    disks_raw = run_ps(
        "Get-CimInstance Win32_LogicalDisk | Where-Object {$_.DriveType -eq 3} | "
        "Select-Object DeviceID,FreeSpace,Size | ConvertTo-Json"
    )
    try:
        disks = json.loads(disks_raw)
        if isinstance(disks, dict):
            disks = [disks]
        for d in disks:
            did   = d.get("DeviceID","?")
            free  = round((d.get("FreeSpace") or 0)/1024**3, 1)
            total = round((d.get("Size") or 1)/1024**3, 1)
            pct   = round(free/total*100) if total else 0
            msg   = f"{free} GB free / {total} GB ({pct}%)"
            if pct < 10:
                warn(f"Disk {did}", msg + " — CRITICALLY LOW")
            elif pct < 15:
                warn(f"Disk {did}", msg + " — low space")
            else:
                ok(f"Disk {did}", msg)
    except:
        info("Disks", disks_raw[:120])

    log("\n── Runtimes ────────────────────────────────────", ACCENT)
    runtime_checks = [
        (winreg.HKEY_LOCAL_MACHINE,
         r"SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64", "VC++ 2015-2022 x64"),
        (winreg.HKEY_LOCAL_MACHINE,
         r"SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x86", "VC++ 2015-2022 x86"),
        (winreg.HKEY_LOCAL_MACHINE,
         r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full",    ".NET Framework 4.x"),
    ]
    for hive, path, label in runtime_checks:
        val = reg_get(hive, path, "Version") or reg_get(hive, path, "Release")
        if val:
            ok(label, str(val))
        else:
            warn(label, "not found — run install_game_env.ps1")

    dx_ver = reg_get(winreg.HKEY_LOCAL_MACHINE,
        r"SOFTWARE\Microsoft\DirectX", "Version")
    info("DirectX", dx_ver or "unknown")

    log("\n── Services ────────────────────────────────────", ACCENT)
    svcs = {
        "AudioSrv":  "Windows Audio",
        "BFE":       "Base Filtering Engine",
        "mpssvc":    "Windows Firewall",
    }
    for svc, desc in svcs.items():
        status = run_ps(f"(Get-Service {svc} -ErrorAction SilentlyContinue).Status")
        if "Running" in status:
            ok(f"{desc} ({svc})", "Running")
        else:
            warn(f"{desc} ({svc})", status or "not found")

    log("\n── Network ─────────────────────────────────────", ACCENT)
    adapters = run_ps(
        "Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} | "
        "Select-Object Name,LinkSpeed | ConvertTo-Json"
    )
    try:
        ads = json.loads(adapters)
        if isinstance(ads, dict): ads = [ads]
        for a in ads:
            info("Adapter", f"{a.get('Name','?')} — {a.get('LinkSpeed','?')}")
    except:
        pass
    ping = run_ps("Test-Connection 8.8.8.8 -Count 1 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty ResponseTime")
    if ping and ping.strip().isdigit():
        ms = int(ping.strip())
        if ms < 80:
            ok("Internet ping", f"{ms} ms")
        else:
            warn("Internet ping", f"{ms} ms — high latency")
    else:
        warn("Internet", "8.8.8.8 unreachable")

    log("\n── Summary ─────────────────────────────────────", ACCENT)
    if warnings:
        log(f"  {len(warnings)} issue(s) found:", WARN)
        for w in warnings:
            log(f"    [!!] {w}", WARN)
    else:
        log("  All checks passed.", OK)

    return warnings

# ══════════════════════════════════════════════════════════════
#  OPTIMIZE
# ══════════════════════════════════════════════════════════════
OPTIMIZE_STEPS = [
    ("Power Plan",
     "Activate Ultimate/High Performance power plan",
     """
$dup = powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61 2>&1
$s = powercfg /list | Select-String 'Ultimate|卓越|High|高性能' | Select-Object -First 1
if ($s) {
    $guid = ($s -split '\s+')[3]
    powercfg /setactive $guid
    "Power plan activated: $guid"
} else {
    powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
    "High Performance activated"
}
"""),
    ("Disable Xbox Game Bar",
     "Reduces background CPU usage",
     """
Set-ItemProperty 'HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\GameDVR' AppCaptureEnabled 0 -Force
Set-ItemProperty 'HKCU:\\System\\GameConfigStore' GameDVR_Enabled 0 -Force
Get-AppxPackage 'Microsoft.XboxGamingOverlay' | Remove-AppxPackage -ErrorAction SilentlyContinue
"Xbox Game Bar disabled"
"""),
    ("Enable HAGS",
     "Hardware Accelerated GPU Scheduling — reduces input latency (reboot required)",
     """
Set-ItemProperty 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers' HwSchMode 2 -Force
"HAGS enabled"
"""),
    ("Disable Fullscreen Optimizations",
     "Reduces frame pacing issues in some games",
     """
Set-ItemProperty 'HKCU:\\System\\GameConfigStore' GameDVR_FSEBehaviorMode 2 -Force
Set-ItemProperty 'HKCU:\\System\\GameConfigStore' GameDVR_HonorUserFSEBehaviorMode 1 -Force
"Fullscreen optimizations disabled"
"""),
    ("Disable Mouse Acceleration",
     "Removes Enhance Pointer Precision",
     """
Set-ItemProperty 'HKCU:\\Control Panel\\Mouse' MouseSpeed '0' -Force
Set-ItemProperty 'HKCU:\\Control Panel\\Mouse' MouseThreshold1 '0' -Force
Set-ItemProperty 'HKCU:\\Control Panel\\Mouse' MouseThreshold2 '0' -Force
"Mouse acceleration disabled"
"""),
    ("Visual Effects: Best Performance",
     "Disables animations and transparency",
     """
Set-ItemProperty 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects' VisualFXSetting 2 -Force
"Visual effects optimized"
"""),
    ("Disable SysMain",
     "Not needed on SSD, reduces background disk activity",
     """
Stop-Service SysMain -Force -ErrorAction SilentlyContinue
Set-Service SysMain -StartupType Disabled -ErrorAction SilentlyContinue
"SysMain disabled"
"""),
    ("TCP Network Optimization",
     "Lower game network latency",
     """
netsh int tcp set global autotuninglevel=normal 2>&1
netsh int tcp set global ecncapability=disabled 2>&1
netsh int tcp set global timestamps=disabled 2>&1
Set-ItemProperty 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters' TcpAckFrequency 1 -Force
Set-ItemProperty 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters' TCPNoDelay 1 -Force
"TCP optimized"
"""),
    ("Page File: Fixed 8192 MB",
     "Reduces fragmentation (reboot required)",
     """
$cs = Get-WmiObject Win32_ComputerSystem
$cs.AutomaticManagedPagefile = $false
$cs.Put() | Out-Null
$pf = Get-WmiObject Win32_PageFileSetting
if ($pf) { $pf.InitialSize = 8192; $pf.MaximumSize = 8192; $pf.Put() | Out-Null }
"Page file set to 8192 MB"
"""),
]

# ══════════════════════════════════════════════════════════════
#  GUI
# ══════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(TITLE)
        self.configure(bg=BG)
        self.geometry("900x640")
        self.resizable(True, True)
        self._build()

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(16,0))
        tk.Label(hdr, text="GAME ENV SETUP", font=("Consolas",18,"bold"),
                 bg=BG, fg=ACCENT).pack(side="left")
        tk.Label(hdr, text=f"v{VERSION}", font=FONT_S, bg=BG, fg=GRAY).pack(side="left", padx=8, pady=4)

        if not is_admin():
            tk.Label(hdr, text="⚠ Run as Administrator for full functionality",
                     font=FONT_S, bg=BG, fg=WARN).pack(side="right")

        # Tabs
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=20, pady=12)

        self._build_diagnose_tab()
        self._build_optimize_tab()
        self._build_about_tab()

    def _build_diagnose_tab(self):
        f = tk.Frame(self.nb, bg=BG)
        self.nb.add(f, text="  Diagnose  ")

        ctrl = tk.Frame(f, bg=BG)
        ctrl.pack(fill="x", padx=4, pady=8)
        self.btn_diag = tk.Button(ctrl, text="▶  Run Diagnostics",
            font=FONT_M, bg=ACCENT, fg=BG, activebackground="#00aacc",
            bd=0, padx=20, pady=8, cursor="hand2",
            command=self._start_diagnose)
        self.btn_diag.pack(side="left")
        self.btn_save_diag = tk.Button(ctrl, text="💾  Save Report",
            font=FONT_M, bg="#222", fg=FG, activebackground="#333",
            bd=0, padx=16, pady=8, cursor="hand2",
            command=self._save_diag_report, state="disabled")
        self.btn_save_diag.pack(side="left", padx=8)
        self.lbl_diag_status = tk.Label(ctrl, text="", font=FONT_S, bg=BG, fg=GRAY)
        self.lbl_diag_status.pack(side="left", padx=8)

        self.diag_log = scrolledtext.ScrolledText(f, font=FONT_S, bg="#0a0a0a", fg=FG,
            insertbackground=FG, relief="flat", bd=0, padx=12, pady=8)
        self.diag_log.pack(fill="both", expand=True, padx=4, pady=(0,4))
        for tag, color in [("OK",OK),("WARN",WARN),("ERR",ERR),("ACCENT",ACCENT),("GRAY",GRAY)]:
            self.diag_log.tag_config(tag, foreground=color)
        self.diag_log.config(state="disabled")
        self._diag_text = ""

    def _build_optimize_tab(self):
        f = tk.Frame(self.nb, bg=BG)
        self.nb.add(f, text="  Optimize  ")

        top = tk.Frame(f, bg=BG)
        top.pack(fill="x", padx=4, pady=8)
        tk.Label(top, text="Select optimizations to apply:",
                 font=FONT_M, bg=BG, fg=FG).pack(side="left")
        tk.Button(top, text="Select All", font=FONT_S, bg="#222", fg=FG,
                  bd=0, padx=10, pady=4, cursor="hand2",
                  command=lambda: [v.set(True) for v in self.opt_vars]).pack(side="right")
        tk.Button(top, text="None", font=FONT_S, bg="#222", fg=FG,
                  bd=0, padx=10, pady=4, cursor="hand2",
                  command=lambda: [v.set(False) for v in self.opt_vars]).pack(side="right", padx=4)

        # Checkboxes
        chk_frame = tk.Frame(f, bg=BG)
        chk_frame.pack(fill="x", padx=4)
        self.opt_vars = []
        for i, (name, desc, _) in enumerate(OPTIMIZE_STEPS):
            var = tk.BooleanVar(value=True)
            self.opt_vars.append(var)
            row = tk.Frame(chk_frame, bg=BG)
            row.pack(fill="x", pady=2)
            tk.Checkbutton(row, variable=var, bg=BG, fg=FG,
                selectcolor="#1a1a1a", activebackground=BG,
                text=f"  {name}", font=FONT_M).pack(side="left")
            tk.Label(row, text=f"— {desc}", font=FONT_S, bg=BG, fg=GRAY).pack(side="left")

        sep = tk.Frame(f, bg=GRAY, height=1)
        sep.pack(fill="x", padx=4, pady=8)

        ctrl2 = tk.Frame(f, bg=BG)
        ctrl2.pack(fill="x", padx=4, pady=4)
        self.btn_opt = tk.Button(ctrl2, text="▶  Apply Selected",
            font=FONT_M, bg=ACCENT, fg=BG, activebackground="#00aacc",
            bd=0, padx=20, pady=8, cursor="hand2",
            command=self._start_optimize)
        self.btn_opt.pack(side="left")
        self.lbl_opt_status = tk.Label(ctrl2, text="", font=FONT_S, bg=BG, fg=GRAY)
        self.lbl_opt_status.pack(side="left", padx=8)

        self.opt_log = scrolledtext.ScrolledText(f, font=FONT_S, bg="#0a0a0a", fg=FG,
            insertbackground=FG, relief="flat", bd=0, padx=12, pady=8, height=8)
        self.opt_log.pack(fill="both", expand=True, padx=4, pady=(0,4))
        for tag, color in [("OK",OK),("WARN",WARN),("ERR",ERR),("ACCENT",ACCENT)]:
            self.opt_log.tag_config(tag, foreground=color)
        self.opt_log.config(state="disabled")

    def _build_about_tab(self):
        f = tk.Frame(self.nb, bg=BG)
        self.nb.add(f, text="  About  ")
        about_text = f"""
  {TITLE}

  Universal Windows 10/11 game environment checker and optimizer.

  Diagnose tab:
    · Scans CPU, GPU, RAM, storage, runtimes, services, network
    · Flags issues with [!!] markers
    · Save full report to text file

  Optimize tab:
    · Each step can be individually selected
    · Applies registry tweaks and system settings
    · Requires Administrator privileges

  Optimizations applied:
    1. Power Plan — Ultimate/High Performance
    2. Xbox Game Bar — disabled
    3. HAGS — Hardware Accelerated GPU Scheduling
    4. Fullscreen Optimizations — disabled
    5. Mouse Acceleration — disabled
    6. Visual Effects — best performance
    7. SysMain — disabled (SSD systems)
    8. TCP Network — latency optimized
    9. Page File — fixed 8192 MB

  After optimizing, reboot Windows for all changes to take effect.

  Built with Python + tkinter. No external dependencies.
"""
        tk.Label(f, text=about_text, font=FONT_S, bg=BG, fg=FG,
                 justify="left", anchor="nw").pack(fill="both", padx=20, pady=12)

    # ── Diagnose logic ───────────────────────────────────────
    def _diag_log(self, text, color=None):
        self.diag_log.config(state="normal")
        tag = None
        if color == OK:    tag = "OK"
        elif color == WARN: tag = "WARN"
        elif color == ERR:  tag = "ERR"
        elif color == ACCENT: tag = "ACCENT"
        elif color == GRAY:   tag = "GRAY"
        self.diag_log.insert("end", text + "\n", tag or "")
        self.diag_log.see("end")
        self.diag_log.config(state="disabled")
        self._diag_text += text + "\n"

    def _start_diagnose(self):
        self.diag_log.config(state="normal")
        self.diag_log.delete("1.0", "end")
        self.diag_log.config(state="disabled")
        self._diag_text = ""
        self.btn_diag.config(state="disabled")
        self.btn_save_diag.config(state="disabled")
        self.lbl_diag_status.config(text="Running...", fg=ACCENT)
        def worker():
            self._diag_log(f"Game Env Setup — Diagnostics", ACCENT)
            self._diag_log(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", GRAY)
            warns = run_diagnose(self._diag_log)
            if warns:
                self.lbl_diag_status.config(text=f"{len(warns)} issue(s) found", fg=WARN)
            else:
                self.lbl_diag_status.config(text="All checks passed", fg=OK)
            self.btn_diag.config(state="normal")
            self.btn_save_diag.config(state="normal")
        threading.Thread(target=worker, daemon=True).start()

    def _save_diag_report(self):
        from tkinter import filedialog
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files","*.txt"),("All","*.*")],
            initialfile=f"diagnose_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        if path:
            with open(path, "w", encoding="utf-8") as fp:
                fp.write(self._diag_text)
            messagebox.showinfo("Saved", f"Report saved to:\n{path}")

    # ── Optimize logic ───────────────────────────────────────
    def _opt_log(self, text, color=None):
        self.opt_log.config(state="normal")
        tag = None
        if color == OK:    tag = "OK"
        elif color == WARN: tag = "WARN"
        elif color == ERR:  tag = "ERR"
        elif color == ACCENT: tag = "ACCENT"
        self.opt_log.insert("end", text + "\n", tag or "")
        self.opt_log.see("end")
        self.opt_log.config(state="disabled")

    def _start_optimize(self):
        selected = [i for i, v in enumerate(self.opt_vars) if v.get()]
        if not selected:
            messagebox.showwarning("Nothing selected", "Select at least one optimization.")
            return
        if not is_admin():
            messagebox.showerror("Admin required",
                "Please restart this program as Administrator.")
            return
        if not messagebox.askyesno("Confirm",
            f"Apply {len(selected)} optimization(s)?\n\nA reboot may be required."):
            return
        self.btn_opt.config(state="disabled")
        self.lbl_opt_status.config(text="Running...", fg=ACCENT)
        self.opt_log.config(state="normal")
        self.opt_log.delete("1.0","end")
        self.opt_log.config(state="disabled")
        def worker():
            self._opt_log(f"Starting optimizations — {datetime.now().strftime('%H:%M:%S')}", ACCENT)
            for i in selected:
                name, desc, ps_cmd = OPTIMIZE_STEPS[i]
                self._opt_log(f"\n  [{i+1}] {name}", ACCENT)
                result = run_ps(ps_cmd, timeout=60)
                self._opt_log(f"      {result.splitlines()[0] if result else 'done'}", OK)
            self._opt_log("\nDone. Reboot Windows to apply all changes.", OK)
            self.lbl_opt_status.config(text="Complete — reboot recommended", fg=OK)
            self.btn_opt.config(state="normal")
        threading.Thread(target=worker, daemon=True).start()

if __name__ == "__main__":
    if platform.system() != "Windows":
        print("This tool is for Windows only.")
        sys.exit(1)
    app = App()
    app.mainloop()
