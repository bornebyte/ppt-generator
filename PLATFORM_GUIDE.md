# Cross-Platform Installation & Usage Guide

## 🖥️ Windows Installation

### Method 1: Using Command Prompt (Recommended)

1. Open Command Prompt
2. Navigate to where you want to install:
   ```cmd
   cd %USERPROFILE%\Documents
   ```
3. Download and run installer:
   ```cmd
   curl -o install.bat https://raw.githubusercontent.com/bornebyte/ppt-generator/main/install.bat
   install.bat
   ```

### Method 2: Using PowerShell

1. Open PowerShell
2. Navigate to install location:
   ```powershell
   cd $env:USERPROFILE\Documents
   ```
3. Download and run installer:
   ```powershell
   Invoke-WebRequest -Uri "https://raw.githubusercontent.com/bornebyte/ppt-generator/main/install.ps1" -OutFile "install.ps1"
   powershell -ExecutionPolicy Bypass -File install.ps1
   ```

### Method 3: Manual Installation

1. Install Python 3.8+ from https://python.org (check "Add to PATH")
2. Install Git from https://git-scm.com
3. Clone repository:
   ```cmd
   git clone https://github.com/bornebyte/ppt-generator.git
   cd ppt-generator
   ```
4. Create virtual environment:
   ```cmd
   python -m venv venv
   venv\Scripts\activate.bat
   ```
5. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

### Running on Windows

**Option 1: Batch Script**
```cmd
cd path\to\ppt-generator
pptgen.bat              # Development mode
pptgen.bat -p           # Production mode
pptgen.bat -p 8000      # Custom port
```

**Option 2: PowerShell Script**
```powershell
cd path\to\ppt-generator
.\pptgen.ps1                      # Development mode
.\pptgen.ps1 -Production          # Production mode
.\pptgen.ps1 -Production -Port 8000
```

**Option 3: Universal Python Launcher**
```cmd
python pptgen-launcher.py
python pptgen-launcher.py -p
python pptgen-launcher.py -p 8000
```

---

## 🍎 macOS Installation

### Method 1: One-Line Install (Recommended)

```bash
curl -sSL https://raw.githubusercontent.com/bornebyte/ppt-generator/main/install.sh | bash
```

### Method 2: Manual Installation

1. Install Homebrew (if not installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install Python and Git:
   ```bash
   brew install python git
   ```

3. Clone and setup:
   ```bash
   git clone https://github.com/bornebyte/ppt-generator.git
   cd ppt-generator
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Running on macOS

```bash
cd /path/to/ppt-generator
./pptgen              # Development mode
./pptgen -p           # Production mode
./pptgen -p 8000      # Custom port
```

Or use the universal launcher:
```bash
python pptgen-launcher.py
python pptgen-launcher.py -p
```

---

## 🐧 Linux Installation

### Ubuntu/Debian

```bash
# Install prerequisites
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# One-line install
curl -sSL https://raw.githubusercontent.com/bornebyte/ppt-generator/main/install.sh | bash
```

### Fedora/RHEL/CentOS

```bash
# Install prerequisites
sudo dnf install python3 python3-pip git

# One-line install
curl -sSL https://raw.githubusercontent.com/bornebyte/ppt-generator/main/install.sh | bash
```

### Arch Linux

```bash
# Install prerequisites
sudo pacman -S python python-pip git

# One-line install
curl -sSL https://raw.githubusercontent.com/bornebyte/ppt-generator/main/install.sh | bash
```

### Running on Linux

```bash
cd /path/to/ppt-generator
./pptgen              # Development mode
./pptgen -p           # Production mode
./pptgen -p 8000      # Custom port
```

Or use the universal launcher:
```bash
python pptgen-launcher.py
python pptgen-launcher.py -p
```

---

## 🚨 Troubleshooting

### Windows Issues

**"Python is not recognized"**
- Reinstall Python and check "Add Python to PATH"
- Or add manually: `C:\Users\YourName\AppData\Local\Programs\Python\Python3x`

**"Execution of scripts is disabled"**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Port already in use**
```cmd
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### macOS Issues

**"command not found: python"**
```bash
# Use python3 explicitly
python3 -m venv venv
```

**Permission denied**
```bash
chmod +x pptgen install.sh pptgen-launcher.py
```

### Linux Issues

**"python3: command not found"**
```bash
# Install Python
sudo apt install python3 python3-pip python3-venv  # Ubuntu/Debian
sudo dnf install python3 python3-pip                # Fedora
```

**Virtual environment activation fails**
```bash
# Ensure venv module is installed
sudo apt install python3-venv  # Ubuntu/Debian
```

### Network/Timeout Issues

**Installation timeout**
```bash
# Increase timeout and retry
cd ~/.ppt-generator  # Linux/Mac
cd %USERPROFILE%\.ppt-generator  # Windows

# Activate venv first, then:
pip install --timeout 300 --retries 5 -r requirements.txt
```

---

## 🌐 Accessing the Application

After starting, open your browser and visit:
```
http://localhost:5000
```

Or from another device on the same network:
```
http://YOUR_IP:5000
```

To find your IP:
- **Windows:** `ipconfig`
- **macOS/Linux:** `ifconfig` or `ip addr`

---

## 🛑 Stopping the Server

- Press `Ctrl + C` in the terminal
- **Windows:** If server doesn't stop, close the terminal window

---

## 📝 Platform-Specific Notes

### Windows
- Use Command Prompt or PowerShell
- Backslashes in paths: `C:\Users\Name\ppt-generator`
- Some antivirus software may interfere with installation

### macOS
- May need to allow Terminal in Security & Privacy settings
- Use `python3` instead of `python`
- Requires Xcode Command Line Tools for some packages

### Linux
- Different package managers per distribution
- May need `sudo` for system-wide installations
- Check firewall settings if can't access from other devices

---

## 🎯 Best Practices

1. **Always activate virtual environment before running**
2. **Use production mode (Gunicorn) for better performance**
3. **Keep your installation updated:**
   ```bash
   cd /path/to/ppt-generator
   git pull
   source venv/bin/activate  # or venv\Scripts\activate.bat on Windows
   pip install -r requirements.txt --upgrade
   ```

---

For more help, see:
- [Main README](README.md)
- [Deployment Guide](DEPLOYMENT.md)
- [GitHub Issues](https://github.com/bornebyte/ppt-generator/issues)
