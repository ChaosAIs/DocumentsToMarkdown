#!/usr/bin/env python3
"""
Image Document to Markdown Converter Service

This service handles conversion of image files to Markdown format using AI vision capabilities.
Supports common image formats: jpg, jpeg, png, gif, bmp, tiff, webp
"""

import sys
import os
import base64
from pathlib import Path
from typing import List, Optional, Dict, Any
import io

try:
    from PIL import Image
    import requests
    from openai import OpenAI
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Error: Required packages not installed. Please install them using:")
    print("pip install -r requirements.txt")
    print(f"Missing: {e}")
    sys.exit(1)

from .base_converter import BaseDocumentConverter


class ImageDocumentConverter(BaseDocumentConverter):
    """Converts image files to Markdown format using AI vision capabilities."""

    def __init__(self):
        """Initialize the image converter with AI vision capabilities."""
        super().__init__()
        
        # Load environment variables
        load_dotenv()
        
        # Initialize OpenAI client
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            self.logger.warning("OPENAI_API_KEY not found in environment variables. Image conversion will not work.")
            self.client = None
        else:
            try:
                # Initialize OpenAI client with minimal parameters
                self.client = OpenAI(
                    api_key=self.openai_api_key
                )
                # Test the client with a simple call
                self.logger.info("OpenAI client initialized successfully")
            except Exception as e:
                self.logger.error(f"Error initializing OpenAI client: {e}")
                self.client = None
        
        # Configuration from environment variables
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o')
        self.max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '4096'))
        self.temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.1'))
        self.max_image_size_mb = int(os.getenv('IMAGE_MAX_SIZE_MB', '20'))
        self.image_quality = int(os.getenv('IMAGE_QUALITY_COMPRESSION', '85'))

    def get_supported_extensions(self) -> List[str]:
        """Get list of supported image file extensions."""
        return ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp']

    def can_convert(self, file_path: Path) -> bool:
        """Check if this converter can handle image files."""
        if not self.client:
            self.logger.error("OpenAI client not initialized. Check OPENAI_API_KEY in environment.")
            return False
        return file_path.suffix.lower() in self.get_supported_extensions()

    def _prepare_image_for_api(self, image_path: Path) -> Optional[str]:
        """
        Prepare image for API by resizing if needed and converting to base64.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Base64 encoded image string or None if processing failed
        """
        try:
            # Open and process the image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary (for formats like PNG with transparency)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Check file size and resize if necessary
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG', quality=self.image_quality, optimize=True)
                img_size_mb = len(img_byte_arr.getvalue()) / (1024 * 1024)
                
                if img_size_mb > self.max_image_size_mb:
                    # Calculate resize ratio to fit within size limit
                    resize_ratio = (self.max_image_size_mb / img_size_mb) ** 0.5
                    new_width = int(img.width * resize_ratio)
                    new_height = int(img.height * resize_ratio)
                    
                    self.logger.info(f"Resizing image from {img.width}x{img.height} to {new_width}x{new_height}")
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Re-encode with new size
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='JPEG', quality=self.image_quality, optimize=True)
                
                # Convert to base64
                img_byte_arr.seek(0)
                img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
                
                self.logger.info(f"Image prepared for API: {len(img_base64)} characters")
                return img_base64
                
        except Exception as e:
            self.logger.error(f"Error preparing image {image_path}: {str(e)}")
            return None

    def _extract_text_with_ai_vision(self, image_path: Path) -> str:
        """
        Extract text content from image using AI vision API.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Extracted text content formatted as markdown
        """
        if not self.client:
            return f"# Error: AI Vision Not Available\n\nOpenAI API key not configured for image: {image_path.name}\n"
        
        try:
            # Prepare image for API
            image_base64 = self._prepare_image_for_api(image_path)
            if not image_base64:
                return f"# Error Processing Image\n\nFailed to prepare image: {image_path.name}\n"
            
            # Create the vision prompt
            prompt = """Please analyze this image and extract all text content. Format your response as clean Markdown with the following guidelines:

1. Use appropriate heading levels (# ## ###) for titles and section headers
2. Preserve the original structure and hierarchy of the content
3. Convert tables to proper Markdown table format
4. Use bullet points or numbered lists where appropriate
5. Bold important text using **bold** formatting
6. Include any captions, labels, or annotations
7. If the image contains charts or diagrams, describe them briefly
8. Maintain the logical flow and organization of the content

Focus on accuracy and readability. If text is unclear or partially obscured, indicate this with [unclear] or [partially visible]."""

            # Make API call to OpenAI Vision
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Extract the response content
            if response.choices and response.choices[0].message.content:
                extracted_content = response.choices[0].message.content.strip()
                self.logger.info(f"Successfully extracted {len(extracted_content)} characters from {image_path.name}")
                return extracted_content
            else:
                self.logger.warning(f"No content extracted from {image_path.name}")
                return f"# {image_path.stem}\n\nNo text content could be extracted from this image.\n"
                
        except Exception as e:
            self.logger.error(f"Error extracting text from image {image_path}: {str(e)}")
            return f"# Error Extracting Text\n\nFailed to extract text from {image_path.name}: {str(e)}\n"

    def _convert_document_to_markdown(self, doc_path: Path) -> str:
        """Convert an image file to Markdown format using AI vision."""
        try:
            self.logger.info(f"Converting image to markdown: {doc_path}")
            
            # Extract text using AI vision
            markdown_content = self._extract_text_with_ai_vision(doc_path)
            
            # Add metadata header
            metadata_header = f"<!-- Converted from image: {doc_path.name} -->\n"
            metadata_header += f"<!-- Conversion method: AI Vision (OpenAI {self.model}) -->\n"
            metadata_header += f"<!-- Original file: {doc_path.absolute()} -->\n\n"
            
            return metadata_header + markdown_content
            
        except Exception as e:
            self.logger.error(f"Error converting image document {doc_path}: {str(e)}")
            return f"# Error Converting Image\n\nFailed to convert {doc_path.name}: {str(e)}\n"
