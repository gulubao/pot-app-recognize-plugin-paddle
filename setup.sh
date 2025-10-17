#!/bin/bash
# Setup script for Linux/macOS
set -e

echo "🚀 Setting up PaddleOCR Plugin for Pot-App"
echo "Platform: $(uname -s)"

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Found Python $PYTHON_VERSION"

# Check if we're in the plugin directory
if [ ! -f "ocr_service.py" ]; then
    echo "❌ Please run this script from the plugin directory"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing PaddleOCR and dependencies..."
pip install -r requirements.txt

# Test installation
echo "🧪 Testing installation..."
python3 -c "
import paddleocr
from PIL import Image
from quart import Quart
print('✅ All dependencies installed successfully!')
print('📋 PaddleOCR version:', paddleocr.__version__)
"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Install the plugin .potext file in Pot-App"
echo "2. The OCR service will start automatically when needed"
echo "3. Check README.md for troubleshooting information"
echo ""
echo "🔧 To manually test the service:"
echo "   source venv/bin/activate"
echo "   python3 ocr_service.py"