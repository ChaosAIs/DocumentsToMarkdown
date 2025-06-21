#!/usr/bin/env python3
"""
Test Script for Plain Text Document Converter

This script tests the PlainTextConverter functionality including:
- CSV to markdown table conversion
- Plain text to markdown conversion
- AI-enhanced text analysis (when available)
- Fallback behavior when AI is disabled
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from services.plain_text_converter import PlainTextConverter


def create_test_files():
    """Create test files for conversion testing."""
    test_files = {}
    
    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp(prefix="plain_text_test_"))
    print(f"Created test directory: {temp_dir}")
    
    # Test CSV file
    csv_content = """Name,Age,City,Country
John Doe,30,New York,USA
Jane Smith,25,London,UK
Bob Johnson,35,Toronto,Canada
Alice Brown,28,Sydney,Australia"""
    
    csv_file = temp_dir / "test_data.csv"
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write(csv_content)
    test_files['csv'] = csv_file
    
    # Test TSV file
    tsv_content = """Product	Price	Category	Stock
Laptop	999.99	Electronics	50
Mouse	29.99	Electronics	200
Desk	199.99	Furniture	25
Chair	149.99	Furniture	30"""
    
    tsv_file = temp_dir / "inventory.tsv"
    with open(tsv_file, 'w', encoding='utf-8') as f:
        f.write(tsv_content)
    test_files['tsv'] = tsv_file
    
    # Test plain text file
    txt_content = """Project Documentation

Introduction
This document outlines the key features and implementation details of our new project.

Features
- User authentication system
- Real-time data processing
- Advanced reporting capabilities
- Mobile-responsive design

Implementation Notes
The system is built using modern web technologies and follows best practices for security and performance.

Database Design
We use a relational database with the following main tables:
- Users: stores user account information
- Sessions: manages user sessions
- Data: contains the main application data
- Reports: stores generated reports

Conclusion
This project represents a significant step forward in our technology stack and will provide substantial value to our users."""
    
    txt_file = temp_dir / "project_docs.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(txt_content)
    test_files['txt'] = txt_file
    
    # Test log file
    log_content = """2024-01-15 10:30:15 INFO Application started
2024-01-15 10:30:16 INFO Database connection established
2024-01-15 10:30:20 INFO User authentication module loaded
2024-01-15 10:35:42 WARN High memory usage detected: 85%
2024-01-15 10:40:15 ERROR Failed to process request: timeout
2024-01-15 10:40:16 INFO Retrying request processing
2024-01-15 10:40:18 INFO Request processed successfully
2024-01-15 11:00:00 INFO Hourly backup completed"""
    
    log_file = temp_dir / "application.log"
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(log_content)
    test_files['log'] = log_file
    
    # Test empty file
    empty_file = temp_dir / "empty.txt"
    with open(empty_file, 'w', encoding='utf-8') as f:
        f.write("")
    test_files['empty'] = empty_file
    
    return test_files, temp_dir


def test_converter_initialization():
    """Test converter initialization with and without AI."""
    print("\n" + "="*60)
    print("TESTING CONVERTER INITIALIZATION")
    print("="*60)
    
    # Test without AI service
    print("\n1. Testing initialization without AI service...")
    converter = PlainTextConverter()
    print(f"   AI enabled: {converter.ai_enabled}")
    print(f"   Supported extensions: {converter.get_supported_extensions()}")
    
    # Test converter info
    info = converter.get_converter_info()
    print(f"   Converter info: {info}")
    
    return converter


def test_file_detection(converter, test_files):
    """Test file type detection."""
    print("\n" + "="*60)
    print("TESTING FILE TYPE DETECTION")
    print("="*60)
    
    for file_type, file_path in test_files.items():
        can_convert = converter.can_convert(file_path)
        print(f"   {file_type.upper()} file ({file_path.name}): {'✅ Can convert' if can_convert else '❌ Cannot convert'}")


def test_csv_conversion(converter, test_files):
    """Test CSV to markdown conversion."""
    print("\n" + "="*60)
    print("TESTING CSV CONVERSION")
    print("="*60)
    
    # Test CSV file
    if 'csv' in test_files:
        print("\n1. Converting CSV file...")
        csv_file = test_files['csv']
        output_file = csv_file.parent / f"{csv_file.stem}_output.md"
        
        success = converter.convert_file(csv_file, output_file)
        print(f"   Conversion successful: {'✅ Yes' if success else '❌ No'}")
        
        if success and output_file.exists():
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"   Output preview (first 300 chars):")
            print(f"   {content[:300]}...")
    
    # Test TSV file
    if 'tsv' in test_files:
        print("\n2. Converting TSV file...")
        tsv_file = test_files['tsv']
        output_file = tsv_file.parent / f"{tsv_file.stem}_output.md"
        
        success = converter.convert_file(tsv_file, output_file)
        print(f"   Conversion successful: {'✅ Yes' if success else '❌ No'}")
        
        if success and output_file.exists():
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"   Output preview (first 300 chars):")
            print(f"   {content[:300]}...")


def test_text_conversion(converter, test_files):
    """Test plain text to markdown conversion."""
    print("\n" + "="*60)
    print("TESTING PLAIN TEXT CONVERSION")
    print("="*60)
    
    # Test regular text file
    if 'txt' in test_files:
        print("\n1. Converting plain text file...")
        txt_file = test_files['txt']
        output_file = txt_file.parent / f"{txt_file.stem}_output.md"
        
        success = converter.convert_file(txt_file, output_file)
        print(f"   Conversion successful: {'✅ Yes' if success else '❌ No'}")
        
        if success and output_file.exists():
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"   Output preview (first 400 chars):")
            print(f"   {content[:400]}...")
    
    # Test log file
    if 'log' in test_files:
        print("\n2. Converting log file...")
        log_file = test_files['log']
        output_file = log_file.parent / f"{log_file.stem}_output.md"
        
        success = converter.convert_file(log_file, output_file)
        print(f"   Conversion successful: {'✅ Yes' if success else '❌ No'}")
        
        if success and output_file.exists():
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"   Output preview (first 300 chars):")
            print(f"   {content[:300]}...")


def test_edge_cases(converter, test_files):
    """Test edge cases and error handling."""
    print("\n" + "="*60)
    print("TESTING EDGE CASES")
    print("="*60)
    
    # Test empty file
    if 'empty' in test_files:
        print("\n1. Converting empty file...")
        empty_file = test_files['empty']
        output_file = empty_file.parent / f"{empty_file.stem}_output.md"
        
        success = converter.convert_file(empty_file, output_file)
        print(f"   Conversion successful: {'✅ Yes' if success else '❌ No'}")
        
        if success and output_file.exists():
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"   Output content: {content}")
    
    # Test non-existent file
    print("\n2. Testing non-existent file...")
    fake_file = Path("non_existent_file.txt")
    can_convert = converter.can_convert(fake_file)
    print(f"   Can convert non-existent file: {'❌ Yes (unexpected)' if can_convert else '✅ No (expected)'}")


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
    print("Plain Text Document Converter Test Suite")
    print("="*60)
    
    try:
        # Create test files
        test_files, temp_dir = create_test_files()
        
        # Initialize converter
        converter = test_converter_initialization()
        
        # Run tests
        test_file_detection(converter, test_files)
        test_csv_conversion(converter, test_files)
        test_text_conversion(converter, test_files)
        test_edge_cases(converter, test_files)
        
        # Show summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print("✅ All tests completed successfully!")
        print(f"   AI enabled: {converter.ai_enabled}")
        if converter.ai_enabled:
            print(f"   AI service: {converter.ai_service.get_service_name()}")
            print(f"   AI model: {converter.ai_service.get_model_name()}")
        else:
            print("   Using fallback text processing")
        
        print(f"\n📁 Test files and outputs are in: {temp_dir}")
        print("   You can examine the generated markdown files to verify the conversion quality.")
        
        # Cleanup
        cleanup_test_files(temp_dir)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
