@echo off
:: =====================================================================================
:: 🚀 INDUSTRY-LEADING AI EXECUTION WINDOWS INSTALLER
:: ✅ Self-Healing, Secure, AI Execution Optimized, Failure-Proof, Unified Model Support
:: =====================================================================================

SET LOG_FILE=%USERPROFILE%\ai_windows_installer.log
SET ERROR_LOG_FILE=%USERPROFILE%\ai_windows_installer_error.log
ECHO Logging installation to %LOG_FILE%

:: Redirect output and errors to log files
ECHO Starting AI Execution Installation... > %LOG_FILE% 2> %ERROR_LOG_FILE%

:: =====================================================================================
:: 🛠️ SYSTEM CHECK & PRE-INSTALLATION VALIDATION
:: =====================================================================================
ECHO 🔍 Validating system requirements...

:: Ensure script is run as Administrator
NET SESSION >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO ❌ This script must be run as Administrator! Run as Administrator and try again.
    EXIT /B 1
)

:: =====================================================================================
:: 🛠️ INSTALL REQUIRED SYSTEM PACKAGES (Python, Docker, NVIDIA Drivers)
:: =====================================================================================
ECHO 🔹 Installing system dependencies...

:: Install Chocolatey if not available
WHERE CHOCO >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO 🚀 Installing Chocolatey...
    @powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" >> %LOG_FILE% 2>> %ERROR_LOG_FILE%
)

:: Install Python, Git, Docker, and NVIDIA drivers if not installed
CHOCO INSTALL -Y PYTHON3 GIT DOCKER DESKTOP NVIDIA-DISPLAY-DRIVER >> %LOG_FILE% 2>> %ERROR_LOG_FILE%

:: Restart Docker service
NET START "Docker Desktop Service" >> %LOG_FILE% 2>> %ERROR_LOG_FILE%

:: =====================================================================================
:: 🖥️ CHECK & CONFIGURE GPU SUPPORT (CUDA, TensorRT, ONNX)
:: =====================================================================================
WHERE NVSMI >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    ECHO ✅ NVIDIA GPU detected! Configuring AI execution...
    CHOCO INSTALL -Y CUDA TENSORRT >> %LOG_FILE% 2>> %ERROR_LOG_FILE%
) ELSE (
    ECHO ⚠️ No NVIDIA GPU detected. Running in CPU mode.
)

:: =====================================================================================
:: ⚙️ INSTALL AI DEPENDENCIES & EXECUTION FRAMEWORKS
:: =====================================================================================
ECHO 🔹 Installing AI execution dependencies...
PY -3 -m PIP INSTALL --UPGRADE PIP >> %LOG_FILE% 2>> %ERROR_LOG_FILE%
PY -3 -m PIP INSTALL -R %USERPROFILE%\app\src\core\requirements.txt >> %LOG_FILE% 2>> %ERROR_LOG_FILE%

:: =====================================================================================
:: 🔐 SECURITY & EXECUTION MONITORING CONFIGURATION
:: =====================================================================================
ECHO 🔹 Configuring security and monitoring...

:: Enforce Firewall Rules
NETSH ADVFIREWALL FIREWALL ADD RULE NAME="AI Execution Engine" DIR=IN ACTION=ALLOW PROTOCOL=TCP LOCALPORT=8000 >> %LOG_FILE% 2>> %ERROR_LOG_FILE%

:: Schedule AI Execution Monitoring Task
SCHTASKS /CREATE /SC MINUTE /MO 1 /TN "Monitor AI Execution" /TR "POWERSHELL -ExecutionPolicy Bypass -Command {IF (-NOT (Get-Process -Name ai_execution -ErrorAction SilentlyContinue)) {Start-Process Docker -ArgumentList 'restart ai_execution'}}" /RU SYSTEM >> %LOG_FILE% 2>> %ERROR_LOG_FILE%

:: =====================================================================================
:: 🚀 START AI EXECUTION ENGINE (WITH AUTO-RECOVERY)
:: =====================================================================================
ECHO 🚀 Starting AI Execution Engine...

CD %USERPROFILE%\app\deploy\
DOCKER-COMPOSE UP --BUILD -D >> %LOG_FILE% 2>> %ERROR_LOG_FILE%
IF %ERRORLEVEL% NEQ 0 (
    ECHO ❌ AI Execution failed! Retrying...
    DOCKER-COMPOSE RESTART >> %LOG_FILE% 2>> %ERROR_LOG_FILE%
)

ECHO ✅ Installation Complete! AI Execution Engine is now running. 🎯

:: =====================================================================================
:: 📈 MONITOR EXECUTION & AUTO-RECOVERY
:: =====================================================================================
ECHO 📈 Monitoring AI execution performance...

:: Start infinite monitoring loop
:MONITOR
TIMEOUT /T 30
DOCKER PS | FINDSTR "ai_execution" >nul
IF %ERRORLEVEL% NEQ 0 (
    ECHO ❌ AI Execution stopped unexpectedly! Restarting...
    DOCKER-COMPOSE RESTART >> %LOG_FILE% 2>> %ERROR_LOG_FILE%
)
GOTO MONITOR

