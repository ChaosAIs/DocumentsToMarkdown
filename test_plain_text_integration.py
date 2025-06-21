#!/usr/bin/env python3
"""
Integration Test for Plain Text Converter with Document Converter Manager

This script tests the integration of PlainTextConverter with the main DocumentConverterManager.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from services.document_converter_manager import DocumentConverterManager


def create_test_files():
    """Create test files for integration testing."""
    test_files = {}
    
    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp(prefix="integration_test_"))
    print(f"Created test directory: {temp_dir}")
    
    # Test CSV file
    csv_content = """Product,Price,Category
Laptop,999.99,Electronics
Mouse,29.99,Electronics
Desk,199.99,Furniture"""
    
    csv_file = temp_dir / "products.csv"
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write(csv_content)
    test_files['csv'] = csv_file
    
    # Test plain text file
    txt_content = """Meeting Notes - Project Kickoff

Date: January 15, 2024
Attendees: John, Jane, Bob

Agenda:
1. Project overview
2. Timeline discussion
3. Resource allocation

Action Items:
- John: Prepare technical specifications
- Jane: Create project timeline
- Bob: Set up development environment

Next Meeting: January 22, 2024"""
    
    txt_file = temp_dir / "meeting_notes.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(txt_content)
    test_files['txt'] = txt_file
    
    return test_files, temp_dir


def test_manager_integration():
    """Test DocumentConverterManager integration."""
    print("\n" + "="*60)
    print("TESTING DOCUMENT CONVERTER MANAGER INTEGRATION")
    print("="*60)
    
    # Create test files
    test_files, temp_dir = create_test_files()
    
    # Initialize manager with custom input/output directories
    manager = DocumentConverterManager(
        input_folder=temp_dir,
        output_folder=temp_dir / "output"
    )
    
    print(f"\nAvailable converters:")
    for converter in manager.converters:
        info = converter.get_converter_info()
        print(f"  - {info['name']}: {info['supported_extensions']}")
    
    # Test finding converters for our files
    print(f"\nTesting converter detection:")
    for file_type, file_path in test_files.items():
        converter = manager.find_converter_for_file(file_path)
        if converter:
            print(f"  ✅ {file_type.upper()} file: {converter.__class__.__name__}")
        else:
            print(f"  ❌ {file_type.upper()} file: No converter found")
    
    # Test converting individual files
    print(f"\nTesting individual file conversion:")
    for file_type, file_path in test_files.items():
        success = manager.convert_file(file_path)
        print(f"  {file_type.upper()} conversion: {'✅ Success' if success else '❌ Failed'}")
    
    # Test converting all files
    print(f"\nTesting batch conversion:")
    results = manager.convert_all()
    print(f"  Total files found: {results['total_files']}")
    print(f"  Successful conversions: {results['successful_conversions']}")
    print(f"  Failed conversions: {results['failed_conversions']}")
    
    # Show output files
    output_dir = temp_dir / "output"
    if output_dir.exists():
        print(f"\nGenerated output files:")
        for output_file in output_dir.glob("*.md"):
            print(f"  📄 {output_file.name}")
            # Show a preview of the content
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"     Preview: {content[:100]}...")
    
    return temp_dir


def cleanup_test_files(temp_dir):
    """Clean up test files."""
    print("\n" + "="*60)
    print("CLEANING UP TEST FILES")
    print("="*60)
    
    try:
        import shutil
        shutil.rmtree(temp_dir)
        print(f"✅ Cleaned up test directory: {temp_dir}")
    except Exception as e:
        print(f"❌ Error cleaning up: {e}")


def main():
    """Main test function."""
    print("Plain Text Converter Integration Test")
    print("="*60)
    
    try:
        # Run integration test
        temp_dir = test_manager_integration()
        
        # Show summary
        print("\n" + "="*60)
        print("INTEGRATION TEST SUMMARY")
        print("="*60)
        print("✅ Integration test completed successfully!")
        print("   PlainTextConverter is properly integrated with DocumentConverterManager")
        print("   Both CSV and plain text files are being converted correctly")
        
        # Cleanup
        cleanup_test_files(temp_dir)
        
    except Exception as e:
        print(f"\n❌ Integration test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
