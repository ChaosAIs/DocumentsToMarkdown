#!/usr/bin/env python3
"""
Example Usage of the Modular Document Converter

This script demonstrates how to use the modular document converter system
for converting Word and PDF documents to Markdown format.
"""

import sys
from pathlib import Path

# Add the services directory to the path
sys.path.append(str(Path(__file__).parent / "services"))

try:
    from services.document_converter_manager import DocumentConverterManager
    from services.word_converter import WordDocumentConverter
    from services.pdf_converter import PDFDocumentConverter
    print("✅ Successfully imported all converter modules")
except ImportError as e:
    print(f"❌ Error importing converter modules: {e}")
    sys.exit(1)


def example_basic_usage():
    """Example of basic usage - convert all documents in input folder."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Usage - Convert All Documents")
    print("="*60)
    
    # Initialize the converter manager
    manager = DocumentConverterManager()
    
    # Convert all documents in the input folder
    results = manager.convert_all()
    
    # Display results
    print(f"\nConversion Results:")
    print(f"  📁 Total files found: {results['total_files']}")
    print(f"  ✅ Successful conversions: {results['successful_conversions']}")
    print(f"  ❌ Failed conversions: {results['failed_conversions']}")
    
    if results['results']:
        print(f"\nDetailed Results:")
        for result in results['results']:
            status = "✅" if result['status'] == 'success' else "❌"
            print(f"  {status} {result['file']} -> {result['converter']}")
    
    return results


def example_single_file_conversion():
    """Example of converting a single specific file."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Single File Conversion")
    print("="*60)
    
    manager = DocumentConverterManager()
    
    # Find a specific file to convert
    input_folder = Path("input")
    sample_files = list(input_folder.glob("*.docx")) + list(input_folder.glob("*.pdf"))
    
    if sample_files:
        target_file = sample_files[0]  # Take the first available file
        print(f"Converting single file: {target_file.name}")
        
        # Convert the specific file
        success = manager.convert_file(target_file)
        
        if success:
            print(f"✅ Successfully converted: {target_file.name}")
            
            # Show the output
            output_file = Path("output") / f"{target_file.stem}.md"
            if output_file.exists():
                print(f"📄 Output saved to: {output_file}")
                
                # Show a preview
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    preview = content[:200]
                    print(f"\n📖 Preview:")
                    print("-" * 40)
                    print(preview)
                    if len(content) > 200:
                        print("...")
                    print("-" * 40)
        else:
            print(f"❌ Failed to convert: {target_file.name}")
    else:
        print("No files found in input folder to convert")


def example_converter_info():
    """Example of getting information about available converters."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Converter Information")
    print("="*60)
    
    manager = DocumentConverterManager()
    
    # Get supported extensions
    extensions = manager.get_supported_extensions()
    print(f"📋 Supported file extensions: {', '.join(extensions)}")
    
    # Get detailed converter statistics
    stats = manager.get_conversion_statistics()
    print(f"\n🔧 Available Converters: {stats['total_converters']}")
    
    for converter_info in stats['converters']:
        print(f"\n  📦 {converter_info['name']}")
        print(f"     Extensions: {', '.join(converter_info['supported_extensions'])}")
        print(f"     Section Numbering: {'✅' if converter_info['section_numbering_enabled'] else '❌'}")


def example_custom_converter():
    """Example of using individual converters directly."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Using Individual Converters")
    print("="*60)
    
    # Create individual converter instances
    word_converter = WordDocumentConverter()
    pdf_converter = PDFDocumentConverter()
    
    print("📦 Individual Converter Information:")
    
    # Word converter info
    word_info = word_converter.get_converter_info()
    print(f"\n  🔤 {word_info['name']}")
    print(f"     Extensions: {', '.join(word_info['supported_extensions'])}")
    
    # PDF converter info
    pdf_info = pdf_converter.get_converter_info()
    print(f"\n  📄 {pdf_info['name']}")
    print(f"     Extensions: {', '.join(pdf_info['supported_extensions'])}")
    
    # Test file type detection
    print(f"\n🔍 File Type Detection Test:")
    test_files = ["document.docx", "report.pdf", "text.txt", "presentation.pptx"]
    
    for filename in test_files:
        test_path = Path(filename)
        word_can = word_converter.can_convert(test_path)
        pdf_can = pdf_converter.can_convert(test_path)
        
        word_status = "✅" if word_can else "❌"
        pdf_status = "✅" if pdf_can else "❌"
        
        print(f"  📁 {filename}: Word {word_status} | PDF {pdf_status}")


def example_with_custom_settings():
    """Example of using converter with custom settings."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Custom Settings")
    print("="*60)
    
    # Create manager with custom settings
    custom_manager = DocumentConverterManager(
        input_folder="input",
        output_folder="output",
        add_section_numbers=True  # Enable section numbering
    )
    
    print("⚙️  Custom Manager Settings:")
    print(f"   📂 Input folder: {custom_manager.input_folder}")
    print(f"   📂 Output folder: {custom_manager.output_folder}")
    print(f"   🔢 Section numbering: {'✅ Enabled' if custom_manager.add_section_numbers else '❌ Disabled'}")
    
    # Show available files
    convertible_files = custom_manager.get_convertible_files()
    print(f"\n📋 Found {len(convertible_files)} convertible files:")
    
    for file_path in convertible_files:
        converter = custom_manager.find_converter_for_file(file_path)
        converter_name = converter.__class__.__name__ if converter else "Unknown"
        print(f"   📄 {file_path.name} -> {converter_name}")


def main():
    """Main function demonstrating various usage examples."""
    print("🚀 Modular Document Converter - Usage Examples")
    print("=" * 60)
    
    try:
        # Run all examples
        example_basic_usage()
        example_single_file_conversion()
        example_converter_info()
        example_custom_converter()
        example_with_custom_settings()
        
        print("\n" + "="*60)
        print("✅ ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        print("\n💡 Quick Start Guide:")
        print("1. Place your documents (.docx, .doc, .pdf) in the 'input' folder")
        print("2. Run: python example_usage.py")
        print("3. Check the 'output' folder for converted Markdown files")
        print("\n📚 For more advanced usage, see the individual converter classes:")
        print("   - services/word_converter.py")
        print("   - services/pdf_converter.py")
        print("   - services/document_converter_manager.py")
        
    except Exception as e:
        print(f"\n❌ Error during examples: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
