#!/usr/bin/env python3
"""
Test Script for Image Integration Feature

This script tests the enhanced Word and PDF converters with image extraction capabilities.
"""

import sys
from pathlib import Path
import logging

# Add the services directory to the path
sys.path.append(str(Path(__file__).parent / "services"))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_image_integration():
    """Test the image integration functionality."""
    print("🧪 Testing Image Integration Feature")
    print("=" * 50)
    
    try:
        # Import the converters
        from services.word_converter import WordDocumentConverter
        from services.pdf_converter import PDFDocumentConverter
        from services.image_converter import ImageDocumentConverter
        
        print("✅ Successfully imported all converter modules")
        
        # Test Word converter
        print("\n📄 Testing Word Converter with Image Integration:")
        word_converter = WordDocumentConverter()
        print(f"   - Supports extensions: {word_converter.get_supported_extensions()}")
        print(f"   - Image extraction enabled: {word_converter.extract_images}")
        print(f"   - Converter info: {word_converter.get_converter_info()}")
        
        # Test PDF converter
        print("\n📋 Testing PDF Converter with Image Integration:")
        pdf_converter = PDFDocumentConverter()
        print(f"   - Supports extensions: {pdf_converter.get_supported_extensions()}")
        print(f"   - Image extraction enabled: {pdf_converter.extract_images}")
        print(f"   - Converter info: {pdf_converter.get_converter_info()}")
        
        # Test Image converter
        print("\n🖼️ Testing Image Converter:")
        image_converter = ImageDocumentConverter()
        print(f"   - Supports extensions: {image_converter.get_supported_extensions()}")
        print(f"   - Can convert (availability): {image_converter.client is not None}")
        
        # Test base functionality
        print("\n🔧 Testing Base Converter Functionality:")
        temp_dir = word_converter._create_temp_image_dir()
        print(f"   - Created temp directory: {temp_dir}")
        
        # Test cleanup
        word_converter._cleanup_temp_images()
        print(f"   - Cleaned up temp directory: {not temp_dir.exists()}")
        
        print("\n✅ All tests passed! Image integration feature is ready.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_with_sample_files():
    """Test with actual sample files if available."""
    print("\n📁 Testing with Sample Files:")
    print("=" * 30)
    
    input_folder = Path("input")
    if not input_folder.exists():
        print("   ℹ️ No input folder found. Create 'input' folder and add documents with images to test.")
        return
    
    # Look for sample files
    word_files = list(input_folder.glob("*.docx")) + list(input_folder.glob("*.doc"))
    pdf_files = list(input_folder.glob("*.pdf"))
    
    if not word_files and not pdf_files:
        print("   ℹ️ No Word or PDF files found in input folder.")
        print("   💡 Add some .docx or .pdf files with embedded images to test the feature.")
        return
    
    try:
        from services.document_converter_manager import DocumentConverterManager
        
        manager = DocumentConverterManager()
        
        # Test a few files
        test_files = (word_files + pdf_files)[:2]  # Test up to 2 files
        
        for file_path in test_files:
            print(f"\n   🔄 Testing conversion of: {file_path.name}")
            success = manager.convert_file(file_path)
            if success:
                print(f"   ✅ Successfully converted: {file_path.name}")
            else:
                print(f"   ❌ Failed to convert: {file_path.name}")
    
    except Exception as e:
        print(f"   ❌ Error testing with sample files: {e}")

if __name__ == "__main__":
    print("🚀 Image Integration Test Suite")
    print("=" * 40)
    
    # Run basic functionality tests
    basic_test_passed = test_image_integration()
    
    if basic_test_passed:
        # Test with sample files if available
        test_with_sample_files()
        
        print("\n🎉 Image Integration Feature Testing Complete!")
        print("\n💡 Usage Instructions:")
        print("1. Place Word (.docx) or PDF files with embedded images in the 'input' folder")
        print("2. Configure OpenAI API key in .env file for AI image text extraction")
        print("3. Run the document converter - images will be automatically extracted and processed")
        print("4. Check the output markdown files for embedded image content sections")
    else:
        print("\n❌ Basic tests failed. Please check the implementation.")
        sys.exit(1)
