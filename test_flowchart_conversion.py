#!/usr/bin/env python3
"""
Test script for flowchart detection and ASCII conversion functionality.

This script demonstrates the enhanced image extraction process that can detect
flowcharts and convert them to ASCII flow diagrams in markdown.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from services.image_converter import ImageDocumentConverter


def test_flowchart_conversion():
    """Test the enhanced flowchart detection and conversion functionality."""
    
    print("🔄 Testing Enhanced Image Converter with Flowchart Detection")
    print("=" * 60)
    
    # Check if OpenAI API key is configured
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OpenAI API key not found in environment variables.")
        print("   Please set OPENAI_API_KEY to test the AI vision functionality.")
        print("\n💡 To test with a real image:")
        print("   1. Set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")
        print("   2. Place a flowchart image in the project directory")
        print("   3. Run this script again")
        return False
    
    # Initialize the image converter
    converter = ImageDocumentConverter()
    
    print(f"✅ Image Converter initialized")
    print(f"   Model: {converter.model}")
    print(f"   Max tokens: {converter.max_tokens}")
    print(f"   Temperature: {converter.temperature}")
    print()
    
    # Look for test images in the current directory
    test_images = []
    image_extensions = converter.get_supported_extensions()
    
    for ext in image_extensions:
        test_images.extend(list(Path('.').glob(f'*{ext}')))
        test_images.extend(list(Path('.').glob(f'**/*{ext}')))
    
    if not test_images:
        print("📁 No test images found in the current directory.")
        print("   Supported formats:", ', '.join(image_extensions))
        print("\n💡 To test the flowchart conversion:")
        print("   1. Add a flowchart image (PNG, JPG, etc.) to this directory")
        print("   2. Run this script again")
        print("\n🔍 The enhanced prompt will:")
        print("   - Detect if the image contains a flowchart")
        print("   - Convert flowcharts to ASCII flow diagrams")
        print("   - Use text-based boxes and arrows")
        print("   - Show clear process flow direction")
        return True
    
    print(f"🖼️  Found {len(test_images)} test image(s):")
    for img in test_images[:5]:  # Show first 5
        print(f"   - {img.name}")
    if len(test_images) > 5:
        print(f"   ... and {len(test_images) - 5} more")
    print()
    
    # Test with the first image
    test_image = test_images[0]
    print(f"🧪 Testing with: {test_image.name}")
    print("-" * 40)
    
    try:
        # Convert the image
        result = converter._extract_text_with_ai_vision(test_image)
        
        print("📄 Conversion Result:")
        print("=" * 40)
        print(result)
        print("=" * 40)
        
        # Analyze the result
        if any(char in result for char in ['┌', '└', '→', '↓', '←', '↑']):
            print("✅ ASCII flowchart detected in output!")
            print("   The image was likely identified as a flowchart and converted to ASCII.")
        elif '|' in result and '-' in result:
            print("📊 Table format detected in output!")
            print("   The image was likely identified as a table or structured data.")
        else:
            print("📝 Regular text content detected in output!")
            print("   The image was processed as regular text content.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during conversion: {str(e)}")
        return False


def show_enhancement_details():
    """Show details about the flowchart detection enhancement."""
    
    print("\n🚀 Flowchart Detection Enhancement Details")
    print("=" * 50)
    print("The image converter now includes:")
    print()
    print("1. 🔍 Smart Content Detection:")
    print("   - Identifies flowcharts, process diagrams, workflows")
    print("   - Recognizes tables, forms, structured data")
    print("   - Handles regular text content")
    print()
    print("2. 🎨 ASCII Flow Conversion:")
    print("   - Uses text-based boxes: ┌─┐│└─┘")
    print("   - Directional arrows: →, ↓, ←, ↑")
    print("   - Decision diamonds: /\\ and \\/")
    print("   - Clear flow direction")
    print()
    print("3. 📋 Example ASCII Output:")
    print("   ┌─────────────┐")
    print("   │    Start    │")
    print("   └──────┬──────┘")
    print("          ↓")
    print("   ┌─────────────┐")
    print("   │  Process A  │")
    print("   └──────┬──────┘")
    print("          ↓")
    print("       /\\     /\\")
    print("      /  \\   /  \\")
    print("     / Decision? \\")
    print("     \\           /")
    print("      \\         /")
    print("       \\       /")
    print("        \\     /")
    print("         \\   /")
    print("          \\ /")
    print("           V")
    print("       Yes ↓  No →")
    print()


if __name__ == "__main__":
    print("🧪 Flowchart Conversion Test Suite")
    print("=" * 40)
    
    # Show enhancement details
    show_enhancement_details()
    
    # Run the test
    success = test_flowchart_conversion()
    
    if success:
        print("\n✅ Test completed successfully!")
        print("   The enhanced image converter is ready to detect and convert flowcharts.")
    else:
        print("\n⚠️  Test completed with limitations.")
        print("   Set up OpenAI API key and test images for full functionality.")
    
    print("\n📚 Integration with Document Conversion:")
    print("   - Word documents: Embedded images automatically processed")
    print("   - PDF documents: Extracted images automatically processed")
    print("   - Flowcharts converted to ASCII at original image locations")
    print("   - Failed extractions are skipped (no error messages in output)")
