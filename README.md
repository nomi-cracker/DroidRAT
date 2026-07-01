<div align="center">
## 🚀 FEATURES

### 🔥 DroidRAT Features
| Feature | Status | Description |
|---------|--------|-------------|
| 📱 USB Scanning | ✅ | Automatic USB device enumeration and exploitation |
| 🎯 Session Management | ✅ | Multi-session handler with background persistence |
| ⚙️ Configuration | ✅ | Full configurable settings and preferences |
| 📦 APK Builder | ✅ | Bind payloads with legitimate Android applications |
| 🐍 Python Payloads | ✅ | Custom Python reverse shell generation |
| 📜 Shell Payloads | ✅ | Bash and Meterpreter payload generation |
| 📂 Modules System | ✅ | Extensible module framework |
| 💥 Exploits Database | ✅ | Built-in exploit collection |
| 🔵 Bluetooth HID | ✅ | Bluetooth HID attack vector |
| 🔌 OTG USB Attack | ✅ | USB Rubber Ducky style attacks |
## 📱 DROIDRAT FRAMEWORK

██████╗ ██████╗ ██████╗ ██╗██████╗ ██████╗ █████╗ ████████╗ ██╔══██╗██╔══██╗██╔═══██╗██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝ ██║ ██║██████╔╝██║ ██║██║██║ ██║██████╔╝███████║ ██║
██║ ██║██╔══██╗██║ ██║██║██║ ██║██╔══██╗██╔══██║ ██║
██████╔╝██║ ██║╚██████╔╝██║██████╔╝██║ ██║██║ ██║ ██║
╚═════╝ ╚═╝ ╚═╝ ╚═════╝ ╚═╝╚═════╝ ╚═╝ ╚═╝╚═╝ ╚═╝ ╚═╝
## 📱 DROIDRAT FRAMEWORK

██████╗ ██████╗ ██████╗ ██╗██████╗ ██████╗ █████╗ ████████╗ ██╔══██╗██╔══██╗██╔═══██╗██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝ ██║ ██║██████╔╝██║ ██║██║██║ ██║██████╔╝███████║ ██║
██║ ██║██╔══██╗██║ ██║██║██║ ██║██╔══██╗██╔══██║ ██║
██████╔╝██║ ██║╚██████╔╝██║██████╔╝██║ ██║██║ ██║ ██║
╚═════╝ ╚═╝ ╚═╝ ╚═════╝ ╚═╝╚═════╝ ╚═╝ ╚═╝╚═╝ ╚═╝ ╚═╝

## 📥 INSTALLATION

### Method 1: Quick Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/nomi-cracker/DroidRAT.git
cd DroidRAT

# Make installer executable
chmod +x install.sh

# Run installer
./install.sh
Method 2: Manual Installation
# Clone the repository
git clone https://github.com/nomi-cracker/DroidRAT.git
cd DroidRAT

# Create virtual environment (Recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install system dependencies (Kali Linux)
sudo apt update
sudo apt install -y python3 python3-pip python3-venv \
    git curl wget tor proxychains \
    chromium chromium-driver 2>/dev/null || true
Method 3: One-Line Install
curl -sL https://bit.ly/nomi-cyber-x | bash
Method 4: Android (Termux)
pkg update && pkg upgrade
pkg install python python-pip git
git clone https://github.com/nomi-cracker/DroidRAT.git
cd DroidRAT
pip install -r requirements.txt
python3 droidrat.py
📋 REQUIREMENTS
System Requirements
Component	Minimum	Recommended
OS	Linux / Android	Kali Linux
Python	3.8+	3.11+
RAM	2GB	4GB+
Storage	500MB	1GB+
Internet	Required	High-speed
Python Dependencies
aiohttp>=3.9.0
colorama>=0.4.6
faker>=20.0.0
fake-useragent>=1.4.0
PyYAML>=6.0
selenium>=4.15.0
webdriver-manager>=4.0.0
requests>=2.31.0
cryptography>=41.0.0
rich>=13.6.0
psutil>=5.9.0
pandas>=2.0.0
🚀 QUICK START
DroidRAT Quick Start
python3 droidrat.py

# Menu:
# [1] Start Server
# [2] Generate Payload
# [3] USB Scanner
# [4] APK Builder
# [5] Modules
📖 USAGE GUIDE
DroidRAT Usage
Option 1: USB Scanner
Scans connected USB devices for vulnerabilities
Automatically detects and exploits known vulnerabilities
Option 2: APK Builder
[1] msfvenom APK - Generate Metasploit payload APK
[2] Legit App Template - Inject into real APK
[3] Smali Injection - Manual smali code injection
[4] Python + Kivy - Python-based Android app
[5] Python Payload - Raw Python reverse shell
[6] JAR Payload - Java archive payload
[7] Shell Payload - Bash/Meterpreter payload
[8] Termux Payload - Android Termux payload
Option 3: Session Manager
List active sessions
Interact with compromised devices
Background session persistence
👥 JOIN NOMI CYBER-X TEAM
WhatsApp Group
Join our official NOMI CYBER-X TEAM WhatsApp group for:

🔥 Latest tool updates
💡 Tips & tricks
🛠️ Technical support
🤝 Collaboration opportunities
📢 Announcements
🎯 Exclusive content
▶️ JOIN NOW - NOMI CYBER-X TEAM
WhatsApp Group
╔══════════════════════════════════════════════════════╗
║           NOMI CYBER-X TEAM - WhatsApp Group        ║
╠══════════════════════════════════════════════════════╣
║  ✅ Direct support from developers                  ║
║  ✅ Early access to new features                    ║
║  ✅ Community of security researchers               ║
║  ✅ Step-by-step guides                             ║
║  ✅ Report bugs & get fixes                         ║
╚══════════════════════════════════════════════════════╝
🛠️ TROUBLESHOOTING
Common Issues & Solutions
Issue	Solution
ModuleNotFoundError	Run pip install -r requirements.txt
Chrome not found	Install: apt install chromium chromium-driver
Git push denied	Use SSH key or token authentication
Python version error	Use Python 3.8+: python3 --version
Permission denied	Run: chmod +x *.py
Virtual Environment Issues
# If you get externally-managed-environment error:
python3 -m venv nomi_env
source nomi_env/bin/activate
pip install -r requirements.txt
⚠️ DISCLAIMER
╔═══════════════════════════════════════════════════════════════╗
║                     IMPORTANT DISCLAIMER                      ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  NOMI CYBER-X Framework is developed SOLELY for:              ║
║                                                               ║
║  ✅ Authorized Penetration Testing                            ║
║  ✅ Security Research                                          ║
║  ✅ Educational Purposes                                       ║
║  ✅ CTF (Capture The Flag) Competitions                       ║
║  ✅ Bug Bounty Programs (with authorization)                   ║
║                                                               ║
║  ❌ UNAUTHORIZED USE IS STRICTLY PROHIBITED                    ║
║                                                               ║
║  By using this tool, you agree to:                            ║
║  • Use only on systems you OWN or have PERMISSION to test     ║
║  • Comply with all applicable local, state, and federal laws  ║
║  • NOT use for any illegal or malicious activities            ║
║  • Accept full responsibility for your actions                ║
║                                                               ║
║  The developers assume NO liability and are NOT responsible   ║
║  for any misuse or damage caused by this tool.                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
📞 CONTACT & SUPPORT
NOMI CYBER-X TEAM
Channel	Link
📱 WhatsApp Group	Join Now
💻 GitHub	nomi-cracker
📧 Email	nomiblackhate@gmail.com
Support Options
🔧 Open an issue on GitHub
💬 Ask in WhatsApp group
📝 Check documentation
🎥 Watch video tutorials
🌟 SUPPORT US
If you find this tool useful, consider:

⭐ Starring the repository
🔄 Sharing with your team
👥 Joining our WhatsApp group
📢 Spreading the word
© 2024-2025 NOMI CYBER-X TEAM. All Rights Reserved.

For authorized security testing purposes only

GitHub stars GitHub forks Twitter

Made with ❤️ by NOMI CYBER-X TEAM


