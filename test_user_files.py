#!/usr/bin/env python3
"""
Test script for user's files in input directory
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from services.document_converter_manager import DocumentConverterManager


def test_user_files():
    """Test conversion of user's files."""
    print("Testing Plain Text Converter with your files:")
    print("=" * 60)
    
    # Initialize manager
    manager = DocumentConverterManager()
    
    # Check which files can be converted by PlainTextConverter
    input_dir = Path('input')
    txt_file = input_dir / 'Gen API Solution.txt'
    csv_file = input_dir / 'product_purchase_orders.csv'
    
    # Test individual files
    for file_path in [txt_file, csv_file]:
        if file_path.exists():
            converter = manager.find_converter_for_file(file_path)
            print(f'File: {file_path.name}')
            print(f'Converter: {converter.__class__.__name__ if converter else "None"}')
            
            if converter and converter.__class__.__name__ == 'PlainTextConverter':
                print(f'✅ Will be processed by PlainTextConverter')
                # Show a preview of the content
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    print(f'Content preview (first 200 chars): {content[:200]}...')
                except Exception as e:
                    print(f'Error reading file: {e}')
            else:
                print(f'❌ Will be processed by different converter: {converter.__class__.__name__ if converter else "None"}')
            print()
    
    # Convert the files
    print('Converting files...')
    print('=' * 60)
    results = manager.convert_all()
    print(f'Total files found: {results["total_files"]}')
    print(f'Successful conversions: {results["successful_conversions"]}')
    print(f'Failed conversions: {results["failed_conversions"]}')
    
    # Show the generated markdown files for our target files
    output_dir = Path('output')
    if output_dir.exists():
        print('\nGenerated markdown files for your text files:')
        print('=' * 60)
        
        target_files = ['Gen API Solution.md', 'product_purchase_orders.md']
        for md_file_name in target_files:
            md_file = output_dir / md_file_name
            if md_file.exists():
                print(f'\n📄 {md_file_name}')
                print('-' * 40)
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # Show first 500 characters
                    preview = content[:500]
                    if len(content) > 500:
                        preview += "..."
                    print(preview)
                except Exception as e:
                    print(f'Error reading output file: {e}')
            else:
                print(f'❌ {md_file_name} was not generated')


if __name__ == "__main__":
    test_user_files()
