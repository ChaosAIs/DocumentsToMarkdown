#!/usr/bin/env python3
"""
OpenAI AI Service Implementation

This module provides OpenAI-specific implementation of the AI service interface.
"""

from pathlib import Path
from typing import Dict, Any
import os

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from .base_ai_service import BaseAIService, AIServiceUnavailableError, AIServiceConfigurationError


class OpenAIService(BaseAIService):
    """OpenAI implementation of the AI service."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize OpenAI service.
        
        Args:
            config: Configuration dictionary with OpenAI settings
        """
        super().__init__(config)
        
        # Extract OpenAI-specific configuration
        self.api_key = config.get('api_key') or os.getenv('OPENAI_API_KEY')
        self.model = config.get('model', 'gpt-4o')
        self.max_tokens = config.get('max_tokens', 4096)
        self.temperature = config.get('temperature', 0.1)
        self.base_url = config.get('base_url') or os.getenv('OPENAI_BASE_URL')
        
        # Initialize client
        self.client = None
        if self.api_key and OpenAI:
            try:
                client_kwargs = {'api_key': self.api_key}
                if self.base_url:
                    client_kwargs['base_url'] = self.base_url
                    
                self.client = OpenAI(**client_kwargs)
                self.logger.info("OpenAI client initialized successfully")
            except Exception as e:
                self.logger.error(f"Error initializing OpenAI client: {e}")
                self.client = None
    
    def is_available(self) -> bool:
        """Check if OpenAI service is available."""
        if not OpenAI:
            self.logger.error("OpenAI library not installed")
            return False
            
        if not self.api_key:
            self.logger.error("OpenAI API key not configured")
            return False
            
        if not self.client:
            self.logger.error("OpenAI client not initialized")
            return False
            
        return True
    
    def get_service_name(self) -> str:
        """Get the service name."""
        return "OpenAI"
    
    def get_model_name(self) -> str:
        """Get the model name."""
        return self.model
    
    def extract_text_from_image(self, image_path: Path, prompt: str) -> str:
        """
        Extract text from image using OpenAI Vision API.
        
        Args:
            image_path: Path to the image file
            prompt: Text prompt to guide the extraction
            
        Returns:
            Extracted text content formatted as markdown
        """
        if not self.is_available():
            raise AIServiceUnavailableError("OpenAI service is not available")
        
        try:
            # Prepare image for API
            image_base64 = self._prepare_image_for_processing(image_path)
            if not image_base64:
                return f"# Error Processing Image\n\nFailed to prepare image: {image_path.name}\n"
            
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
