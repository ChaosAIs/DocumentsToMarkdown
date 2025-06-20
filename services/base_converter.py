#!/usr/bin/env python3
"""
Base Document Converter Interface

This module defines the abstract base class for all document converters.
All specific converters (Word, PDF, etc.) should inherit from this base class.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Dict, Any
import logging


class BaseDocumentConverter(ABC):
    """Abstract base class for document converters."""

    def __init__(self):
        """Initialize the base converter."""
        self.section_counters = [0] * 6  # Support up to 6 heading levels

        # Setup logging
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def get_supported_extensions(self) -> List[str]:
        """
        Get list of file extensions supported by this converter.
        
        Returns:
            List of supported file extensions (e.g., ['.docx', '.doc'])
        """
        pass
    
    @abstractmethod
    def can_convert(self, file_path: Path) -> bool:
        """
        Check if this converter can handle the given file.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            True if this converter can handle the file, False otherwise
        """
        pass
    
    @abstractmethod
    def _convert_document_to_markdown(self, doc_path: Path) -> str:
        """
        Convert a document to Markdown format.
        
        Args:
            doc_path: Path to the document to convert
            
        Returns:
            Markdown content as string
        """
        pass
    
    def _reset_section_counters(self) -> None:
        """Reset section counters for a new document."""
        self.section_counters = [0] * 6
    
    def _update_section_counter(self, level: int) -> str:
        """
        Update section counter for the given level and return section number.

        Args:
            level: Heading level (1-6)

        Returns:
            Section number string (e.g., "1.2.3 ")
        """
        # Increment counter for current level
        self.section_counters[level - 1] += 1

        # Reset counters for deeper levels
        for i in range(level, 6):
            self.section_counters[i] = 0

        # Build section number string
        section_parts = []
        for i in range(level):
            if self.section_counters[i] > 0:
                section_parts.append(str(self.section_counters[i]))

        return ".".join(section_parts) + " " if section_parts else ""
    
    def convert_file(self, input_file: Path, output_file: Path) -> bool:
        """
        Convert a single document to Markdown.
        
        Args:
            input_file: Path to the input document
            output_file: Path where the Markdown file should be saved
            
        Returns:
            True if conversion successful, False otherwise
        """
        try:
            self.logger.info(f"Converting: {input_file.name}")
            
            # Check if we can convert this file
            if not self.can_convert(input_file):
                self.logger.error(f"Cannot convert file type: {input_file.suffix}")
                return False
            
            # Convert document content
            markdown_content = self._convert_document_to_markdown(input_file)
            
            # Write Markdown file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            self.logger.info(f"Successfully converted: {input_file.name} -> {output_file.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to convert {input_file.name}: {str(e)}")
            return False
    
    def get_converter_info(self) -> Dict[str, Any]:
        """
        Get information about this converter.

        Returns:
            Dictionary with converter information
        """
        return {
            "name": self.__class__.__name__,
            "supported_extensions": self.get_supported_extensions(),
            "supports_section_numbering": True,
            "section_numbering_enabled": True
        }
