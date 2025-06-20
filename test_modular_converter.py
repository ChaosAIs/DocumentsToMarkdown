#!/usr/bin/env python3
"""
Test script for the modular Document Converter Manager

This script tests the new modular converter system with both Word and PDF documents.
"""

import sys
from pathlib import Path

# Add the services directory to the path
sys.path.append(str(Path(__file__).parent / "services"))

try:
    from services.document_converter_manager import DocumentConverterManager
    print("Successfully imported DocumentConverterManager")
except ImportError as e:
    print(f"Error importing DocumentConverterManager: {e}")
    sys.exit(1)


def test_modular_converter():
    """Test the modular converter system."""
    print("Modular Document Converter Manager - Test")
    print("=" * 50)
    
    try:
        # Initialize the converter manager
        print("\n1. Initializing DocumentConverterManager...")
        manager = DocumentConverterManager()
        
        # Get supported extensions
        print("\n2. Getting supported extensions...")
        extensions = manager.get_supported_extensions()
        print(f"Supported extensions: {extensions}")
        
        # Get conversion statistics
        print("\n3. Getting converter statistics...")
        stats = manager.get_conversion_statistics()
        print(f"Total converters: {stats['total_converters']}")
        print("Available converters:")
        for converter_info in stats['converters']:
            print(f"  - {converter_info['name']}: {converter_info['supported_extensions']}")
        
        # Find convertible files
        print("\n4. Finding convertible files...")
        convertible_files = manager.get_convertible_files()
        print(f"Found {len(convertible_files)} convertible files:")
        for file_path in convertible_files:
            converter = manager.find_converter_for_file(file_path)
            converter_name = converter.__class__.__name__ if converter else "None"
            print(f"  - {file_path.name} -> {converter_name}")
        
        # Test conversion of all files
        if convertible_files:
            print("\n5. Converting all files...")
            results = manager.convert_all()
            
            print(f"\nConversion Results:")
            print(f"  Total files: {results['total_files']}")
            print(f"  Successful: {results['successful_conversions']}")
            print(f"  Failed: {results['failed_conversions']}")
            
            print("\nDetailed results:")
            for result in results['results']:
                status_icon = "✅" if result['status'] == 'success' else "❌"
                print(f"  {status_icon} {result['file']} ({result['converter']})")
            
            # Show sample output if any conversions were successful
            if results['successful_conversions'] > 0:
                print("\n6. Sample output preview:")
                output_folder = Path("output")
                for md_file in output_folder.glob("*.md"):
                    print(f"\n--- {md_file.name} ---")
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Show first 300 characters
                        preview = content[:300]
                        print(preview)
                        if len(content) > 300:
                            print("...")
                        print(f"[Full content in: {md_file}]")
                    break  # Only show first file
        else:
            print("No convertible files found in input folder.")
            print("Please add some .docx, .doc, or .pdf files to the 'input' folder.")
        
        print("\n✅ Modular converter test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


def test_individual_converters():
    """Test individual converter functionality."""
    print("\n" + "=" * 50)
    print("Testing Individual Converters")
    print("=" * 50)
    
    try:
        from services.word_converter import WordDocumentConverter
        from services.pdf_converter import PDFDocumentConverter
        
        # Test Word converter
        print("\n1. Testing WordDocumentConverter...")
        word_converter = WordDocumentConverter()
        word_info = word_converter.get_converter_info()
        print(f"Word converter info: {word_info}")
        
        # Test PDF converter
        print("\n2. Testing PDFDocumentConverter...")
        pdf_converter = PDFDocumentConverter()
        pdf_info = pdf_converter.get_converter_info()
        print(f"PDF converter info: {pdf_info}")
        
        # Test file type detection
        print("\n3. Testing file type detection...")
        test_files = [
            Path("test.docx"),
            Path("test.doc"),
            Path("test.pdf"),
            Path("test.txt")
        ]
        
        for test_file in test_files:
            word_can_convert = word_converter.can_convert(test_file)
            pdf_can_convert = pdf_converter.can_convert(test_file)
            print(f"  {test_file.name}: Word={word_can_convert}, PDF={pdf_can_convert}")
        
        print("\n✅ Individual converter tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Individual converter test failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_modular_converter()
    test_individual_converters()
