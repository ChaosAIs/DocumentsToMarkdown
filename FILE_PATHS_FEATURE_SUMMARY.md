# File Paths Configuration Feature - Implementation Summary

## Overview

Successfully implemented configurable input and output folder support for the Documents to Markdown converter. Users can now set default input and output folders through environment variables, configuration files, and CLI commands.

## Changes Made

### 1. Environment Variables Support

**File: `.env.template`**
- Added `INPUT_FOLDER` and `OUTPUT_FOLDER` environment variables
- Added comprehensive documentation and examples
- Maintains backward compatibility with existing configuration

### 2. Configuration System Updates

**File: `documents_to_markdown/config.py`**
- Added `file_paths` section to default configuration
- Implemented `_merge_env_vars()` method to load environment variables
- Added `get_input_folder()` and `get_output_folder()` utility functions
- Enhanced validation to check file paths (empty paths, same input/output)
- Updated `.env` file generation to include file paths
- Added dotenv import with fallback for environments without python-dotenv

### 3. CLI Integration

**File: `documents_to_markdown/cli.py`**
- Updated argument parser to use configured defaults dynamically
- Enhanced `--config show` to display file paths configuration
- Added file paths prompts to interactive setup (`--config init`)
- Updated help text to show current configured defaults
- Added support for setting file paths via `--config set` command

### 4. API Integration

**File: `documents_to_markdown/api.py`**
- Updated `DocumentConverter` class to use configured defaults
- Modified `_get_manager()` method to accept None values and use configured defaults
- Updated `convert_all()` method to use configured defaults when parameters are None
- Updated convenience functions (`convert_folder()`) to support configured defaults
- Maintained backward compatibility with explicit folder parameters

### 5. Documentation

**Files: `README.md`, `FILE_PATHS_CONFIGURATION_GUIDE.md`**
- Added comprehensive documentation for the new feature
- Updated README.md to mention configurable file paths
- Created detailed configuration guide with examples
- Added environment variable examples
- Documented configuration priority order
- Added troubleshooting section

## Configuration Priority Order

The system follows this priority order (highest to lowest):

1. **Command-line arguments** (`--input`, `--output`)
2. **Environment variables** (`INPUT_FOLDER`, `OUTPUT_FOLDER`)
3. **Configuration file** (`config.json`)
4. **Default values** (`input`, `output`)

## Usage Examples

### Environment Variables
```bash
# Set via .env file
INPUT_FOLDER=my_documents
OUTPUT_FOLDER=my_markdown

# Set via system environment
export INPUT_FOLDER=documents
export OUTPUT_FOLDER=markdown
```

### CLI Configuration
```bash
# Set via CLI commands
documents-to-markdown --config set file_paths.input_folder my_docs
documents-to-markdown --config set file_paths.output_folder my_output

# View current configuration
documents-to-markdown --config show

# Use configured defaults
documents-to-markdown

# Override for specific run
documents-to-markdown --input custom_docs --output custom_output
```

### API Usage
```python
from documents_to_markdown import DocumentConverter

# Uses configured defaults
converter = DocumentConverter()
results = converter.convert_all()

# Override with explicit folders
results = converter.convert_all("custom_input", "custom_output")
```

## Validation Rules

The configuration system validates:
- ✅ Input folder cannot be empty
- ✅ Output folder cannot be empty  
- ✅ Input and output folders cannot be the same

## Backward Compatibility

- ✅ All existing code continues to work unchanged
- ✅ Default behavior remains the same (`input` → `output`)
- ✅ Explicit folder parameters still override defaults
- ✅ No breaking changes to existing APIs

## Testing

Comprehensive testing was implemented covering:
- ✅ Default configuration loading
- ✅ Environment variable override
- ✅ CLI configuration commands
- ✅ API integration
- ✅ Configuration validation
- ✅ .env file generation
- ✅ Configuration priority order
- ✅ Backward compatibility

## Benefits

1. **Flexibility**: Users can configure default folders to match their workflow
2. **Convenience**: No need to specify folders on every command
3. **Integration**: Works seamlessly with CI/CD pipelines and scripts
4. **Consistency**: Same configuration system as other settings
5. **Documentation**: Comprehensive guides and examples

## Files Modified

1. `.env.template` - Added file paths environment variables
2. `documents_to_markdown/config.py` - Core configuration system updates
3. `documents_to_markdown/cli.py` - CLI integration and commands
4. `documents_to_markdown/api.py` - API integration with configured defaults
5. `README.md` - Updated documentation
6. `FILE_PATHS_CONFIGURATION_GUIDE.md` - New comprehensive guide

## Implementation Quality

- ✅ **Robust**: Handles edge cases and validation
- ✅ **Tested**: Comprehensive test coverage
- ✅ **Documented**: Clear documentation and examples
- ✅ **Compatible**: Maintains backward compatibility
- ✅ **Consistent**: Follows existing patterns and conventions
- ✅ **User-friendly**: Intuitive configuration and usage

The file paths configuration feature is now fully implemented and ready for use!
