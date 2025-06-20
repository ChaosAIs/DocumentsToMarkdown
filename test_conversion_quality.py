#!/usr/bin/env python3
"""
Comprehensive Test Suite for Document Conversion Quality

This script validates the quality and correctness of document conversions
by checking various aspects of the converted Markdown files.
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Add the services directory to the path
sys.path.append(str(Path(__file__).parent / "services"))

try:
    from services.document_converter_manager import DocumentConverterManager
    print("Successfully imported DocumentConverterManager")
except ImportError as e:
    print(f"Error importing DocumentConverterManager: {e}")
    sys.exit(1)


class ConversionQualityTester:
    """Tests the quality of document conversions."""
    
    def __init__(self):
        self.manager = DocumentConverterManager()
        self.test_results = []
    
    def test_heading_structure(self, markdown_content: str, filename: str) -> Dict[str, Any]:
        """Test if heading structure is properly preserved."""
        lines = markdown_content.split('\n')
        headings = []
        
        for i, line in enumerate(lines):
            if line.strip().startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                heading_text = line.strip('#').strip()
                headings.append({
                    'level': level,
                    'text': heading_text,
                    'line_number': i + 1
                })
        
        # Check for proper heading hierarchy
        hierarchy_issues = []
        prev_level = 0
        
        for heading in headings:
            if heading['level'] > prev_level + 1:
                hierarchy_issues.append(f"Heading level jump from {prev_level} to {heading['level']} at line {heading['line_number']}")
            prev_level = heading['level']
        
        return {
            'test_name': 'Heading Structure',
            'filename': filename,
            'total_headings': len(headings),
            'headings': headings,
            'hierarchy_issues': hierarchy_issues,
            'passed': len(hierarchy_issues) == 0
        }
    
    def test_section_numbering(self, markdown_content: str, filename: str) -> Dict[str, Any]:
        """Test if section numbering is properly applied."""
        lines = markdown_content.split('\n')
        numbered_headings = []
        
        for i, line in enumerate(lines):
            if line.strip().startswith('#'):
                heading_text = line.strip('#').strip()
                # Check if heading starts with a number pattern
                number_match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+)$', heading_text)
                if number_match:
                    numbered_headings.append({
                        'line_number': i + 1,
                        'section_number': number_match.group(1),
                        'title': number_match.group(2),
                        'full_text': heading_text
                    })
        
        return {
            'test_name': 'Section Numbering',
            'filename': filename,
            'numbered_headings': len(numbered_headings),
            'numbering_examples': numbered_headings[:5],  # Show first 5 examples
            'passed': len(numbered_headings) > 0
        }
    
    def test_table_formatting(self, markdown_content: str, filename: str) -> Dict[str, Any]:
        """Test if tables are properly formatted."""
        lines = markdown_content.split('\n')
        tables = []
        in_table = False
        current_table = []
        
        for i, line in enumerate(lines):
            if '|' in line and line.strip():
                if not in_table:
                    in_table = True
                    current_table = [{'line_number': i + 1, 'content': line.strip()}]
                else:
                    current_table.append({'line_number': i + 1, 'content': line.strip()})
            else:
                if in_table:
                    tables.append(current_table)
                    current_table = []
                    in_table = False
        
        # Add the last table if we were still in one
        if in_table and current_table:
            tables.append(current_table)
        
        # Validate table structure
        valid_tables = 0
        table_issues = []
        
        for table in tables:
            if len(table) >= 2:  # At least header and separator
                header = table[0]['content']
                separator = table[1]['content'] if len(table) > 1 else ""
                
                # Check if separator line contains dashes
                if '---' in separator:
                    valid_tables += 1
                else:
                    table_issues.append(f"Invalid table separator at line {table[1]['line_number']}")
            else:
                table_issues.append(f"Incomplete table starting at line {table[0]['line_number']}")
        
        return {
            'test_name': 'Table Formatting',
            'filename': filename,
            'total_tables': len(tables),
            'valid_tables': valid_tables,
            'table_issues': table_issues,
            'passed': len(table_issues) == 0 and len(tables) > 0
        }
    
    def test_text_formatting(self, markdown_content: str, filename: str) -> Dict[str, Any]:
        """Test if text formatting (bold, italic) is preserved."""
        bold_count = len(re.findall(r'\*\*[^*]+\*\*', markdown_content))
        italic_count = len(re.findall(r'\*[^*]+\*', markdown_content))
        
        # Check for proper formatting patterns
        formatting_issues = []
        
        # Check for unmatched asterisks
        unmatched_bold = re.findall(r'\*\*[^*]*$', markdown_content, re.MULTILINE)
        unmatched_italic = re.findall(r'(?<!\*)\*(?!\*)[^*]*$', markdown_content, re.MULTILINE)
        
        if unmatched_bold:
            formatting_issues.append(f"Found {len(unmatched_bold)} unmatched bold markers")
        if unmatched_italic:
            formatting_issues.append(f"Found {len(unmatched_italic)} unmatched italic markers")
        
        return {
            'test_name': 'Text Formatting',
            'filename': filename,
            'bold_count': bold_count,
            'italic_count': italic_count,
            'formatting_issues': formatting_issues,
            'passed': len(formatting_issues) == 0
        }
    
    def test_content_preservation(self, markdown_content: str, filename: str) -> Dict[str, Any]:
        """Test if content is properly preserved (no empty sections, reasonable length)."""
        lines = markdown_content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        # Check for empty sections (heading followed immediately by another heading)
        empty_sections = []
        for i in range(len(lines) - 1):
            if lines[i].strip().startswith('#') and lines[i + 1].strip().startswith('#'):
                empty_sections.append(f"Empty section at line {i + 1}: {lines[i].strip()}")
        
        # Basic content metrics
        word_count = len(markdown_content.split())
        char_count = len(markdown_content)
        
        return {
            'test_name': 'Content Preservation',
            'filename': filename,
            'total_lines': len(lines),
            'non_empty_lines': len(non_empty_lines),
            'word_count': word_count,
            'char_count': char_count,
            'empty_sections': empty_sections,
            'passed': len(empty_sections) == 0 and word_count > 10
        }
    
    def run_quality_tests(self, file_path: Path) -> List[Dict[str, Any]]:
        """Run all quality tests on a converted Markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tests = [
                self.test_heading_structure(content, file_path.name),
                self.test_section_numbering(content, file_path.name),
                self.test_table_formatting(content, file_path.name),
                self.test_text_formatting(content, file_path.name),
                self.test_content_preservation(content, file_path.name)
            ]
            
            return tests
            
        except Exception as e:
            return [{
                'test_name': 'File Reading Error',
                'filename': file_path.name,
                'error': str(e),
                'passed': False
            }]
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive quality tests on all converted files."""
        print("Running Comprehensive Conversion Quality Tests")
        print("=" * 60)
        
        # First, convert all files
        print("\n1. Converting all documents...")
        conversion_results = self.manager.convert_all()
        
        if conversion_results['successful_conversions'] == 0:
            return {
                'conversion_results': conversion_results,
                'quality_tests': [],
                'overall_passed': False,
                'message': 'No successful conversions to test'
            }
        
        # Then test the quality of converted files
        print(f"\n2. Testing quality of {conversion_results['successful_conversions']} converted files...")
        
        output_folder = Path("output")
        all_test_results = []
        
        for md_file in output_folder.glob("*.md"):
            print(f"\n   Testing: {md_file.name}")
            file_tests = self.run_quality_tests(md_file)
            all_test_results.extend(file_tests)
        
        # Summarize results
        total_tests = len(all_test_results)
        passed_tests = sum(1 for test in all_test_results if test.get('passed', False))
        
        return {
            'conversion_results': conversion_results,
            'quality_tests': all_test_results,
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'overall_passed': passed_tests == total_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0
        }


def main():
    """Main function to run comprehensive quality tests."""
    tester = ConversionQualityTester()
    results = tester.run_comprehensive_test()
    
    print(f"\n{'='*60}")
    print("COMPREHENSIVE TEST RESULTS")
    print(f"{'='*60}")
    
    # Conversion summary
    conv_results = results['conversion_results']
    print(f"\nConversion Summary:")
    print(f"  Total files: {conv_results['total_files']}")
    print(f"  Successful: {conv_results['successful_conversions']}")
    print(f"  Failed: {conv_results['failed_conversions']}")
    
    # Quality test summary
    print(f"\nQuality Test Summary:")
    print(f"  Total tests: {results['total_tests']}")
    print(f"  Passed tests: {results['passed_tests']}")
    print(f"  Success rate: {results['success_rate']:.1f}%")
    
    # Detailed results
    print(f"\nDetailed Test Results:")
    for test in results['quality_tests']:
        status = "✅ PASS" if test.get('passed', False) else "❌ FAIL"
        print(f"  {status} {test['test_name']} - {test['filename']}")
        
        # Show specific details for failed tests
        if not test.get('passed', False):
            if 'error' in test:
                print(f"    Error: {test['error']}")
            if 'hierarchy_issues' in test and test['hierarchy_issues']:
                print(f"    Issues: {test['hierarchy_issues']}")
            if 'table_issues' in test and test['table_issues']:
                print(f"    Issues: {test['table_issues']}")
            if 'formatting_issues' in test and test['formatting_issues']:
                print(f"    Issues: {test['formatting_issues']}")
            if 'empty_sections' in test and test['empty_sections']:
                print(f"    Issues: {test['empty_sections']}")
    
    # Overall result
    overall_status = "✅ ALL TESTS PASSED" if results['overall_passed'] else "❌ SOME TESTS FAILED"
    print(f"\n{overall_status}")
    
    return results['overall_passed']


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
