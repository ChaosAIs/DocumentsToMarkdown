#!/usr/bin/env python3
"""
Configuration Management for Documents to Markdown

This module handles configuration file creation, validation, and management
for users who install the package via pip.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import json

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


class ConfigManager:
    """Manages configuration files and settings for the package."""
    
    def __init__(self):
        self.config_dir = self._get_config_directory()
        self.config_file = self.config_dir / "config.json"
        self.env_file = self.config_dir / ".env"
        
    def _get_config_directory(self) -> Path:
        """Get the appropriate configuration directory for the current OS."""
        if sys.platform == "win32":
            # Windows: Use APPDATA
            config_dir = Path(os.environ.get("APPDATA", "")) / "documents-to-markdown"
        elif sys.platform == "darwin":
            # macOS: Use ~/Library/Application Support
            config_dir = Path.home() / "Library" / "Application Support" / "documents-to-markdown"
        else:
            # Linux/Unix: Use XDG_CONFIG_HOME or ~/.config
            xdg_config = os.environ.get("XDG_CONFIG_HOME", "")
            if xdg_config:
                config_dir = Path(xdg_config) / "documents-to-markdown"
            else:
                config_dir = Path.home() / ".config" / "documents-to-markdown"
        
        return config_dir
    
    def ensure_config_directory(self) -> None:
        """Create configuration directory if it doesn't exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration values."""
        return {
            "ai_service": "",  # Auto-detection if empty
            "add_section_numbers": True,
            "verbose_logging": False,
            "file_paths": {
                "input_folder": "input",
                "output_folder": "output"
            },
            "openai": {
                "api_key": "",
                "model": "gpt-4o",
                "max_tokens": 4096,
                "temperature": 0.1,
                "base_url": "https://api.openai.com/v1"
            },
            "ollama": {
                "base_url": "http://localhost:11434",
                "model": "llava:latest",
                "timeout": 120,
                "temperature": 0.1
            },
            "image_processing": {
                "max_size_mb": 20,
                "quality_compression": 85,
                "max_size_pixels": 2048
            },
            "logging": {
                "level": "INFO",
                "file_logging": False,
                "log_file": "documents_to_markdown.log"
            }
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file, creating default if needed."""
        # Start with default configuration
        config = self.get_default_config()

        # Load from config file if it exists
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                config = self._merge_configs(config, file_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file: {e}")

        # Load environment variables and merge them
        config = self._merge_env_vars(config)

        return config
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file."""
        try:
            self.ensure_config_directory()
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving config: {e}")
            return False
    
    def _merge_configs(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge user config with defaults."""
        result = default.copy()

        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def _merge_env_vars(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge environment variables into configuration."""
        # Load .env file if available
        if load_dotenv:
            load_dotenv()

        # File paths configuration
        input_folder = os.getenv('INPUT_FOLDER')
        if input_folder:
            config['file_paths']['input_folder'] = input_folder

        output_folder = os.getenv('OUTPUT_FOLDER')
        if output_folder:
            config['file_paths']['output_folder'] = output_folder

        # AI service configuration
        ai_service = os.getenv('AI_SERVICE')
        if ai_service:
            config['ai_service'] = ai_service

        # OpenAI configuration
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key:
            config['openai']['api_key'] = openai_api_key

        openai_model = os.getenv('OPENAI_MODEL')
        if openai_model:
            config['openai']['model'] = openai_model

        openai_max_tokens = os.getenv('OPENAI_MAX_TOKENS')
        if openai_max_tokens:
            try:
                config['openai']['max_tokens'] = int(openai_max_tokens)
            except ValueError:
                pass

        openai_temperature = os.getenv('OPENAI_TEMPERATURE')
        if openai_temperature:
            try:
                config['openai']['temperature'] = float(openai_temperature)
            except ValueError:
                pass

        openai_base_url = os.getenv('OPENAI_BASE_URL')
        if openai_base_url:
            config['openai']['base_url'] = openai_base_url

        # OLLAMA configuration
        ollama_base_url = os.getenv('OLLAMA_BASE_URL')
        if ollama_base_url:
            config['ollama']['base_url'] = ollama_base_url

        ollama_model = os.getenv('OLLAMA_MODEL')
        if ollama_model:
            config['ollama']['model'] = ollama_model

        ollama_timeout = os.getenv('OLLAMA_TIMEOUT')
        if ollama_timeout:
            try:
                config['ollama']['timeout'] = int(ollama_timeout)
            except ValueError:
                pass

        ollama_temperature = os.getenv('OLLAMA_TEMPERATURE')
        if ollama_temperature:
            try:
                config['ollama']['temperature'] = float(ollama_temperature)
            except ValueError:
                pass

        # Image processing configuration
        image_max_size_mb = os.getenv('IMAGE_MAX_SIZE_MB')
        if image_max_size_mb:
            try:
                config['image_processing']['max_size_mb'] = int(image_max_size_mb)
            except ValueError:
                pass

        image_quality = os.getenv('IMAGE_QUALITY_COMPRESSION')
        if image_quality:
            try:
                config['image_processing']['quality_compression'] = int(image_quality)
            except ValueError:
                pass

        image_max_pixels = os.getenv('IMAGE_MAX_SIZE_PIXELS')
        if image_max_pixels:
            try:
                config['image_processing']['max_size_pixels'] = int(image_max_pixels)
            except ValueError:
                pass

        # Logging configuration
        log_level = os.getenv('LOG_LEVEL')
        if log_level:
            config['logging']['level'] = log_level

        return config
    
    def create_env_file(self, config: Dict[str, Any]) -> bool:
        """Create .env file from configuration."""
        try:
            self.ensure_config_directory()
            
            env_content = []
            env_content.append("# Documents to Markdown Configuration")
            env_content.append("# Generated automatically - edit config.json instead")
            env_content.append("")
            
            # AI Service selection
            if config.get("ai_service"):
                env_content.append(f"AI_SERVICE={config['ai_service']}")

            # File paths settings
            file_paths_config = config.get("file_paths", {})
            if file_paths_config.get("input_folder"):
                env_content.append(f"INPUT_FOLDER={file_paths_config['input_folder']}")
            if file_paths_config.get("output_folder"):
                env_content.append(f"OUTPUT_FOLDER={file_paths_config['output_folder']}")

            # OpenAI settings
            openai_config = config.get("openai", {})
            if openai_config.get("api_key"):
                env_content.append(f"OPENAI_API_KEY={openai_config['api_key']}")
            if openai_config.get("model"):
                env_content.append(f"OPENAI_MODEL={openai_config['model']}")
            if openai_config.get("max_tokens"):
                env_content.append(f"OPENAI_MAX_TOKENS={openai_config['max_tokens']}")
            if openai_config.get("temperature") is not None:
                env_content.append(f"OPENAI_TEMPERATURE={openai_config['temperature']}")
            if openai_config.get("base_url"):
                env_content.append(f"OPENAI_BASE_URL={openai_config['base_url']}")
            
            # OLLAMA settings
            ollama_config = config.get("ollama", {})
            if ollama_config.get("base_url"):
                env_content.append(f"OLLAMA_BASE_URL={ollama_config['base_url']}")
            if ollama_config.get("model"):
                env_content.append(f"OLLAMA_MODEL={ollama_config['model']}")
            if ollama_config.get("timeout"):
                env_content.append(f"OLLAMA_TIMEOUT={ollama_config['timeout']}")
            if ollama_config.get("temperature") is not None:
                env_content.append(f"OLLAMA_TEMPERATURE={ollama_config['temperature']}")
            
            # Image processing settings
            image_config = config.get("image_processing", {})
            if image_config.get("max_size_mb"):
                env_content.append(f"IMAGE_MAX_SIZE_MB={image_config['max_size_mb']}")
            if image_config.get("quality_compression"):
                env_content.append(f"IMAGE_QUALITY_COMPRESSION={image_config['quality_compression']}")
            if image_config.get("max_size_pixels"):
                env_content.append(f"IMAGE_MAX_SIZE_PIXELS={image_config['max_size_pixels']}")
            
            # Logging settings
            logging_config = config.get("logging", {})
            if logging_config.get("level"):
                env_content.append(f"LOG_LEVEL={logging_config['level']}")
            
            with open(self.env_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(env_content))
            
            return True
            
        except IOError as e:
            print(f"Error creating .env file: {e}")
            return False
    
    def get_config_info(self) -> Dict[str, Any]:
        """Get information about configuration files and locations."""
        return {
            "config_directory": str(self.config_dir),
            "config_file": str(self.config_file),
            "env_file": str(self.env_file),
            "config_exists": self.config_file.exists(),
            "env_exists": self.env_file.exists(),
            "config_directory_exists": self.config_dir.exists()
        }
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        """Validate configuration and return list of issues."""
        issues = []

        # Check AI service configuration
        ai_service = config.get("ai_service", "").lower()
        if ai_service and ai_service not in ["openai", "ollama", "none", ""]:
            issues.append(f"Invalid AI service: {ai_service}. Must be 'openai', 'ollama', 'none', or empty for auto-detection.")

        # Check OpenAI configuration
        openai_config = config.get("openai", {})
        if ai_service == "openai" or not ai_service:
            if not openai_config.get("api_key"):
                issues.append("OpenAI API key is required when using OpenAI service.")

        # Check OLLAMA configuration
        ollama_config = config.get("ollama", {})
        if ai_service == "ollama" or not ai_service:
            base_url = ollama_config.get("base_url", "")
            if not base_url:
                issues.append("OLLAMA base URL is required when using OLLAMA service.")
            elif not base_url.startswith(("http://", "https://")):
                issues.append("OLLAMA base URL must start with http:// or https://")

        # Check image processing settings
        image_config = config.get("image_processing", {})
        max_size_mb = image_config.get("max_size_mb", 0)
        if max_size_mb <= 0:
            issues.append("Image max size must be greater than 0 MB.")

        quality = image_config.get("quality_compression", 0)
        if not (1 <= quality <= 100):
            issues.append("Image quality compression must be between 1 and 100.")

        # Check file paths settings
        file_paths_config = config.get("file_paths", {})
        input_folder = file_paths_config.get("input_folder", "")
        output_folder = file_paths_config.get("output_folder", "")

        if not input_folder:
            issues.append("Input folder path cannot be empty.")
        if not output_folder:
            issues.append("Output folder path cannot be empty.")
        if input_folder == output_folder:
            issues.append("Input and output folders cannot be the same.")

        return issues

    def test_ai_services(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Test AI service connectivity and return status."""
        results = {
            "ollama": {"available": False, "error": None},
            "openai": {"available": False, "error": None}
        }

        # Test OLLAMA
        ollama_config = config.get("ollama", {})
        base_url = ollama_config.get("base_url", "http://localhost:11434")

        try:
            import requests
            response = requests.get(f"{base_url}/api/version", timeout=5)
            if response.status_code == 200:
                results["ollama"]["available"] = True
                # Try to check if vision model is available
                try:
                    model_response = requests.get(f"{base_url}/api/tags", timeout=5)
                    if model_response.status_code == 200:
                        models = model_response.json().get("models", [])
                        vision_models = [m for m in models if "llava" in m.get("name", "").lower()]
                        if vision_models:
                            results["ollama"]["model"] = vision_models[0]["name"]
                        else:
                            results["ollama"]["error"] = "No vision models (llava) found. Run: ollama pull llava:latest"
                except:
                    pass
            else:
                results["ollama"]["error"] = f"OLLAMA server responded with status {response.status_code}"
        except requests.exceptions.ConnectionError:
            results["ollama"]["error"] = "Cannot connect to OLLAMA server. Is it running?"
        except requests.exceptions.Timeout:
            results["ollama"]["error"] = "OLLAMA server timeout"
        except Exception as e:
            results["ollama"]["error"] = f"OLLAMA test failed: {str(e)}"

        # Test OpenAI
        openai_config = config.get("openai", {})
        api_key = openai_config.get("api_key")

        if api_key:
            try:
                import requests
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                base_url = openai_config.get("base_url", "https://api.openai.com/v1")
                response = requests.get(f"{base_url}/models", headers=headers, timeout=10)

                if response.status_code == 200:
                    results["openai"]["available"] = True
                    # Check if vision model is available
                    models = response.json().get("data", [])
                    vision_models = [m for m in models if "gpt-4" in m.get("id", "") and "vision" in m.get("id", "")]
                    if vision_models:
                        results["openai"]["model"] = vision_models[0]["id"]
                    else:
                        # Check for gpt-4o which has vision capabilities
                        gpt4o_models = [m for m in models if "gpt-4o" in m.get("id", "")]
                        if gpt4o_models:
                            results["openai"]["model"] = gpt4o_models[0]["id"]
                elif response.status_code == 401:
                    results["openai"]["error"] = "Invalid API key"
                elif response.status_code == 429:
                    results["openai"]["error"] = "Rate limit exceeded or insufficient credits"
                else:
                    results["openai"]["error"] = f"API responded with status {response.status_code}"
            except requests.exceptions.ConnectionError:
                results["openai"]["error"] = "Cannot connect to OpenAI API"
            except requests.exceptions.Timeout:
                results["openai"]["error"] = "OpenAI API timeout"
            except Exception as e:
                results["openai"]["error"] = f"OpenAI test failed: {str(e)}"
        else:
            results["openai"]["error"] = "No API key configured"

        return results
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to default values."""
        default_config = self.get_default_config()
        return self.save_config(default_config)


# Global config manager instance
config_manager = ConfigManager()


def get_config() -> Dict[str, Any]:
    """Get current configuration."""
    return config_manager.load_config()


def save_config(config: Dict[str, Any]) -> bool:
    """Save configuration."""
    return config_manager.save_config(config)


def get_config_directory() -> Path:
    """Get configuration directory path."""
    return config_manager.config_dir


def ensure_config_exists() -> Dict[str, Any]:
    """Ensure configuration exists, creating default if needed."""
    config = config_manager.load_config()
    if not config_manager.config_file.exists():
        config_manager.save_config(config)
        config_manager.create_env_file(config)
    return config


def get_input_folder() -> str:
    """Get the configured input folder path."""
    config = get_config()
    return config.get('file_paths', {}).get('input_folder', 'input')


def get_output_folder() -> str:
    """Get the configured output folder path."""
    config = get_config()
    return config.get('file_paths', {}).get('output_folder', 'output')
