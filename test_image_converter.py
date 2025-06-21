#!/usr/bin/env python3
"""
Test script for the Image Document Converter

This script tests the new image-to-markdown conversion feature using AI vision.
"""

import sys
import os
from pathlib import Path

# Add the services directory to the path
sys.path.append(str(Path(__file__).parent / "services"))

try:
    from services.document_converter_manager import DocumentConverterManager
    from services.image_converter import ImageDocumentConverter
    print("✅ Successfully imported image converter modules")
except ImportError as e:
    print(f"❌ Error importing image converter modules: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)


def check_environment_setup():
    """Check if the environment is properly configured for image conversion."""
    print("\n" + "="*60)
    print("CHECKING ENVIRONMENT SETUP")
    print("="*60)
    
    # Check for .env file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
    else:
        print("❌ .env file not found")
        print("   Copy .env.template to .env and add your OpenAI API key")
        return False
    
    # Check for OpenAI API key
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and api_key != 'your_openai_api_key_here':
        print("✅ OpenAI API key configured")
        return True
    else:
        print("❌ OpenAI API key not configured")
        print("   Add your OpenAI API key to the .env file")
        return False


def test_image_converter_initialization():
    """Test image converter initialization."""
    print("\n" + "="*60)
    print("TESTING IMAGE CONVERTER INITIALIZATION")
    print("="*60)
    
    try:
        converter = ImageDocumentConverter()
        
        # Check supported extensions
        extensions = converter.get_supported_extensions()
        print(f"✅ Supported extensions: {extensions}")
        
        # Check converter info
        info = converter.get_converter_info()
        print(f"✅ Converter name: {info['name']}")
        print(f"✅ Converter description: {info['description']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing image converter: {e}")
        return False


def test_document_manager_with_images():
    """Test document manager with image support."""
    print("\n" + "="*60)
    print("TESTING DOCUMENT MANAGER WITH IMAGE SUPPORT")
    print("="*60)
    
    try:
        manager = DocumentConverterManager()
        
        # Check supported extensions
        extensions = manager.get_supported_extensions()
        print(f"✅ All supported extensions: {extensions}")
        
        # Check if image extensions are included
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp']
        supported_image_extensions = [ext for ext in image_extensions if ext in extensions]
        
        if supported_image_extensions:
            print(f"✅ Image extensions supported: {supported_image_extensions}")
        else:
            print("❌ No image extensions found in supported formats")
            return False
        
        # Get converter statistics
        stats = manager.get_conversion_statistics()
        print(f"✅ Total converters: {stats['total_converters']}")
        
        # Check for image converter
        image_converter_found = False
        for converter_info in stats['converters']:
            if 'Image' in converter_info['name']:
                print(f"✅ Image converter found: {converter_info['name']}")
                image_converter_found = True
                break
        
        if not image_converter_found:
            print("❌ Image converter not found in manager")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing document manager: {e}")
        return False


def test_image_file_detection():
    """Test image file detection in input folder."""
    print("\n" + "="*60)
    print("TESTING IMAGE FILE DETECTION")
    print("="*60)
    
    try:
        manager = DocumentConverterManager()
        
        # Get all files in input folder
        input_folder = Path("input")
        if not input_folder.exists():
            print("❌ Input folder not found")
            return False
        
        all_files = list(input_folder.iterdir())
        image_files = [f for f in all_files if f.suffix.lower() in manager.get_supported_extensions() 
                      and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp']]
        
        print(f"📁 Total files in input folder: {len(all_files)}")
        print(f"🖼️  Image files found: {len(image_files)}")
        
        if image_files:
            print("   Image files:")
            for img_file in image_files:
                print(f"   - {img_file.name}")
        else:
            print("   No image files found in input folder")
            print("   Add some image files (.jpg, .png, etc.) to test conversion")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking image files: {e}")
        return False


def create_sample_usage_guide():
    """Create a sample usage guide for image conversion."""
    print("\n" + "="*60)
    print("CREATING SAMPLE USAGE GUIDE")
    print("="*60)
    
    guide_content = """# Image to Markdown Conversion Guide

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure OpenAI API**:
   - Copy `.env.template` to `.env`
   - Get your OpenAI API key from: https://platform.openai.com/api-keys
   - Add your API key to `.env`:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```

3. **Add Image Files**:
   - Place your image files in the `input` folder
   - Supported formats: JPG, PNG, GIF, BMP, TIFF, WebP

4. **Run Conversion**:
   ```bash
   python document_converter_v2.py
   ```

## Example Usage

```python
from services.document_converter_manager import DocumentConverterManager

# Initialize converter manager
manager = DocumentConverterManager()

# Convert all documents (including images)
results = manager.convert_all()

print(f"Converted {results['successful_conversions']} files")
```

## Features

- **AI-Powered**: Uses OpenAI GPT-4 Vision for text extraction
- **Smart Formatting**: Preserves document structure and formatting
- **Multiple Formats**: Supports all common image formats
- **Automatic Optimization**: Resizes large images for API efficiency
- **Batch Processing**: Convert multiple images at once

## Tips for Best Results

1. **High Quality Images**: Use clear, high-resolution images
2. **Good Lighting**: Ensure text is clearly visible
3. **Proper Orientation**: Make sure images are right-side up
4. **Clean Background**: Avoid cluttered backgrounds around text
5. **Standard Fonts**: Common fonts work better than decorative ones

## Troubleshooting

- **API Key Issues**: Make sure your OpenAI API key is valid and has credits
- **Large Images**: Images are automatically resized if too large
- **Poor Quality**: Try enhancing image quality before conversion
- **Complex Layouts**: Simple layouts work better than complex designs
"""
    
    try:
        guide_path = Path("IMAGE_CONVERSION_GUIDE.md")
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print(f"✅ Created usage guide: {guide_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating usage guide: {e}")
        return False


def main():
    """Run all image converter tests."""
    print("Image Document Converter - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Environment Setup", check_environment_setup),
        ("Image Converter Initialization", test_image_converter_initialization),
        ("Document Manager Integration", test_document_manager_with_images),
        ("Image File Detection", test_image_file_detection),
        ("Usage Guide Creation", create_sample_usage_guide)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running test: {test_name}")
        try:
            if test_func():
                passed_tests += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    print(f"Tests passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("\n💡 Next Steps:")
        print("1. Add image files to the 'input' folder")
        print("2. Run: python document_converter_v2.py")
        print("3. Check the 'output' folder for converted Markdown files")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        print("\n🔧 Common fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure OpenAI API key in .env file")
        print("3. Make sure input/output folders exist")
    
    return passed_tests == total_tests


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
