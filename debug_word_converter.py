#!/usr/bin/env python3
"""
Debug script for Word converter image positioning
"""

import logging
from pathlib import Path
from services.word_converter import WordDocumentConverter

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Create converter
    converter = WordDocumentConverter()
    
    # Convert the specific document
    input_file = Path("input/Partner Plans - Business Requirements Document (BRD) v0.1.docx")
    output_file = Path("output/debug_output.md")
    
    if not input_file.exists():
        print(f"Input file not found: {input_file}")
        return
    
    print(f"Converting: {input_file}")
    
    try:
        # Convert document
        success = converter.convert_file(input_file, output_file)

        if success:
            print(f"Conversion complete. Output saved to: {output_file}")
        else:
            print("Conversion failed")

    except Exception as e:
        print(f"Error during conversion: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
