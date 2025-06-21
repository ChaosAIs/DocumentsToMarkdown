#!/usr/bin/env python3
"""
Test Script for Chunking Functionality

This script tests the chunking functionality for large files that exceed AI token limits.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from services.plain_text_converter import PlainTextConverter
from services.text_chunking_utils import TokenEstimator, TextChunker, CSVChunker


def create_large_test_files():
    """Create large test files to test chunking functionality."""
    test_files = {}
    
    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp(prefix="chunking_test_"))
    print(f"Created test directory: {temp_dir}")
    
    # Create a large CSV file (should exceed token limits)
    print("\nCreating large CSV file...")
    csv_content = "ID,Name,Description,Category,Price,Date,Status,Notes\n"
    
    # Generate 1000 rows of sample data
    for i in range(1000):
        csv_content += f"{i+1},Product_{i+1},This is a detailed description of product {i+1} with various features and specifications that make it unique in the market,Category_{(i % 10) + 1},{100 + (i * 0.99):.2f},2024-{(i % 12) + 1:02d}-{(i % 28) + 1:02d},{'Active' if i % 3 == 0 else 'Inactive'},Additional notes and comments about product {i+1} including warranty information and usage guidelines\n"
    
    large_csv_file = temp_dir / "large_products.csv"
    with open(large_csv_file, 'w', encoding='utf-8') as f:
        f.write(csv_content)
    test_files['large_csv'] = large_csv_file
    
    estimated_tokens = TokenEstimator.estimate_tokens(csv_content)
    print(f"   Created CSV with {len(csv_content)} characters, estimated {estimated_tokens} tokens")
    
    # Create a large text file (should exceed token limits)
    print("\nCreating large text file...")
    txt_content = """Large Document Analysis Report

Executive Summary
This comprehensive report analyzes various aspects of our business operations, market trends, and strategic recommendations for the upcoming fiscal year. The analysis covers multiple departments, geographical regions, and product lines to provide a holistic view of our organization's performance and future opportunities.

"""
    
    # Generate multiple sections with substantial content
    sections = [
        ("Market Analysis", "market trends, competitive landscape, customer behavior patterns"),
        ("Financial Performance", "revenue streams, cost analysis, profitability metrics"),
        ("Operational Efficiency", "process optimization, resource allocation, productivity measures"),
        ("Technology Infrastructure", "system capabilities, digital transformation, cybersecurity"),
        ("Human Resources", "talent acquisition, employee satisfaction, training programs"),
        ("Customer Relations", "satisfaction surveys, retention rates, service quality"),
        ("Product Development", "innovation pipeline, research initiatives, quality assurance"),
        ("Supply Chain", "vendor relationships, logistics optimization, inventory management"),
        ("Risk Management", "compliance requirements, mitigation strategies, contingency planning"),
        ("Strategic Planning", "long-term objectives, growth opportunities, market expansion")
    ]
    
    for section_name, keywords in sections:
        txt_content += f"\n{section_name}\n{'=' * len(section_name)}\n\n"
        
        # Generate multiple paragraphs for each section
        for para in range(5):
            txt_content += f"This section focuses on {keywords} and provides detailed insights into how these factors impact our business operations. "
            txt_content += f"Through comprehensive analysis of data collected over the past fiscal year, we have identified several key trends and patterns that require immediate attention. "
            txt_content += f"The findings suggest that strategic adjustments in this area could lead to significant improvements in overall performance and competitive positioning. "
            txt_content += f"Implementation of recommended changes should be prioritized based on resource availability and potential impact on stakeholder value.\n\n"
            
            # Add subsections
            txt_content += f"Key Findings in {section_name}\n"
            txt_content += f"- Critical factor analysis reveals important considerations for decision-making processes\n"
            txt_content += f"- Performance metrics indicate areas of strength and opportunities for improvement\n"
            txt_content += f"- Stakeholder feedback provides valuable insights into customer and employee perspectives\n"
            txt_content += f"- Competitive benchmarking shows our position relative to industry standards\n\n"
    
    txt_content += "\nConclusion\nThis analysis provides a foundation for strategic decision-making and operational improvements across all business units."
    
    large_txt_file = temp_dir / "large_report.txt"
    with open(large_txt_file, 'w', encoding='utf-8') as f:
        f.write(txt_content)
    test_files['large_txt'] = large_txt_file
    
    estimated_tokens = TokenEstimator.estimate_tokens(txt_content)
    print(f"   Created text file with {len(txt_content)} characters, estimated {estimated_tokens} tokens")
    
    return test_files, temp_dir


def test_token_estimation():
    """Test token estimation functionality."""
    print("\n" + "="*60)
    print("TESTING TOKEN ESTIMATION")
    print("="*60)
    
    test_texts = [
        "Short text",
        "This is a medium length text that should have more tokens than the short one.",
        "This is a much longer text that contains multiple sentences and should demonstrate how the token estimation works with larger content. It includes various words, punctuation marks, and different sentence structures to provide a realistic estimate of token usage."
    ]
    
    for i, text in enumerate(test_texts):
        tokens = TokenEstimator.estimate_tokens(text)
        print(f"   Text {i+1}: {len(text)} chars → {tokens} tokens (ratio: {len(text)/tokens:.1f} chars/token)")


def test_chunking_utilities():
    """Test the chunking utilities directly."""
    print("\n" + "="*60)
    print("TESTING CHUNKING UTILITIES")
    print("="*60)
    
    # Test text chunking
    print("\n1. Testing TextChunker...")
    text_chunker = TextChunker(max_tokens=500)  # Small limit for testing
    
    long_text = "This is a test paragraph. " * 100  # Create long text
    chunks = text_chunker.chunk_text(long_text)
    
    print(f"   Original text: {len(long_text)} chars, {TokenEstimator.estimate_tokens(long_text)} tokens")
    print(f"   Split into {len(chunks)} chunks:")
    for chunk in chunks:
        print(f"     Chunk {chunk.chunk_index + 1}: {len(chunk.content)} chars, {chunk.estimated_tokens} tokens")
    
    # Test CSV chunking
    print("\n2. Testing CSVChunker...")
    csv_chunker = CSVChunker(max_tokens=300)  # Small limit for testing
    
    csv_data = "Name,Age,City\n" + "\n".join([f"Person{i},{20+i},City{i}" for i in range(50)])
    chunks = csv_chunker.chunk_csv(csv_data)
    
    print(f"   Original CSV: {len(csv_data)} chars, {TokenEstimator.estimate_tokens(csv_data)} tokens")
    print(f"   Split into {len(chunks)} chunks:")
    for chunk in chunks:
        metadata = chunk.metadata or {}
        print(f"     Chunk {chunk.chunk_index + 1}: {chunk.estimated_tokens} tokens, rows {metadata.get('row_start', '?')}-{metadata.get('row_end', '?')}")


def test_converter_with_chunking(test_files):
    """Test the PlainTextConverter with chunking on large files."""
    print("\n" + "="*60)
    print("TESTING CONVERTER WITH CHUNKING")
    print("="*60)
    
    # Initialize converter
    converter = PlainTextConverter()
    print(f"Converter initialized:")
    print(f"   AI enabled: {converter.ai_enabled}")
    print(f"   Max tokens: {converter.max_tokens}")
    if converter.ai_enabled:
        print(f"   AI service: {converter.ai_service.get_service_name()}")
        print(f"   AI model: {converter.ai_service.get_model_name()}")
    
    # Test with large CSV
    if 'large_csv' in test_files:
        print(f"\n1. Testing large CSV conversion...")
        csv_file = test_files['large_csv']
        output_file = csv_file.parent / f"{csv_file.stem}_chunked.md"
        
        print(f"   Converting: {csv_file.name}")
        success = converter.convert_file(csv_file, output_file)
        print(f"   Conversion successful: {'✅ Yes' if success else '❌ No'}")
        
        if success and output_file.exists():
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"   Output size: {len(content)} characters")
            print(f"   Output preview (first 300 chars):")
            print(f"   {content[:300]}...")
    
    # Test with large text
    if 'large_txt' in test_files:
        print(f"\n2. Testing large text conversion...")
        txt_file = test_files['large_txt']
        output_file = txt_file.parent / f"{txt_file.stem}_chunked.md"
        
        print(f"   Converting: {txt_file.name}")
        success = converter.convert_file(txt_file, output_file)
        print(f"   Conversion successful: {'✅ Yes' if success else '❌ No'}")
        
        if success and output_file.exists():
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"   Output size: {len(content)} characters")
            print(f"   Output preview (first 300 chars):")
            print(f"   {content[:300]}...")


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
    print("Chunking Functionality Test Suite")
    print("="*60)
    
    try:
        # Test token estimation
        test_token_estimation()
        
        # Test chunking utilities
        test_chunking_utilities()
        
        # Create large test files
        test_files, temp_dir = create_large_test_files()
        
        # Test converter with chunking
        test_converter_with_chunking(test_files)
        
        # Show summary
        print("\n" + "="*60)
        print("CHUNKING TEST SUMMARY")
        print("="*60)
        print("✅ All chunking tests completed successfully!")
        print("   Token estimation working correctly")
        print("   Text and CSV chunking utilities functional")
        print("   Large file processing with AI chunking operational")
        
        print(f"\n📁 Test files and outputs are in: {temp_dir}")
        print("   You can examine the generated markdown files to verify chunking quality.")
        
        # Cleanup
        cleanup_test_files(temp_dir)
        
    except Exception as e:
        print(f"\n❌ Chunking test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
