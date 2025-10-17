@echo off
REM Setup script for Windows
setlocal enabledelayedexpansion

echo 🚀 Setting up PaddleOCR Plugin for Pot-App
echo Platform: Windows

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Found Python %PYTHON_VERSION%

REM Check if we're in the plugin directory
if not exist "ocr_service.py" (
    echo ❌ Please run this script from the plugin directory
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing PaddleOCR and dependencies...
pip install -r requirements.txt

REM Test installation
echo 🧪 Testing installation...
python -c "import paddleocr; from PIL import Image; from quart import Quart; print('✅ All dependencies installed successfully!'); print('📋 PaddleOCR version:', paddleocr.__version__)"

echo.
echo 🎉 Setup completed successfully!
echo.
echo 📋 Next steps:
echo 1. Install the plugin .potext file in Pot-App
echo 2. The OCR service will start automatically when needed
echo 3. Check README.md for troubleshooting information
echo.
echo 🔧 To manually test the service:
echo    venv\Scripts\activate.bat
echo    python ocr_service.py
echo.
pause