#!/usr/bin/env python3
"""
Test script to verify the installed package works correctly
"""

def test_library_import():
    """Test that the library can be imported and basic functionality works."""
    print("Testing library import...")
    
    try:
        from documents_to_markdown import DocumentConverter, convert_document, get_supported_formats
        print("✓ Library import successful!")
        
        # Test basic functionality
        converter = DocumentConverter()
        formats = converter.get_supported_formats()
        print(f"✓ Supported formats: {len(formats)} formats")
        
        # Test convenience functions
        supported = get_supported_formats()
        print(f"✓ Convenience function works: {len(supported)} formats")
        
        # Test converter statistics
        stats = converter.get_conversion_statistics()
        print(f"✓ Statistics: {stats['total_converters']} converters available")
        
        return True
        
    except Exception as e:
        print(f"✗ Library test failed: {e}")
        return False


def test_cli_commands():
    """Test that CLI commands are available."""
    print("\nTesting CLI commands...")
    
    import subprocess
    import sys
    
    try:
        # Test documents-to-markdown command
        result = subprocess.run([sys.executable, "-m", "pip", "show", "documents-to-markdown"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Package is properly installed")
        else:
            print("✗ Package installation issue")
            return False
            
        # Test that the CLI entry point exists
        result = subprocess.run(["documents-to-markdown", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ CLI command 'documents-to-markdown' works")
        else:
            print("✗ CLI command 'documents-to-markdown' failed")
            
        # Test alternative command
        result = subprocess.run(["doc2md", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ CLI command 'doc2md' works")
        else:
            print("✗ CLI command 'doc2md' failed")
            
        return True
        
    except Exception as e:
        print(f"✗ CLI test failed: {e}")
        return False


def test_package_structure():
    """Test that the package structure is correct."""
    print("\nTesting package structure...")
    
    try:
        # Test main package
        import documents_to_markdown
        print(f"✓ Main package version: {documents_to_markdown.__version__}")
        
        # Test submodules
        from documents_to_markdown.services import document_converter_manager
        print("✓ Services module accessible")
        
        from documents_to_markdown.services.ai_services import ai_service_factory
        print("✓ AI services module accessible")
        
        # Test individual converters
        from documents_to_markdown import (
            WordDocumentConverter, 
            PDFDocumentConverter, 
            ExcelDocumentConverter,
            ImageDocumentConverter,
            PlainTextConverter
        )
        print("✓ All converter classes accessible")
        
        return True
        
    except Exception as e:
        print(f"✗ Package structure test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing Documents to Markdown Package Installation")
    print("=" * 60)
    
    tests = [
        test_library_import,
        test_cli_commands,
        test_package_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Package is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the installation.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
