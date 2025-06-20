#!/usr/bin/env python3
"""
PDF Document to Markdown Converter Service

This service handles conversion of PDF documents to Markdown format.
Uses PyMuPDF (fitz) for PDF text extraction and processing.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
import re

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF is not installed. Please install it using:")
    print("pip install PyMuPDF")
    sys.exit(1)

from .base_converter import BaseDocumentConverter


class PDFDocumentConverter(BaseDocumentConverter):
    """Converts PDF documents to Markdown format with full content preservation."""

    def __init__(self):
        """Initialize PDF converter."""
        super().__init__()
        self.font_size_threshold = 12  # Minimum font size to consider for headings
        self.heading_font_sizes = {}  # Track font sizes to determine heading levels
    
    def get_supported_extensions(self) -> List[str]:
        """Get list of supported PDF document extensions."""
        return ['.pdf']
    
    def can_convert(self, file_path: Path) -> bool:
        """Check if this converter can handle PDF documents."""
        return file_path.suffix.lower() in self.get_supported_extensions()
    
    def _analyze_font_sizes(self, doc: fitz.Document) -> Dict[float, int]:
        """
        Analyze font sizes in the document to determine heading levels.
        
        Args:
            doc: PyMuPDF document object
            
        Returns:
            Dictionary mapping font sizes to heading levels
        """
        font_sizes = set()
        
        # Collect all font sizes from the document
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("dict")["blocks"]
            
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            font_size = span["size"]
                            if font_size > self.font_size_threshold:
                                font_sizes.add(font_size)
        
        # Sort font sizes in descending order and assign heading levels
        sorted_sizes = sorted(font_sizes, reverse=True)
        font_to_level = {}
        
        for i, size in enumerate(sorted_sizes[:6]):  # Max 6 heading levels
            font_to_level[size] = i + 1
        
        self.logger.info(f"Detected font sizes for headings: {font_to_level}")
        return font_to_level
    
    def _is_heading_text(self, text: str) -> bool:
        """
        Check if text content suggests it's a heading (conservative approach).

        Args:
            text: Text content to analyze

        Returns:
            True if text appears to be a heading
        """
        text = text.strip()

        # Only detect clear heading patterns to preserve original content
        # Check for explicit section numbering patterns
        section_patterns = [
            r'^\d+\.?\s+[A-Z]',  # "1. Introduction" or "1 Introduction"
            r'^\d+\.\d+\.?\s+[A-Z]',  # "1.1. Overview" or "1.1 Overview"
            r'^[A-Z][A-Z\s&/]{3,}$',  # All caps text like "INTRODUCTION", "BUSINESS REQUIREMENTS"
        ]

        for pattern in section_patterns:
            if re.match(pattern, text):
                return True

        # Check for title case patterns that are clearly headings
        title_patterns = [
            r'^[A-Z][a-z]+(\s+[A-Z][a-z]*)*:?$',  # Title case like "Business Requirements"
            r'^Abstract$',  # Common academic paper sections
            r'^Conclusion$',
            r'^References$',
            r'^Acknowledgments?$',
        ]

        for pattern in title_patterns:
            if re.match(pattern, text):
                return True

        return False
    
    def _extract_text_with_formatting(self, doc: fitz.Document) -> List[Dict[str, Any]]:
        """
        Extract text with formatting information from PDF.
        
        Args:
            doc: PyMuPDF document object
            
        Returns:
            List of text blocks with formatting information
        """
        text_blocks = []
        font_to_level = self._analyze_font_sizes(doc)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("dict")["blocks"]
            
            for block in blocks:
                if "lines" in block:  # Text block
                    block_text = ""
                    block_font_size = 0
                    is_bold = False
                    
                    for line in block["lines"]:
                        line_text = ""
                        for span in line["spans"]:
                            span_text = span["text"]
                            font_size = span["size"]
                            font_flags = span["flags"]
                            
                            # Check if text is bold (font flags & 16)
                            if font_flags & 16:
                                is_bold = True
                            
                            # Track the largest font size in the block
                            if font_size > block_font_size:
                                block_font_size = font_size
                            
                            line_text += span_text
                        
                        block_text += line_text + "\n"
                    
                    block_text = block_text.strip()
                    if block_text:
                        # Determine if this is a heading
                        is_heading = (
                            block_font_size in font_to_level or
                            (is_bold and self._is_heading_text(block_text)) or
                            self._is_heading_text(block_text)
                        )
                        
                        heading_level = font_to_level.get(block_font_size, 2) if is_heading else 0
                        
                        text_blocks.append({
                            'text': block_text,
                            'font_size': block_font_size,
                            'is_bold': is_bold,
                            'is_heading': is_heading,
                            'heading_level': heading_level,
                            'page': page_num + 1
                        })
        
        return text_blocks
    
    def _convert_text_blocks_to_markdown(self, text_blocks: List[Dict[str, Any]]) -> str:
        """
        Convert extracted text blocks to Markdown format.
        
        Args:
            text_blocks: List of text blocks with formatting information
            
        Returns:
            Markdown content as string
        """
        markdown_content = ""
        
        for block in text_blocks:
            text = block['text']
            
            if block['is_heading']:
                # Convert to markdown heading
                heading_level = block['heading_level']
                heading_prefix = "#" * heading_level
                section_number = self._update_section_counter(heading_level)
                markdown_content += f"{heading_prefix} {section_number}{text}\n\n"
            else:
                # Regular paragraph
                # Handle potential table-like content
                if self._looks_like_table(text):
                    markdown_content += self._convert_table_like_text(text)
                else:
                    # Apply bold formatting if the entire block was bold
                    if block['is_bold'] and not block['is_heading']:
                        # Clean up the text and ensure proper bold formatting
                        text = text.strip()
                        if text:
                            text = f"**{text}**"

                    markdown_content += f"{text}\n\n"
        
        return markdown_content
    
    def _looks_like_table(self, text: str) -> bool:
        """
        Check if text looks like tabular data.
        
        Args:
            text: Text to analyze
            
        Returns:
            True if text appears to be tabular
        """
        lines = text.split('\n')
        if len(lines) < 2:
            return False
        
        # Check for consistent column separators
        separators = ['\t', '  ', ' | ', '|']
        for sep in separators:
            if all(sep in line for line in lines if line.strip()):
                return True
        
        return False
    
    def _convert_table_like_text(self, text: str) -> str:
        """
        Convert table-like text to Markdown table format.
        
        Args:
            text: Table-like text
            
        Returns:
            Markdown table format
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if not lines:
            return text + "\n\n"
        
        # Try to detect separator
        separator = None
        for sep in ['\t', ' | ', '|', '  ']:
            if sep in lines[0]:
                separator = sep
                break
        
        if not separator:
            return text + "\n\n"
        
        # Convert to markdown table
        markdown_table = ""
        for i, line in enumerate(lines):
            cells = [cell.strip() for cell in line.split(separator)]
            markdown_table += "| " + " | ".join(cells) + " |\n"
            
            # Add separator row after header
            if i == 0:
                markdown_table += "| " + " | ".join(["---"] * len(cells)) + " |\n"
        
        return markdown_table + "\n"
    
    def _convert_document_to_markdown(self, doc_path: Path) -> str:
        """Convert a PDF document to Markdown format."""
        try:
            # Reset section counters for new document
            self._reset_section_counters()
            
            self.logger.info(f"Opening PDF document: {doc_path}")
            doc = fitz.open(doc_path)
            
            # Extract text with formatting
            text_blocks = self._extract_text_with_formatting(doc)
            
            # Convert to markdown
            markdown_content = self._convert_text_blocks_to_markdown(text_blocks)
            
            doc.close()
            
            return markdown_content
            
        except Exception as e:
            self.logger.error(f"Error converting PDF document {doc_path}: {str(e)}")
            return f"# Error Converting Document\n\nFailed to convert {doc_path.name}: {str(e)}\n"
