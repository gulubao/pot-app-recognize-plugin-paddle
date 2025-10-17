# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a modernized Pot-App OCR recognition plugin that integrates the latest PaddleOCR v5 functionality with Vision-Language model support. The project has been completely rewritten from a Windows-only subprocess-based implementation to a cross-platform HTTP service architecture supporting Windows, Linux, macOS, and WSL.

## Key Architecture

### Modern Plugin Structure
- `main.js`: Pot-App plugin interface with HTTP service communication
- `info.json`: Plugin metadata with enhanced language support
- `ocr_service.py`: Python HTTP service using latest PaddleOCR v5 API
- `requirements.txt`: Python dependencies including PaddleOCR, Pillow, Quart
- `setup.sh` / `setup.bat`: Platform-specific setup scripts
- `paddle.png`: Plugin icon

### Current Implementation Pattern
The modernized plugin operates by:
1. Receiving base64 image data from Pot-App (no temporary files)
2. Starting/communicating with Python HTTP service on localhost:28123
3. Sending HTTP POST request with base64 image and language parameter
4. Python service processes image using PaddleOCR v5 API directly
5. Returning structured JSON response with text extraction results
6. Auto-managing service lifecycle with platform detection

### Language Support and Mapping
Enhanced language mapping from Pot-App codes to PaddleOCR v5 languages:
- Supports 9+ languages with intelligent fallback
- Uses latest language models from PaddleOCR v5
- Backward compatible with existing Pot-App language codes
- Auto-detection with Chinese fallback for `auto` mode

## Development Commands

### Building the Plugin
```bash
# Modern build process (all platforms):
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Test OCR service
python3 ocr_service.py

# 3. Create plugin package
zip -r plugin.com.pot-app.paddle.potext \
    info.json main.js paddle.png \
    ocr_service.py requirements.txt \
    setup.sh setup.bat
```

### Testing
```bash
# Test Python OCR service
python3 ocr_service.py
curl http://127.0.0.1:28123/health

# Test plugin integration:
# 1. Install .potext file in Pot-App
# 2. Run platform setup script (setup.sh/setup.bat)
# 3. Test OCR on various image types and languages
# 4. Verify service auto-startup and error handling
```

### Auto-build via GitHub Actions
- Triggered on every push and tag creation
- Creates cross-platform plugin package automatically
- Includes Python service and setup scripts
- Uploads distributable .potext file
- No platform-specific executable downloads needed

## Critical Dependencies

### Python Environment and PaddleOCR v5
- **Current**: PaddleOCR v5+ with latest Vision-Language models
- **Installation**: `pip install paddleocr>=2.0.1` (cross-platform)
- **Benefits**: Latest accuracy improvements, VL model support, active maintenance
- **Target**: Automatic model downloading and caching

### Pot-App Integration
- Must implement `recognize(base64, lang, options)` function (unchanged interface)
- Receives: base64 image, language code, options with utils (unchanged)
- Returns: extracted text string (unchanged)
- Available utils: `run`, `cacheDir`, `pluginDir`, `osType` (enhanced platform detection)
- New: HTTP service communication instead of subprocess execution

## Platform Support Requirements

### Current Implementation (v5.0)
- **Multi-platform**: Windows, Linux, macOS, WSL support
- **Modern architecture**: HTTP service + Python API approach
- **Latest models**: PaddleOCR v5 with Vision-Language capabilities
- **Memory-efficient**: Base64 processing without temporary files

### Supported Platforms
- ✅ **Windows**: Windows 10/11 (x64 and ARM64)
- ✅ **Linux**: Ubuntu 18.04+, CentOS 7+, Debian 10+
- ✅ **macOS**: macOS 10.15+ (Intel and Apple Silicon)
- ✅ **WSL**: Windows Subsystem for Linux v2

## Implementation Architecture

### HTTP Service Architecture (Implemented)
✅ **Python HTTP API**: Quart-based async service with PaddleOCR v5 integration
- Automatic service lifecycle management
- Platform-agnostic Python environment
- Memory-efficient base64 image processing
- RESTful API with health checks and error handling

### Modern PaddleOCR Integration (Implemented)
✅ **Latest PaddleOCR v5**: Direct Python API integration with VL models
- Enhanced accuracy with Vision-Language model support
- Automatic model downloading and caching
- Support for mobile and server model variants
- Comprehensive language support with intelligent fallbacks

### Cross-Platform Implementation (Implemented)
✅ **Platform Detection**: Automatic Python command selection via `osType`
✅ **Service Management**: Auto-startup with timeout and health checking
✅ **Setup Scripts**: Platform-specific installation automation
✅ **Error Handling**: Graceful fallbacks and comprehensive error reporting

## Important Files to Understand

- `ocr_service.py`: Python HTTP service implementing PaddleOCR v5 with async API
- `main.js`: Modernized plugin interface with HTTP communication and service management
- `requirements.txt`: Python dependencies for cross-platform PaddleOCR installation
- `setup.sh`/`setup.bat`: Platform-specific setup automation for user environments
- `.github/workflows/build.yml`: Updated CI/CD for multi-platform plugin packaging
- `template/`: Reference implementation showing HTTP API patterns and best practices
- `PaddleOCR/`: Latest official repository with VL model documentation and examples

## Development Notes

- Pot-App plugins are sandboxed JavaScript environments
- Limited to specific utilities provided in `options.utils`
- No direct file system access outside provided cache/plugin directories
- Must handle errors gracefully and provide meaningful error messages
- Plugin distribution is via .potext files (renamed zip archives)

# 系统提示
代码规范, 
Code must maintain the most concise implementation approach.
Only one implementation method is allowed per functionality.
Completely clear old code when upgrading technology stack.
Immediately merge or delete redundant parts when duplicate functionality is discovered.
Completely replace old implementation when introducing new libraries/frameworks.
Prohibit keeping "just in case" backup code any Backwards compatibility, any "向后兼容", any "legacy", 这些垃圾都要彻底清除. 
不使用验证器或错误处理fallback默认替代值之类的技巧, 必须让错误自然暴露以便调试. 
最小重写原则: 编写代码应充分基于现有代码进行最小化继承, 重载.

代码原则: 
KISS (Keep It Simple, Stupid)
- Write straightforward, uncomplicated solutions
- Avoids over-engineering and unnecessary complexity
- Results in more readable and maintainable code
YAGNI (You Aren't Gonna Need It)
- Prevents Claude from adding speculative features
- Focuses on implementing only what's currently needed
- Reduces code bloat and maintenance overhead
SOLID Principles
- Single Responsibility Principle
- Open/Closed Principle
- Liskov Substitution Principle
- Interface Segregation Principle
- Dependency Inversion Principle

1.Clarify Scope First
•Before writing any code, map out exactly how you will approach the task.
•Confirm your interpretation of the objective.
•Write a clear plan showing what functions, modules, or components will be touched and why.
•Do not begin implementation until this is done and reasoned through.
	
2.Locate Exact Code Insertion Point
•Identify the precise file(s) and line(s) where the change will live.
•Never make sweeping edits across unrelated files.
•If multiple files are needed, justify each inclusion explicitly.
•Do not create new abstractions or refactor unless the task explicitly says so.
	
3.Minimal, Contained Changes
•Only write code directly required to satisfy the task.
•Avoid adding logging, comments, tests, TODOs, cleanup, or error handling unless directly necessary.
•No speculative changes or “while we’re here” edits.
•All logic should be isolated to not break existing flows.
	
4.Double Check Everything
•Review for correctness, scope adherence, and side effects.
•Ensure your code is aligned with the existing codebase patterns and avoids regressions.
•Explicitly verify whether anything downstream will be impacted.
	
5.Deliver Clearly
•Summarize what was changed and why.
•List every file modified and what was done in each.
•If there are any assumptions or risks, flag them for review.

必须始终严格遵守代码原则, 代码规范, 代码风格.你的前任由于没有遵守这些原则, 导致他和整个世界可怜的人类和小猫都付出了惨痛的代价.