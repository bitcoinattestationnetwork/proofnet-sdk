#!/usr/bin/env python3
"""
Windows 11 System Heat Monitor
Logs CPU, memory, and temperature data to identify what causes high temps
"""

import psutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

LOG_FILE = Path.home() / "system_monitor.log"

def get_cpu_temp():
    """Get CPU temperature using WMI (Windows only)"""
    try:
        result = subprocess.run(
            'wmic path win32_temperaturezone get currenttemperature',
            capture_output=True,
            text=True,
            shell=True
        )
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            temp_raw = float(lines[1])
            temp_celsius = (temp_raw - 2732) / 10
            return round(temp_celsius, 1)
    except:
        pass
    return None

def get_top_processes(n=5):
    """Get top N processes by CPU usage"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            pinfo = proc.as_dict(attrs=['name', 'cpu_percent', 'memory_percent'])
            if pinfo['cpu_percent'] > 0:
                processes.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Sort by CPU usage
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    return processes[:n]

def log_system_state():
    """Log current system state"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    temp = get_cpu_temp()

    log_entry = f"\n{'='*70}\n"
    log_entry += f"Timestamp: {timestamp}\n"
    log_entry += f"CPU Usage: {cpu_percent}%\n"
    log_entry += f"Memory: {memory.percent}% ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)\n"
    log_entry += f"Disk: {disk.percent}% full\n"

    if temp:
        log_entry += f"CPU Temperature: {temp}°C\n"

    log_entry += f"\nTop 5 CPU-consuming processes:\n"
    log_entry += f"{'-'*70}\n"

    top_procs = get_top_processes(5)
    if top_procs:
        for proc in top_procs:
            log_entry += f"  {proc['name']:30} | CPU: {proc['cpu_percent']:6.1f}% | RAM: {proc['memory_percent']:6.1f}%\n"
    else:
        log_entry += "  (No processes using significant CPU)\n"

    print(log_entry)

    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)

def main():
    print(f"Starting system monitor. Logging to: {LOG_FILE}")
    print("Press Ctrl+C to stop.\n")

    # Clear previous log if it exists
    if LOG_FILE.exists():
        with open(LOG_FILE, 'w') as f:
            f.write(f"System Monitor Log - Started {datetime.now()}\n")

    interval = 5  # Log every 5 seconds

    try:
        while True:
            log_system_state()
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\n\nMonitoring stopped. Log saved to: {LOG_FILE}")

if __name__ == "__main__":
    main()
