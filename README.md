# Pot-App PaddleOCR Plugin v5

![Version](https://img.shields.io/badge/version-v5.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-green)
![PaddleOCR](https://img.shields.io/badge/PaddleOCR-v5+-orange)

A modern, cross-platform OCR recognition plugin for [Pot-App](https://github.com/pot-app/pot-desktop) based on the latest PaddleOCR v5 with Vision-Language model support.

## ✨ Features

- 🌍 **Cross-platform support**: Windows, Linux, macOS, and WSL
- 🚀 **Latest PaddleOCR v5**: Enhanced accuracy with Vision-Language models  
- 🔄 **Auto-service management**: OCR service starts automatically when needed
- 📱 **Memory-efficient**: Base64 image processing without temporary files
- 🌐 **Multi-language support**: 9+ languages with intelligent detection
- ⚡ **HTTP API architecture**: Modern, scalable design

## 🆚 What's New (v5 vs Legacy)

| Feature | Legacy (v1.3.1) | New (v5.0) |
|---------|-----------------|------------|
| **Platform** | Windows x64 only | Windows, Linux, macOS, WSL |
| **PaddleOCR** | v1.3.1 (2022) | v5+ (2024) with VL models |
| **Architecture** | Subprocess + exe | HTTP service + Python API |
| **File I/O** | Temporary files | Memory-based base64 |
| **Setup** | Manual executable | Automated Python environment |

## 📋 Requirements

### System Requirements
- **Python 3.8+** (required for all platforms)
- **4GB+ RAM** (recommended for model loading)
- **Internet connection** (for initial model download)

### Platform-Specific Requirements

#### Windows
- Python 3.8+ installed and in PATH
- Windows 10/11 (x64 or ARM64)

#### Linux
- Python 3.8+ with development headers: `sudo apt-get install python3-dev`
- Ubuntu 18.04+, CentOS 7+, or equivalent

#### macOS
- Python 3.8+ (install via Homebrew: `brew install python`)
- macOS 10.15+ (Intel or Apple Silicon)

#### WSL (Windows Subsystem for Linux)
- WSL2 with Ubuntu 20.04+
- Python 3.8+ installed in WSL environment

## 🚀 Installation

### Option 1: Quick Setup (Recommended)

1. **Download** the latest `.potext` plugin file from [Releases](https://github.com/pot-app/pot-app-recognize-plugin-paddle/releases)

2. **Install in Pot-App**:
   - Open Pot-App → Preferences → Service Settings → Translation → Add External Plugin
   - Select the downloaded `.potext` file
   - Add to service list

3. **Run platform setup**:
   ```bash
   # Extract the .potext file (it's a zip archive)
   unzip plugin.com.pot-app.paddle.potext -d paddle-ocr-plugin
   cd paddle-ocr-plugin
   
   # Run setup script for your platform
   # Linux/macOS:
   chmod +x setup.sh && ./setup.sh
   
   # Windows:
   setup.bat
   ```

### Option 2: Manual Setup

1. **Clone or download** this repository
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Test the service**:
   ```bash
   python3 ocr_service.py
   # Should start service on http://127.0.0.1:28123
   ```

## 🔧 Configuration

### Supported Languages

| Pot-App Code | PaddleOCR Language | Description |
|-------------|-------------------|-------------|
| `zh_cn` | `chinese` | Simplified Chinese |
| `zh_tw` | `chinese_cht` | Traditional Chinese |
| `en` | `en` | English |
| `ja` | `japan` | Japanese |
| `ko` | `korean` | Korean |
| `fr` | `french_v2` | French |
| `ru` | `cyrillic` | Russian/Cyrillic |
| `de` | `german_v2` | German |
| `auto` | `chinese` | Auto-detect (fallback to Chinese) |

### Performance Tuning

You can modify `ocr_service.py` to optimize for your use case:

```python
# For faster startup (less accuracy):
PaddleOCR(ocr_version="PP-OCRv5", use_angle_cls=False)

# For better accuracy (slower):
PaddleOCR(ocr_version="PP-OCRv5", use_gpu=True)  # if CUDA available

# For different model sizes:
# mobile models: faster, less accurate
# server models: slower, more accurate (default)
```

## 🛠️ Development

### Project Structure
```
├── main.js              # Pot-App plugin interface
├── info.json            # Plugin metadata  
├── ocr_service.py       # Python OCR HTTP service
├── requirements.txt     # Python dependencies
├── setup.sh            # Linux/macOS setup script
├── setup.bat           # Windows setup script
└── .github/workflows/  # CI/CD automation
```

### Building from Source

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pot-app/pot-app-recognize-plugin-paddle.git
   cd pot-app-recognize-plugin-paddle
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Build plugin package**:
   ```bash
   # Manual build
   zip -r plugin.com.pot-app.paddle.potext \
       info.json main.js paddle.png \
       ocr_service.py requirements.txt \
       setup.sh setup.bat
   ```

### Testing

#### Test OCR Service
```bash
# Start the service
python3 ocr_service.py

# Test health endpoint
curl http://127.0.0.1:28123/health

# Test OCR endpoint (replace with your base64 image)
curl -X POST http://127.0.0.1:28123/ocr \
  -H "Content-Type: application/json" \
  -d '{"image": "base64_image_data", "language": "en"}'
```

#### Test Plugin Integration
1. Install plugin in Pot-App  
2. Test with various image types
3. Check console for any error messages

## 🐛 Troubleshooting

### Common Issues

#### "Python not found" Error
```bash
# Check Python installation
python3 --version  # or python --version on Windows

# Install Python if missing:
# Windows: Download from python.org
# macOS: brew install python
# Linux: sudo apt-get install python3
```

#### "Service startup timeout"
```bash
# Check if port 28123 is available
netstat -tulpn | grep 28123  # Linux/macOS
netstat -an | findstr 28123  # Windows

# Manually start service for debugging
python3 ocr_service.py
```

#### "Failed to initialize PaddleOCR"
```bash
# Clear PaddleOCR cache and reinstall
rm -rf ~/.paddleocr/  # Linux/macOS
# or %USERPROFILE%\.paddleocr\  # Windows

pip uninstall paddleocr
pip install paddleocr>=2.0.1
```

#### Memory Issues
- Ensure at least 4GB RAM available
- Close other applications if needed
- Consider using mobile models for faster startup

### Platform-Specific Issues

#### WSL Issues
```bash
# Ensure WSL2 is being used
wsl --list -v

# Install required packages
sudo apt-get update
sudo apt-get install python3-dev python3-pip
```

#### macOS ARM64 (M1/M2) Issues
```bash
# Install compatible versions
pip install paddleocr --no-deps
pip install paddlepaddle>=2.4.0
```

## 📚 API Reference

### OCR Service Endpoints

#### GET /health
Returns service health status.

#### POST /ocr
Performs OCR on base64 image.

**Request:**
```json
{
  "image": "base64_encoded_image",
  "language": "en"
}
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "text": "detected text",
      "confidence": 0.95,
      "box": [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
    }
  ]
}
```

#### GET /languages
Returns supported language list.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - Powerful OCR toolkit
- [Pot-App](https://github.com/pot-app/pot-desktop) - Translation and OCR tool
- [PaddleOCR-json](https://github.com/hiroi-sora/PaddleOCR-json) - Original inspiration

## 📞 Support

- 🐛 [Report Issues](https://github.com/pot-app/pot-app-recognize-plugin-paddle/issues)
- 💬 [Discussions](https://github.com/pot-app/pot-app-recognize-plugin-paddle/discussions)
- 📖 [Pot-App Documentation](https://pot-app.com/)# Pot-App PaddleOCR Plugin v5

![Version](https://img.shields.io/badge/version-v5.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-green)
![PaddleOCR](https://img.shields.io/badge/PaddleOCR-v5+-orange)

A modern, cross-platform OCR recognition plugin for [Pot-App](https://github.com/pot-app/pot-desktop) based on the latest PaddleOCR v5 with Vision-Language model support.

## ✨ Features

- 🌍 **Cross-platform support**: Windows, Linux, macOS, and WSL
- 🚀 **Latest PaddleOCR v5**: Enhanced accuracy with Vision-Language models  
- 🔄 **Auto-service management**: OCR service starts automatically when needed
- 📱 **Memory-efficient**: Base64 image processing without temporary files
- 🌐 **Multi-language support**: 9+ languages with intelligent detection
- ⚡ **HTTP API architecture**: Modern, scalable design

## 🆚 What's New (v5 vs Legacy)

| Feature | Legacy (v1.3.1) | New (v5.0) |
|---------|-----------------|------------|
| **Platform** | Windows x64 only | Windows, Linux, macOS, WSL |
| **PaddleOCR** | v1.3.1 (2022) | v5+ (2024) with VL models |
| **Architecture** | Subprocess + exe | HTTP service + Python API |
| **File I/O** | Temporary files | Memory-based base64 |
| **Setup** | Manual executable | Automated Python environment |

## 📋 Requirements

### System Requirements
- **Python 3.8+** (required for all platforms)
- **4GB+ RAM** (recommended for model loading)
- **Internet connection** (for initial model download)

### Platform-Specific Requirements

#### Windows
- Python 3.8+ installed and in PATH
- Windows 10/11 (x64 or ARM64)

#### Linux
- Python 3.8+ with development headers: `sudo apt-get install python3-dev`
- Ubuntu 18.04+, CentOS 7+, or equivalent

#### macOS
- Python 3.8+ (install via Homebrew: `brew install python`)
- macOS 10.15+ (Intel or Apple Silicon)

#### WSL (Windows Subsystem for Linux)
- WSL2 with Ubuntu 20.04+
- Python 3.8+ installed in WSL environment

## 🚀 Installation

### Option 1: Quick Setup (Recommended)

1. **Download** the latest `.potext` plugin file from [Releases](https://github.com/pot-app/pot-app-recognize-plugin-paddle/releases)

2. **Install in Pot-App**:
   - Open Pot-App → Preferences → Service Settings → Translation → Add External Plugin
   - Select the downloaded `.potext` file
   - Add to service list

3. **Run platform setup**:
   ```bash
   # Extract the .potext file (it's a zip archive)
   unzip plugin.com.pot-app.paddle.potext -d paddle-ocr-plugin
   cd paddle-ocr-plugin
   
   # Run setup script for your platform
   # Linux/macOS:
   chmod +x setup.sh && ./setup.sh
   
   # Windows:
   setup.bat
   ```

### Option 2: Manual Setup

1. **Clone or download** this repository
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Test the service**:
   ```bash
   python3 ocr_service.py
   # Should start service on http://127.0.0.1:28123
   ```

## 🔧 Configuration

### Supported Languages

| Pot-App Code | PaddleOCR Language | Description |
|-------------|-------------------|-------------|
| `zh_cn` | `chinese` | Simplified Chinese |
| `zh_tw` | `chinese_cht` | Traditional Chinese |
| `en` | `en` | English |
| `ja` | `japan` | Japanese |
| `ko` | `korean` | Korean |
| `fr` | `french_v2` | French |
| `ru` | `cyrillic` | Russian/Cyrillic |
| `de` | `german_v2` | German |
| `auto` | `chinese` | Auto-detect (fallback to Chinese) |

### Performance Tuning

You can modify `ocr_service.py` to optimize for your use case:

```python
# For faster startup (less accuracy):
PaddleOCR(ocr_version="PP-OCRv5", use_angle_cls=False)

# For better accuracy (slower):
PaddleOCR(ocr_version="PP-OCRv5", use_gpu=True)  # if CUDA available

# For different model sizes:
# mobile models: faster, less accurate
# server models: slower, more accurate (default)
```

## 🛠️ Development

### Project Structure
```
├── main.js              # Pot-App plugin interface
├── info.json            # Plugin metadata  
├── ocr_service.py       # Python OCR HTTP service
├── requirements.txt     # Python dependencies
├── setup.sh            # Linux/macOS setup script
├── setup.bat           # Windows setup script
└── .github/workflows/  # CI/CD automation
```

### Building from Source

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pot-app/pot-app-recognize-plugin-paddle.git
   cd pot-app-recognize-plugin-paddle
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Build plugin package**:
   ```bash
   # Manual build
   zip -r plugin.com.pot-app.paddle.potext \
       info.json main.js paddle.png \
       ocr_service.py requirements.txt \
       setup.sh setup.bat
   ```

### Testing

#### Test OCR Service
```bash
# Start the service
python3 ocr_service.py

# Test health endpoint
curl http://127.0.0.1:28123/health

# Test OCR endpoint (replace with your base64 image)
curl -X POST http://127.0.0.1:28123/ocr \
  -H "Content-Type: application/json" \
  -d '{"image": "base64_image_data", "language": "en"}'
```

#### Test Plugin Integration
1. Install plugin in Pot-App  
2. Test with various image types
3. Check console for any error messages

## 🐛 Troubleshooting

### Common Issues

#### "Python not found" Error
```bash
# Check Python installation
python3 --version  # or python --version on Windows

# Install Python if missing:
# Windows: Download from python.org
# macOS: brew install python
# Linux: sudo apt-get install python3
```

#### "Service startup timeout"
```bash
# Check if port 28123 is available
netstat -tulpn | grep 28123  # Linux/macOS
netstat -an | findstr 28123  # Windows

# Manually start service for debugging
python3 ocr_service.py
```

#### "Failed to initialize PaddleOCR"
```bash
# Clear PaddleOCR cache and reinstall
rm -rf ~/.paddleocr/  # Linux/macOS
# or %USERPROFILE%\.paddleocr\  # Windows

pip uninstall paddleocr
pip install paddleocr>=2.0.1
```

#### Memory Issues
- Ensure at least 4GB RAM available
- Close other applications if needed
- Consider using mobile models for faster startup

### Platform-Specific Issues

#### WSL Issues
```bash
# Ensure WSL2 is being used
wsl --list -v

# Install required packages
sudo apt-get update
sudo apt-get install python3-dev python3-pip
```

#### macOS ARM64 (M1/M2) Issues
```bash
# Install compatible versions
pip install paddleocr --no-deps
pip install paddlepaddle>=2.4.0
```

## 📚 API Reference

### OCR Service Endpoints

#### GET /health
Returns service health status.

#### POST /ocr
Performs OCR on base64 image.

**Request:**
```json
{
  "image": "base64_encoded_image",
  "language": "en"
}
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "text": "detected text",
      "confidence": 0.95,
      "box": [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
    }
  ]
}
```

#### GET /languages
Returns supported language list.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - Powerful OCR toolkit
- [Pot-App](https://github.com/pot-app/pot-desktop) - Translation and OCR tool
- [PaddleOCR-json](https://github.com/hiroi-sora/PaddleOCR-json) - Original inspiration

## 📞 Support

- 🐛 [Report Issues](https://github.com/pot-app/pot-app-recognize-plugin-paddle/issues)
- 💬 [Discussions](https://github.com/pot-app/pot-app-recognize-plugin-paddle/discussions)
- 📖 [Pot-App Documentation](https://pot-app.com/)