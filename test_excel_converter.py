#!/usr/bin/env python3
"""
Test script for Excel converter functionality.

This script creates sample Excel files and tests the Excel converter.
"""

import sys
from pathlib import Path
import logging

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

def create_sample_excel_file():
    """Create a sample Excel file for testing."""
    try:
        import openpyxl
        from openpyxl import Workbook
        
        # Create a new workbook
        wb = Workbook()
        
        # Get the active worksheet
        ws1 = wb.active
        ws1.title = "Sample Data"
        
        # Add sample data to first worksheet
        ws1['A1'] = "Name"
        ws1['B1'] = "Age"
        ws1['C1'] = "City"
        ws1['D1'] = "Salary"
        
        ws1['A2'] = "John Doe"
        ws1['B2'] = 30
        ws1['C2'] = "New York"
        ws1['D2'] = 75000
        
        ws1['A3'] = "Jane Smith"
        ws1['B3'] = 25
        ws1['C3'] = "Los Angeles"
        ws1['D3'] = 68000
        
        ws1['A4'] = "Bob Johnson"
        ws1['B4'] = 35
        ws1['C4'] = "Chicago"
        ws1['D4'] = 82000
        
        # Create a second worksheet
        ws2 = wb.create_sheet("Financial Summary")
        ws2['A1'] = "Quarter"
        ws2['B1'] = "Revenue"
        ws2['C1'] = "Expenses"
        ws2['D1'] = "Profit"
        
        ws2['A2'] = "Q1 2024"
        ws2['B2'] = 150000
        ws2['C2'] = 120000
        ws2['D2'] = 30000
        
        ws2['A3'] = "Q2 2024"
        ws2['B3'] = 175000
        ws2['C3'] = 135000
        ws2['D3'] = 40000
        
        # Create input directory if it doesn't exist
        input_dir = Path("input")
        input_dir.mkdir(exist_ok=True)
        
        # Save the workbook
        test_file = input_dir / "test_sample.xlsx"
        wb.save(test_file)
        print(f"✓ Created sample Excel file: {test_file}")
        return test_file
        
    except ImportError:
        print("Error: openpyxl is not installed. Please install it using:")
        print("pip install openpyxl")
        return None
    except Exception as e:
        print(f"Error creating sample Excel file: {e}")
        return None

def test_excel_converter():
    """Test the Excel converter functionality."""
    try:
        # Import the converter
        from services.excel_converter import ExcelDocumentConverter
        
        # Create converter instance
        converter = ExcelDocumentConverter()
        
        # Test supported extensions
        extensions = converter.get_supported_extensions()
        print(f"✓ Supported extensions: {extensions}")
        
        # Create sample file
        sample_file = create_sample_excel_file()
        if not sample_file:
            return False
        
        # Test if converter can handle the file
        can_convert = converter.can_convert(sample_file)
        print(f"✓ Can convert {sample_file.name}: {can_convert}")
        
        if not can_convert:
            print("✗ Converter cannot handle the test file")
            return False
        
        # Create output directory
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Test conversion
        output_file = output_dir / "test_sample.md"
        success = converter.convert_file(sample_file, output_file)
        
        if success:
            print(f"✓ Successfully converted {sample_file.name} to {output_file.name}")
            
            # Display the converted content
            if output_file.exists():
                print("\n" + "="*50)
                print("CONVERTED MARKDOWN CONTENT:")
                print("="*50)
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(content)
                print("="*50)
            
            return True
        else:
            print(f"✗ Failed to convert {sample_file.name}")
            return False
            
    except ImportError as e:
        print(f"Error: Required module not available: {e}")
        print("Please install required dependencies:")
        print("pip install openpyxl xlrd")
        return False
    except Exception as e:
        print(f"Error testing Excel converter: {e}")
        return False

def test_document_converter_manager():
    """Test the Excel converter integration with DocumentConverterManager."""
    try:
        from services.document_converter_manager import DocumentConverterManager
        
        # Create manager instance
        manager = DocumentConverterManager()
        
        # Check if Excel extensions are supported
        supported_extensions = manager.get_supported_extensions()
        excel_extensions = ['.xlsx', '.xlsm', '.xlsb', '.xls']
        
        print(f"✓ All supported extensions: {supported_extensions}")
        
        excel_supported = all(ext in supported_extensions for ext in excel_extensions[:3])  # Skip .xls if xlrd not available
        print(f"✓ Excel extensions supported: {excel_supported}")
        
        # Test finding converter for Excel file
        sample_file = Path("input/test_sample.xlsx")
        if sample_file.exists():
            converter = manager.find_converter_for_file(sample_file)
            if converter:
                print(f"✓ Found converter for Excel file: {converter.__class__.__name__}")
                return True
            else:
                print("✗ No converter found for Excel file")
                return False
        else:
            print("ℹ Sample Excel file not found, skipping converter lookup test")
            return excel_supported
            
    except Exception as e:
        print(f"Error testing DocumentConverterManager: {e}")
        return False

def main():
    """Main test function."""
    print("=" * 60)
    print("Excel Converter Test Suite")
    print("=" * 60)
    
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    tests_passed = 0
    total_tests = 3
    
    print("\n1. Testing Excel Converter...")
    if test_excel_converter():
        tests_passed += 1
        print("✓ Excel Converter test PASSED")
    else:
        print("✗ Excel Converter test FAILED")
    
    print("\n2. Testing DocumentConverterManager integration...")
    if test_document_converter_manager():
        tests_passed += 1
        print("✓ DocumentConverterManager integration test PASSED")
    else:
        print("✗ DocumentConverterManager integration test FAILED")
    
    print("\n3. Testing converter info...")
    try:
        from services.excel_converter import ExcelDocumentConverter
        converter = ExcelDocumentConverter()
        info = converter.get_converter_info()
        print(f"✓ Converter info: {info}")
        tests_passed += 1
        print("✓ Converter info test PASSED")
    except Exception as e:
        print(f"✗ Converter info test FAILED: {e}")
    
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {tests_passed}/{total_tests} tests passed")
    print("=" * 60)
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Excel converter is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
