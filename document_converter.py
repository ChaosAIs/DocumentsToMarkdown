#!/usr/bin/env python3
"""
Document to Markdown Converter (Unified Version)

A comprehensive Python application that converts various document types to Markdown format.

Supported formats:
- Word documents (.docx, .doc)
- PDF documents (.pdf)

Features:
- Automatic section numbering
- Modular architecture with pluggable converters
- Preserves document structure and formatting
- Batch processing of multiple documents
- Detailed logging and error handling
- Command-line interface with options
- Backward compatibility with legacy usage

Usage:
    python document_converter.py                    # Convert all files in input/ folder
    python document_converter.py --no-numbering     # Convert without section numbering
    python document_converter.py --input docs --output markdown  # Custom folders
    python document_converter.py --stats            # Show converter statistics only

"""

import sys
import argparse
from pathlib import Path
import logging

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import the modular system
try:
    from services.document_converter_manager import DocumentConverterManager
except ImportError as e:
    print(f"Error: Modular converter system not available: {e}")
    print("Please ensure the 'services' directory and converter modules are present.")
    sys.exit(1)






def print_banner():
    """Print application banner."""
    print("=" * 60)
    print("Document to Markdown Converter (Unified)")
    print("=" * 60)
    print("Supported formats: Word (.docx, .doc), PDF (.pdf)")
    print("Features: Section numbering, batch processing, modular architecture")
    print("=" * 60)


def print_statistics(manager):
    """Print converter statistics."""
    stats = manager.get_conversion_statistics()

    print(f"\nAvailable Converters: {stats['total_converters']}")
    print(f"Supported Extensions: {', '.join(stats['supported_extensions'])}")

    print("\nConverter Details:")
    for converter_info in stats['converters']:
        name = converter_info['name']
        extensions = ', '.join(converter_info['supported_extensions'])
        numbering = "✓" if converter_info['section_numbering_enabled'] else "✗"
        print(f"  • {name}: {extensions} (Section numbering: {numbering})")


def print_conversion_results(results):
    """Print conversion results summary."""
    print(f"\nConversion Results:")
    print(f"  Total files: {results['total_files']}")
    print(f"  Successful: {results['successful_conversions']}")
    print(f"  Failed: {results['failed_conversions']}")

    if results['results']:
        print(f"\nDetailed Results:")
        for result in results['results']:
            status_icon = "✓" if result['status'] == 'success' else "✗"
            print(f"  {status_icon} {result['file']} ({result['converter']})")


def main():
    """Main function to run the document converter."""
    parser = argparse.ArgumentParser(
        description="Convert documents to Markdown format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python document_converter.py                    # Convert all files in input/ folder
  python document_converter.py --no-numbering     # Convert without section numbering
  python document_converter.py --input docs --output markdown  # Custom folders
  python document_converter.py --stats            # Show converter statistics only
        """
    )

    parser.add_argument(
        '--input', '-i',
        default='input',
        help='Input folder containing documents to convert (default: input)'
    )

    parser.add_argument(
        '--output', '-o',
        default='output',
        help='Output folder for converted Markdown files (default: output)'
    )

    parser.add_argument(
        '--no-numbering',
        action='store_true',
        help='Disable automatic section numbering'
    )

    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show converter statistics and exit'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )



    args = parser.parse_args()

    # Print banner
    print_banner()

    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    print("\nUsing Modular Converter System")

    # Initialize modular converter manager
    try:
        manager = DocumentConverterManager(
            input_folder=args.input,
            output_folder=args.output,
            add_section_numbers=not args.no_numbering
        )
    except Exception as e:
        print(f"Error initializing converter: {e}")
        return 1

    # Show statistics if requested
    if args.stats:
        print_statistics(manager)
        return 0

    # Show converter information
    print_statistics(manager)

    # Check for files to convert
    convertible_files = manager.get_convertible_files()
    if not convertible_files:
        print(f"\nNo convertible files found in '{args.input}' folder.")
        print("Supported formats: Word (.docx, .doc), PDF (.pdf)")
        print("\nPlease add some documents to the input folder and try again.")
        return 0

    print(f"\nFound {len(convertible_files)} file(s) to convert:")
    for file_path in convertible_files:
        converter = manager.find_converter_for_file(file_path)
        converter_name = converter.__class__.__name__ if converter else "Unknown"
        print(f"  • {file_path.name} ({converter_name})")

    # Perform conversion
    print(f"\nStarting conversion...")
    try:
        results = manager.convert_all()
        print_conversion_results(results)

        if results['successful_conversions'] > 0:
            print(f"\n✓ Conversion completed successfully!")
            print(f"Check the '{args.output}' folder for converted Markdown files.")

        if results['failed_conversions'] > 0:
            print(f"\n⚠ Some conversions failed. Check the logs for details.")
            return 1

        return 0

    except Exception as e:
        print(f"\nError during conversion: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
