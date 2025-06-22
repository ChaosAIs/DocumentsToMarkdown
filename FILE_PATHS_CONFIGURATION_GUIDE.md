# File Paths Configuration Guide

This guide explains how to configure default input and output folders for the Documents to Markdown converter using environment variables and configuration files.

## Overview

The Documents to Markdown converter now supports configurable default input and output folders through:

- **Environment variables** (`.env` file or system environment)
- **Configuration file** (`config.json`)
- **Interactive setup** (CLI configuration wizard)
- **Command-line arguments** (for per-run overrides)

## Configuration Methods

### 1. Environment Variables (.env file)

Create or edit a `.env` file in your project directory:

```bash
# File Paths Configuration
INPUT_FOLDER=my_documents
OUTPUT_FOLDER=my_markdown

# Other configuration...
AI_SERVICE=openai
OPENAI_API_KEY=your_key_here
```

**Supported Environment Variables:**
- `INPUT_FOLDER` - Default input folder path
- `OUTPUT_FOLDER` - Default output folder path

### 2. Configuration File

The configuration is automatically saved to a JSON file in your user configuration directory:

**Location:**
- **Windows:** `%APPDATA%\documents-to-markdown\config.json`
- **macOS:** `~/Library/Application Support/documents-to-markdown/config.json`
- **Linux:** `~/.config/documents-to-markdown/config.json`

**Example config.json:**
```json
{
  "ai_service": "",
  "add_section_numbers": true,
  "verbose_logging": false,
  "file_paths": {
    "input_folder": "my_documents",
    "output_folder": "my_markdown"
  },
  "openai": {
    "api_key": "your_key_here",
    "model": "gpt-4o"
  }
}
```

### 3. Interactive Setup

Use the CLI configuration wizard to set up file paths interactively:

```bash
# Run interactive setup
documents-to-markdown --config init

# Or using Python module
python -m documents_to_markdown.cli --config init
```

The wizard will prompt you for:
- AI service selection
- Section numbering preference
- Verbose logging preference
- **Input folder path**
- **Output folder path**

### 4. Command-Line Configuration

Set configuration values directly from the command line:

```bash
# Set input folder
documents-to-markdown --config set --config-key file_paths.input_folder --config-value my_docs

# Set output folder
documents-to-markdown --config set --config-key file_paths.output_folder --config-value my_output

# View current configuration
documents-to-markdown --config show

# Validate configuration
documents-to-markdown --config validate
```

## Usage Examples

### CLI Usage with Configured Defaults

Once configured, the CLI will use your default folders automatically:

```bash
# Uses configured input and output folders
documents-to-markdown

# Override with custom folders for this run
documents-to-markdown --input custom_docs --output custom_output

# Single file conversion (ignores folder configuration)
documents-to-markdown --file document.docx output.md
```

### API Usage with Configured Defaults

The Python API automatically uses configured defaults:

```python
from documents_to_markdown import DocumentConverter

# Uses configured default folders
converter = DocumentConverter()
results = converter.convert_all()

# Override with explicit folders
results = converter.convert_all("custom_input", "custom_output")

# Convenience function uses defaults
from documents_to_markdown import convert_folder
results = convert_folder()  # Uses configured defaults
```

### Programmatic Configuration

You can also configure paths programmatically:

```python
from documents_to_markdown.config import get_config, save_config

# Load current configuration
config = get_config()

# Modify file paths
config['file_paths']['input_folder'] = 'my_custom_input'
config['file_paths']['output_folder'] = 'my_custom_output'

# Save configuration
save_config(config)
```

## Configuration Priority

The configuration system follows this priority order (highest to lowest):

1. **Command-line arguments** (`--input`, `--output`)
2. **Environment variables** (`INPUT_FOLDER`, `OUTPUT_FOLDER`)
3. **Configuration file** (`config.json`)
4. **Default values** (`input`, `output`)

## Validation Rules

The configuration system validates file paths with these rules:

- ✅ **Input folder cannot be empty**
- ✅ **Output folder cannot be empty**
- ✅ **Input and output folders cannot be the same**

Use `documents-to-markdown --config validate` to check your configuration.

## Path Examples

### Relative Paths
```bash
INPUT_FOLDER=documents        # ./documents
OUTPUT_FOLDER=markdown        # ./markdown
INPUT_FOLDER=../shared_docs   # ../shared_docs
```

### Absolute Paths
```bash
# Windows
INPUT_FOLDER=C:\Users\YourName\Documents
OUTPUT_FOLDER=C:\Users\YourName\Markdown

# macOS/Linux
INPUT_FOLDER=/Users/yourname/Documents
OUTPUT_FOLDER=/Users/yourname/Markdown
```

### Special Folders
```bash
INPUT_FOLDER=~/Documents      # User's Documents folder
OUTPUT_FOLDER=~/Desktop/MD    # Desktop subfolder
```

## Troubleshooting

### Check Current Configuration
```bash
documents-to-markdown --config show
```

### Validate Configuration
```bash
documents-to-markdown --config validate
```

### Reset to Defaults
```bash
documents-to-markdown --config reset
```

### View Configuration File Location
```bash
documents-to-markdown --config location
```

### Common Issues

**Issue:** "Input and output folders cannot be the same"
**Solution:** Set different paths for input and output folders

**Issue:** Configuration not taking effect
**Solution:** Check that environment variables are properly set and restart your terminal

**Issue:** Permission errors
**Solution:** Ensure you have read/write permissions for the configured folders

## Integration with Existing Workflows

### Batch Processing Scripts
```bash
#!/bin/bash
# Set custom folders for this session
export INPUT_FOLDER="./batch_input"
export OUTPUT_FOLDER="./batch_output"

# Run conversion
documents-to-markdown
```

### CI/CD Pipelines
```yaml
# GitHub Actions example
env:
  INPUT_FOLDER: docs
  OUTPUT_FOLDER: generated_markdown
  
steps:
  - name: Convert documents
    run: documents-to-markdown
```

### Docker Containers
```dockerfile
ENV INPUT_FOLDER=/app/documents
ENV OUTPUT_FOLDER=/app/markdown
```

This flexible configuration system allows you to adapt the Documents to Markdown converter to your specific workflow and directory structure while maintaining backward compatibility with existing usage patterns.
