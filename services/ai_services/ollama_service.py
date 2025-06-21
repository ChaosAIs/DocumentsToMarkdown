#!/usr/bin/env python3
"""
OLLAMA AI Service Implementation

This module provides OLLAMA-specific implementation of the AI service interface.
OLLAMA is a local AI inference server that can run models like LLaVA for vision tasks.
"""

from pathlib import Path
from typing import Dict, Any
import os
import json

try:
    import requests
except ImportError:
    requests = None

from .base_ai_service import BaseAIService, AIServiceUnavailableError, AIServiceConfigurationError


class OllamaService(BaseAIService):
    """OLLAMA implementation of the AI service."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize OLLAMA service.
        
        Args:
            config: Configuration dictionary with OLLAMA settings
        """
        super().__init__(config)
        
        # Extract OLLAMA-specific configuration
        self.base_url = config.get('base_url', 'http://localhost:11434')
        self.model = config.get('model', 'llava:latest')
        self.timeout = config.get('timeout', 120)  # OLLAMA can be slower than cloud APIs
        self.temperature = config.get('temperature', 0.1)
        
        # Ensure base_url doesn't end with slash
        self.base_url = self.base_url.rstrip('/')
        
        # API endpoints
        self.generate_endpoint = f"{self.base_url}/api/generate"
        self.tags_endpoint = f"{self.base_url}/api/tags"
        
    def is_available(self) -> bool:
        """Check if OLLAMA service is available."""
        if not requests:
            self.logger.error("requests library not installed")
            return False
        
        try:
            # Check if OLLAMA server is running
            response = requests.get(self.tags_endpoint, timeout=5)
            if response.status_code != 200:
                self.logger.error(f"OLLAMA server not responding: {response.status_code}")
                return False
            
            # Check if the specified model is available
            models_data = response.json()
            available_models = [model['name'] for model in models_data.get('models', [])]
            
            if self.model not in available_models:
                self.logger.error(f"Model '{self.model}' not found in OLLAMA. Available models: {available_models}")
                self.logger.info("To install the model, run: ollama pull llava:latest")
                return False
            
            self.logger.info(f"OLLAMA service available with model: {self.model}")
            return True
            
        except requests.exceptions.ConnectionError:
            self.logger.error("Cannot connect to OLLAMA server. Make sure OLLAMA is running.")
            self.logger.info("Start OLLAMA with: ollama serve")
            return False
        except Exception as e:
            self.logger.error(f"Error checking OLLAMA availability: {e}")
            return False
    
    def get_service_name(self) -> str:
        """Get the service name."""
        return "OLLAMA"
    
    def get_model_name(self) -> str:
        """Get the model name."""
        return self.model
    
    def extract_text_from_image(self, image_path: Path, prompt: str) -> str:
        """
        Extract text from image using OLLAMA Vision API.
        
        Args:
            image_path: Path to the image file
            prompt: Text prompt to guide the extraction
            
        Returns:
            Extracted text content formatted as markdown
        """
        if not self.is_available():
            raise AIServiceUnavailableError("OLLAMA service is not available")
        
        try:
            # Prepare image for API
            image_base64 = self._prepare_image_for_processing(image_path)
            if not image_base64:
                return f"# Error Processing Image\n\nFailed to prepare image: {image_path.name}\n"
            
            # Prepare the request payload for OLLAMA
            payload = {
                "model": self.model,
                "prompt": prompt,
                "images": [image_base64],
                "stream": False,
                "options": {
                    "temperature": self.temperature
                }
            }
            
            # Make API call to OLLAMA
            self.logger.info(f"Sending request to OLLAMA for image: {image_path.name}")
            response = requests.post(
                self.generate_endpoint,
                json=payload,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code != 200:
                error_msg = f"OLLAMA API error: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                return f"# Error Extracting Text\n\n{error_msg}\n"
            
            # Parse the response
            response_data = response.json()
            extracted_content = response_data.get('response', '').strip()
            
            if extracted_content:
                self.logger.info(f"Successfully extracted {len(extracted_content)} characters from {image_path.name}")
                return extracted_content
            else:
                self.logger.warning(f"No content extracted from {image_path.name}")
                return f"# {image_path.stem}\n\nNo text content could be extracted from this image.\n"
                
        except requests.exceptions.Timeout:
            error_msg = f"OLLAMA request timed out after {self.timeout} seconds"
            self.logger.error(error_msg)
            return f"# Error Extracting Text\n\n{error_msg}\n"
        except Exception as e:
            self.logger.error(f"Error extracting text from image {image_path}: {str(e)}")
            return f"# Error Extracting Text\n\nFailed to extract text from {image_path.name}: {str(e)}\n"
