#!/usr/bin/env python3
"""
Test script for improved image content filtering.

This script tests the enhanced filtering that removes unwanted analysis steps
and minimal content like logos from the image extraction output.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from services.base_converter import BaseDocumentConverter


def test_content_filtering():
    """Test the improved content filtering functionality."""
    
    print("🧪 Testing Improved Image Content Filtering")
    print("=" * 50)
    
    # Create a test converter instance
    class TestConverter(BaseDocumentConverter):
        def get_supported_extensions(self):
            return ['.test']
        
        def can_convert(self, file_path):
            return True
        
        def _convert_document_to_markdown(self, doc_path):
            return ""
    
    converter = TestConverter()
    
    # Test cases for content that should be filtered out
    test_cases = [
        {
            "content": """STEP 1: Determine the image type:
- This is a logo.

STEP 2: Extract content based on type:

- The image contains the text: **BDO**""",
            "description": "Analysis steps with logo",
            "should_filter": True
        },
        {
            "content": """STEP 1: Determine the image type:
- This is a regular image with a logo and people in a meeting setting.

STEP 2: Extract content based on type:

FOR REGULAR TEXT:
- Extracted Text: "BDO" """,
            "description": "Analysis steps with minimal text",
            "should_filter": True
        },
        {
            "content": "BDO",
            "description": "Simple logo text",
            "should_filter": True
        },
        {
            "content": "**IBM**",
            "description": "Bold logo text",
            "should_filter": True
        },
        {
            "content": """```
┌─────────────┐
│   Start     │
└──────┬──────┘
       ↓
┌─────────────┐
│  Process A  │
└──────┬──────┘
       ↓
┌─────────────┐
│     End     │
└─────────────┘
```""",
            "description": "Valid ASCII flowchart",
            "should_filter": False
        },
        {
            "content": """# Business Requirements

This document outlines the key requirements for the partner planning system.

## Overview

The system should support multiple planning cycles and review processes.""",
            "description": "Valid document content",
            "should_filter": False
        },
        {
            "content": "[unclear]",
            "description": "Unclear content marker",
            "should_filter": True
        },
        {
            "content": "",
            "description": "Empty content",
            "should_filter": True
        }
    ]
    
    print("Testing content filtering logic:")
    print("-" * 30)
    
    passed = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        content = test_case["content"]
        description = test_case["description"]
        expected_filter = test_case["should_filter"]
        
        # Test the filtering logic
        actual_filter = converter._is_failed_image_extraction(content, "test.jpg")
        
        status = "✅ PASS" if actual_filter == expected_filter else "❌ FAIL"
        if actual_filter == expected_filter:
            passed += 1
        
        print(f"{i:2d}. {description}")
        print(f"    Expected: {'Filter' if expected_filter else 'Keep'}")
        print(f"    Actual:   {'Filter' if actual_filter else 'Keep'}")
        print(f"    Result:   {status}")
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The improved filtering is working correctly.")
        print("\n✅ Benefits:")
        print("   - Analysis steps are filtered out")
        print("   - Simple logos are filtered out")
        print("   - Valid flowcharts are preserved")
        print("   - Meaningful content is preserved")
    else:
        print("⚠️  Some tests failed. The filtering logic may need adjustment.")
    
    return passed == total


if __name__ == "__main__":
    success = test_content_filtering()
    
    print("\n📚 Integration Impact:")
    print("   - Word documents: Cleaner image extraction output")
    print("   - PDF documents: Cleaner image extraction output") 
    print("   - Flowcharts: Still converted to ASCII as expected")
    print("   - Logos/minimal content: Now filtered out automatically")
