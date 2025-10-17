#!/usr/bin/env python3
"""
PaddleOCR HTTP Service for Pot-App Plugin
Provides a lightweight HTTP API for OCR recognition using latest PaddleOCR.
"""

import asyncio
import base64
import json
import logging
import os
import sys
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional

try:
    from PIL import Image
    from paddleocr import PaddleOCR
    from quart import Quart, request, jsonify
    import uvloop
except ImportError as e:
    print(f"Missing dependencies. Please run: pip install paddleocr pillow quart uvloop")
    print(f"Error: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Language mapping from Pot-App to PaddleOCR
LANGUAGE_MAP = {
    "chinese": "ch",
    "chinese_cht": "chinese_cht", 
    "en": "en",
    "japan": "japan",
    "korean": "korean",
    "french_v2": "fr",
    "cyrillic": "ru",
    "german_v2": "german",
    "auto": "ch"  # Default fallback
}

class OCRService:
    def __init__(self):
        self.ocr_instances: Dict[str, PaddleOCR] = {}
        self.default_lang = "en"
        
    def get_ocr_instance(self, lang: str) -> PaddleOCR:
        """Get or create OCR instance for specified language."""
        paddle_lang = LANGUAGE_MAP.get(lang, self.default_lang)
        
        if paddle_lang not in self.ocr_instances:
            logger.info(f"Initializing PaddleOCR for language: {paddle_lang}")
            try:
                # Use PP-OCRv5 with mobile models for better performance
                self.ocr_instances[paddle_lang] = PaddleOCR(
                    use_angle_cls=True,
                    lang=paddle_lang,
                    use_gpu=False,  # CPU for better compatibility
                    show_log=False,
                    ocr_version="PP-OCRv5"
                )
                logger.info(f"Successfully initialized PaddleOCR for {paddle_lang}")
            except Exception as e:
                logger.error(f"Failed to initialize PaddleOCR for {paddle_lang}: {e}")
                # Fallback to English if the language fails
                if paddle_lang != "en":
                    paddle_lang = "en"
                    self.ocr_instances[paddle_lang] = PaddleOCR(
                        use_angle_cls=True,
                        lang="en",
                        use_gpu=False,
                        show_log=False
                    )
                else:
                    raise
                    
        return self.ocr_instances[paddle_lang]
    
    def process_base64_image(self, base64_data: str, lang: str) -> List[Dict]:
        """Process base64 image and return OCR results."""
        try:
            # Remove data URL prefix if present
            if base64_data.startswith('data:image'):
                base64_data = base64_data.split(',')[1]
            
            # Decode base64 to image
            image_bytes = base64.b64decode(base64_data)
            image = Image.open(BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Get OCR instance and perform recognition
            ocr = self.get_ocr_instance(lang)
            results = ocr.ocr(image, cls=True)
            
            # Parse results into structured format
            parsed_results = []
            if results and results[0]:
                for line in results[0]:
                    if line:
                        box, (text, confidence) = line
                        parsed_results.append({
                            "text": text,
                            "confidence": confidence,
                            "box": box
                        })
            
            return parsed_results
            
        except Exception as e:
            logger.error(f"OCR processing error: {e}")
            raise

# Create Quart app
app = Quart(__name__)
ocr_service = OCRService()

@app.route('/health', methods=['GET'])
async def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "PaddleOCR"})

@app.route('/ocr', methods=['POST'])
async def recognize_text():
    """Main OCR endpoint."""
    try:
        data = await request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({"error": "Missing image data"}), 400
        
        base64_image = data['image']
        language = data.get('language', 'en')
        
        # Process OCR
        results = ocr_service.process_base64_image(base64_image, language)
        
        # Format response similar to PaddleOCR-json output
        response = {
            "status": "success",
            "data": results
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({
            "status": "error", 
            "error": str(e)
        }), 500

@app.route('/languages', methods=['GET'])
async def get_supported_languages():
    """Get list of supported languages."""
    return jsonify({
        "languages": list(LANGUAGE_MAP.keys()),
        "default": ocr_service.default_lang
    })

def main():
    """Main entry point."""
    port = int(os.environ.get('PORT', 28123))
    host = os.environ.get('HOST', '127.0.0.1')
    
    logger.info(f"Starting PaddleOCR service on {host}:{port}")
    
    # Use uvloop for better performance
    if sys.platform != 'win32':
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    
    app.run(host=host, port=port, debug=False)

if __name__ == '__main__':
    main()