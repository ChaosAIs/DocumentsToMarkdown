#!/usr/bin/env python3
"""
Test Script for AI Services

This script tests the AI service implementations to ensure both OpenAI and OLLAMA
integrations work correctly with the DocumentsToMarkdown converter.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_ai_service_availability():
    """Test which AI services are available."""
    print("🔍 Testing AI Service Availability")
    print("=" * 50)
    
    try:
        from services.ai_services import ai_service_factory
        
        # Check availability of all services
        availability = ai_service_factory.list_available_services()
        
        for service_name, is_available in availability.items():
            status = "✅ Available" if is_available else "❌ Not Available"
            print(f"{service_name.upper()}: {status}")
        
        return availability
        
    except Exception as e:
        print(f"❌ Error checking AI service availability: {e}")
        return {}

def test_service_creation(service_type):
    """Test creating a specific AI service."""
    print(f"\n🧪 Testing {service_type.upper()} Service Creation")
    print("=" * 50)
    
    try:
        from services.ai_services import ai_service_factory, AIServiceUnavailableError
        
        service = ai_service_factory.create_service(service_type)
        print(f"✅ {service_type.upper()} service created successfully")
        print(f"   Service: {service.get_service_name()}")
        print(f"   Model: {service.get_model_name()}")
        return service
        
    except AIServiceUnavailableError as e:
        print(f"❌ {service_type.upper()} service not available: {e}")
        return None
    except Exception as e:
        print(f"❌ Error creating {service_type.upper()} service: {e}")
        return None

def test_image_converter(ai_service_type=None):
    """Test the image converter with specified AI service."""
    service_name = ai_service_type.upper() if ai_service_type else "AUTO-DETECT"
    print(f"\n🖼️  Testing Image Converter ({service_name})")
    print("=" * 50)
    
    try:
        from services.image_converter import ImageDocumentConverter
        
        # Create converter
        converter = ImageDocumentConverter(ai_service_type=ai_service_type)
        
        if not converter.ai_service:
            print(f"❌ No AI service available for image conversion")
            return False
        
        print(f"✅ Image converter created successfully")
        print(f"   AI Service: {converter.ai_service.get_service_name()}")
        print(f"   Model: {converter.ai_service.get_model_name()}")
        
        # Test supported extensions
        extensions = converter.get_supported_extensions()
        print(f"   Supported extensions: {', '.join(extensions)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing image converter: {e}")
        return False

def test_environment_configuration():
    """Test environment configuration."""
    print("\n⚙️  Testing Environment Configuration")
    print("=" * 50)
    
    load_dotenv()
    
    # Check key environment variables
    config_items = [
        ("AI_SERVICE", "AI service selection"),
        ("OPENAI_API_KEY", "OpenAI API key"),
        ("OPENAI_MODEL", "OpenAI model"),
        ("OLLAMA_BASE_URL", "OLLAMA base URL"),
        ("OLLAMA_MODEL", "OLLAMA model"),
    ]
    
    for env_var, description in config_items:
        value = os.getenv(env_var)
        if value:
            # Mask API keys for security
            if "API_KEY" in env_var and len(value) > 10:
                display_value = f"{value[:8]}...{value[-4:]}"
            else:
                display_value = value
            print(f"✅ {env_var}: {display_value}")
        else:
            print(f"⚠️  {env_var}: Not set")

def create_test_image():
    """Create a simple test image for testing."""
    print("\n🎨 Creating Test Image")
    print("=" * 50)
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple test image with text
        img = Image.new('RGB', (400, 200), color='white')
        draw = ImageDraw.Draw(img)
        
        # Add some text
        text = "Hello World!\nThis is a test image\nfor AI conversion."
        
        try:
            # Try to use a default font
            font = ImageFont.load_default()
        except:
            font = None
        
        # Draw text
        draw.text((20, 50), text, fill='black', font=font)
        
        # Save test image
        test_image_path = Path("test_image.png")
        img.save(test_image_path)
        
        print(f"✅ Test image created: {test_image_path}")
        return test_image_path
        
    except ImportError:
        print("⚠️  PIL not available, cannot create test image")
        return None
    except Exception as e:
        print(f"❌ Error creating test image: {e}")
        return None

def test_image_conversion(test_image_path, ai_service_type=None):
    """Test actual image conversion."""
    if not test_image_path or not test_image_path.exists():
        print("⚠️  No test image available for conversion test")
        return False
    
    service_name = ai_service_type.upper() if ai_service_type else "AUTO-DETECT"
    print(f"\n🔄 Testing Image Conversion ({service_name})")
    print("=" * 50)
    
    try:
        from services.image_converter import ImageDocumentConverter
        
        converter = ImageDocumentConverter(ai_service_type=ai_service_type)
        
        if not converter.ai_service:
            print(f"❌ No AI service available")
            return False
        
        print(f"Converting test image using {converter.ai_service.get_service_name()}...")
        
        # Convert the image
        result = converter._convert_document_to_markdown(test_image_path)
        
        if result and len(result.strip()) > 0:
            print("✅ Image conversion successful!")
            print("\n📄 Conversion Result:")
            print("-" * 30)
            # Show first 200 characters of result
            preview = result[:200] + "..." if len(result) > 200 else result
            print(preview)
            print("-" * 30)
            return True
        else:
            print("❌ Image conversion returned empty result")
            return False
            
    except Exception as e:
        print(f"❌ Error during image conversion: {e}")
        return False

def cleanup_test_files():
    """Clean up test files."""
    test_files = ["test_image.png"]
    for file_name in test_files:
        file_path = Path(file_name)
        if file_path.exists():
            file_path.unlink()
            print(f"🧹 Cleaned up: {file_name}")

def main():
    """Main test function."""
    print("🚀 AI Services Test Suite")
    print("=" * 60)
    print("This script tests the AI service implementations for DocumentsToMarkdown")
    print()
    
    # Test environment configuration
    test_environment_configuration()
    
    # Test AI service availability
    availability = test_ai_service_availability()
    
    # Test service creation
    services_to_test = []
    for service_type in ['ollama', 'openai']:
        if availability.get(service_type, False):
            service = test_service_creation(service_type)
            if service:
                services_to_test.append(service_type)
    
    # Test image converter creation
    test_image_converter()  # Auto-detect
    for service_type in services_to_test:
        test_image_converter(service_type)
    
    # Create test image
    test_image_path = create_test_image()
    
    # Test actual conversion if we have available services
    if test_image_path and services_to_test:
        print(f"\n🎯 Running Conversion Tests")
        print("=" * 50)
        
        # Test auto-detection first
        test_image_conversion(test_image_path)
        
        # Test specific services
        for service_type in services_to_test:
            test_image_conversion(test_image_path, service_type)
    
    # Cleanup
    cleanup_test_files()
    
    # Summary
    print(f"\n📊 Test Summary")
    print("=" * 50)
    print(f"Available services: {', '.join(services_to_test) if services_to_test else 'None'}")
    
    if not services_to_test:
        print("\n⚠️  No AI services are available!")
        print("To set up AI services:")
        print("1. For OLLAMA: See OLLAMA_SETUP_GUIDE.md")
        print("2. For OpenAI: Add OPENAI_API_KEY to .env file")
    else:
        print(f"\n✅ AI services are working correctly!")
        print("You can now use the DocumentsToMarkdown converter with AI-powered image conversion.")

if __name__ == "__main__":
    main()
