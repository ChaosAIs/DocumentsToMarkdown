# Documents to Markdown Converter

A comprehensive Python library for converting various document types to Markdown format with AI-powered image extraction and processing capabilities.

[![PyPI version](https://badge.fury.io/py/documents-to-markdown.svg)](https://badge.fury.io/py/documents-to-markdown)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

### Installation

```bash
# Install the latest version from PyPI
pip install documents-to-markdown==1.0.0

# Or install without version specification (gets latest)
pip install documents-to-markdown

# Or install from source
git clone https://github.com/ChaosAIs/DocumentsToMarkdown.git
cd DocumentsToMarkdown
pip install -e .
```

### Library Usage

```python
from documents_to_markdown import DocumentConverter

# Initialize converter
converter = DocumentConverter()

# Convert a single file
success = converter.convert_file("document.docx", "output.md")
print(f"Conversion successful: {success}")

# Convert all files in a folder
results = converter.convert_all("input_folder", "output_folder")
print(f"Converted {results['successful_conversions']} files")
```

### Command Line Usage

```bash
# Convert all files in input folder
documents-to-markdown

# Convert specific file
documents-to-markdown --file document.docx output.md

# Custom input/output folders
documents-to-markdown --input docs --output markdown

# Show help
documents-to-markdown --help
```

## 📋 Supported Formats

- **Word Documents**: `.docx`, `.doc`
- **PDF Documents**: `.pdf`
- **Excel Spreadsheets**: `.xlsx`, `.xlsm`, `.xls`
- **Images**: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.tiff` (AI-powered)
- **Plain Text**: `.txt`, `.csv`, `.tsv`, `.log` (AI-enhanced)

## ✨ Features

### Core Capabilities
- **Multi-format support**: Word, PDF, Excel, Plain Text, and Image documents
- **AI-powered processing**: Choose between OpenAI (cloud) and OLLAMA (local)
- **Batch processing**: Convert multiple documents efficiently
- **Preserves formatting**: Bold, italic, tables, and document structure
- **Automatic section numbering**: Hierarchical numbering (1, 1.1, 1.2, etc.)
- **Configurable file paths**: Set default input/output folders via environment variables
- **Modular architecture**: Extensible converter system

### AI-Enhanced Features
- **Image text extraction**: Extract text from images using AI vision
- **Embedded image processing**: Process images within Word/PDF documents
- **Flowchart conversion**: Convert flowcharts to ASCII diagrams
- **Smart text processing**: AI-enhanced plain text formatting
- **Privacy options**: Local AI processing with OLLAMA

## 📚 Library API

### Basic Usage

```python
from documents_to_markdown import DocumentConverter

# Initialize converter
converter = DocumentConverter(
    add_section_numbers=True,  # Enable section numbering
    verbose=False              # Enable verbose logging
)

# Convert single file
success = converter.convert_file("input.docx", "output.md")

# Convert all files in folder
results = converter.convert_all("input_folder", "output_folder")

# Check supported formats
formats = converter.get_supported_formats()
print(f"Supported: {formats}")

# Check if file can be converted
if converter.can_convert("document.pdf"):
    print("File can be converted!")
```

### Advanced Usage

```python
from documents_to_markdown import DocumentConverter, convert_document, convert_folder

# Quick single file conversion
success = convert_document("report.docx", "report.md")

# Quick folder conversion
results = convert_folder("documents", "markdown_output")

# Advanced converter configuration
converter = DocumentConverter()
converter.set_section_numbering(False)  # Disable numbering
converter.set_verbose_logging(True)     # Enable debug output

# Get detailed statistics
stats = converter.get_conversion_statistics()
print(f"Available converters: {stats['total_converters']}")
for conv in stats['converters']:
    print(f"- {conv['name']}: {', '.join(conv['supported_extensions'])}")
```

### Working with Results

```python
# Convert folder and handle results
results = converter.convert_all("input", "output")

print(f"Total files: {results['total_files']}")
print(f"Successful: {results['successful_conversions']}")
print(f"Failed: {results['failed_conversions']}")

# Process individual results
for result in results['results']:
    status = "✓" if result['status'] == 'success' else "✗"
    print(f"{status} {result['file']} ({result['converter']})")
```

## 🖥️ Command Line Interface

### Installation

After installing the package, you can use the command-line interface:

```bash
# Install the specific version
pip install documents-to-markdown==1.0.0

# Or install latest version
pip install documents-to-markdown

# Now you can use the CLI commands
documents-to-markdown --help
doc2md --help  # Alternative shorter command
```

### Basic Commands

```bash
# Convert all files in current input folder
documents-to-markdown

# Convert all files with custom folders
documents-to-markdown --input docs --output markdown

# Convert a single file
documents-to-markdown --file document.docx output.md

# Show converter statistics
documents-to-markdown --stats

# Disable section numbering
documents-to-markdown --no-numbering

# Enable verbose output
documents-to-markdown --verbose
```

### Command Options

```bash
documents-to-markdown [OPTIONS]

Options:
  -i, --input FOLDER     Input folder (default: input)
  -o, --output FOLDER    Output folder (default: output)
  -f, --file INPUT OUTPUT Convert single file
  --no-numbering         Disable section numbering
  --stats               Show converter statistics
  -v, --verbose         Enable verbose logging
  --version             Show version
  --help                Show help message

Configuration Commands:
  --config show         Show current configuration
  --config init         Run interactive setup wizard
  --config set KEY VALUE Set configuration value
  --config test         Test AI service connectivity
  --config validate     Validate configuration
  --config location     Show config file locations
  --config reset        Reset to default settings
```

## ⚙️ Configuration & Settings

The package includes a comprehensive configuration system that makes setup easy and flexible.

### 🎯 First-Time Setup (Automatic)

When you first run the package, it automatically detects this is a new installation and offers to run a setup wizard:

```bash
# First time running any command triggers setup wizard
documents-to-markdown --help

# Or run setup explicitly anytime
documents-to-markdown --config init
```

The setup wizard will:
1. ✅ **Detect available AI services** (OLLAMA, OpenAI)
2. ✅ **Guide you through configuration** step-by-step
3. ✅ **Test your settings** to ensure they work
4. ✅ **Create all necessary files** automatically

### 🔧 Configuration Commands

```bash
# View current configuration
documents-to-markdown --config show

# Run interactive setup wizard
documents-to-markdown --config init

# Set specific values
documents-to-markdown --config set ai_service openai
documents-to-markdown --config set openai.api_key your_key_here
documents-to-markdown --config set file_paths.input_folder my_docs
documents-to-markdown --config set file_paths.output_folder my_output

# Test AI service connectivity
documents-to-markdown --config test

# Validate configuration
documents-to-markdown --config validate

# Show configuration file locations
documents-to-markdown --config location

# Reset to defaults
documents-to-markdown --config reset
```

### 📁 Configuration Files

The package automatically creates configuration files in the appropriate location for your OS:

**Windows:** `%APPDATA%\documents-to-markdown\`
**macOS:** `~/Library/Application Support/documents-to-markdown/`
**Linux:** `~/.config/documents-to-markdown/`

Files created:
- `config.json` - Main configuration settings
- `.env` - Environment variables

### 🤖 AI Service Configuration

#### Option 1: OLLAMA (Local AI) - Privacy Focused

```bash
# Install OLLAMA (https://ollama.ai)
ollama serve
ollama pull llava:latest

# Configure via CLI
documents-to-markdown --config set ai_service ollama
documents-to-markdown --config set ollama.base_url http://localhost:11434
documents-to-markdown --config set ollama.model llava:latest
```

**Benefits:**
- ✅ **Free**: No API costs
- ✅ **Private**: Data never leaves your computer
- ✅ **Offline**: Works without internet

#### Option 2: OpenAI (Cloud AI) - Easy Setup

```bash
# Get API key from https://platform.openai.com/api-keys
documents-to-markdown --config set ai_service openai
documents-to-markdown --config set openai.api_key your_key_here

# Or set via environment variable
export OPENAI_API_KEY=your_key_here  # Linux/macOS
set OPENAI_API_KEY=your_key_here     # Windows
```

**Benefits:**
- ✅ **Easy Setup**: Just need API key
- ✅ **High Quality**: Consistently good results
- ❌ **Costs Money**: Pay per API call

#### Option 3: Auto-Detection (Recommended)

```bash
# Let the system choose the best available service
documents-to-markdown --config set ai_service ""

# Configure both services as backup
documents-to-markdown --config set ollama.base_url http://localhost:11434
documents-to-markdown --config set openai.api_key your_key_here
```

The system will try OLLAMA first (private), then fallback to OpenAI if needed.

### ⚙️ Advanced Configuration

#### Complete Configuration Example

```json
{
  "ai_service": "",
  "add_section_numbers": true,
  "verbose_logging": false,
  "file_paths": {
    "input_folder": "input",
    "output_folder": "output"
  },
  "openai": {
    "api_key": "sk-your-key-here",
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
    "file_logging": false
  }
}
```

#### Setting Values via CLI

```bash
# General settings
documents-to-markdown --config set add_section_numbers true
documents-to-markdown --config set verbose_logging false

# File paths
documents-to-markdown --config set file_paths.input_folder my_documents
documents-to-markdown --config set file_paths.output_folder my_markdown

# OpenAI settings
documents-to-markdown --config set openai.model gpt-4o
documents-to-markdown --config set openai.max_tokens 4096
documents-to-markdown --config set openai.temperature 0.1

# OLLAMA settings
documents-to-markdown --config set ollama.model llava:latest
documents-to-markdown --config set ollama.timeout 120

# Image processing
documents-to-markdown --config set image_processing.max_size_mb 20
documents-to-markdown --config set image_processing.quality_compression 85

# Logging
documents-to-markdown --config set logging.level DEBUG
```

#### Environment Variables

You can also use environment variables (they override config file settings):

```bash
# AI Service
export AI_SERVICE=openai

# OpenAI
export OPENAI_API_KEY=your_key_here
export OPENAI_MODEL=gpt-4o
export OPENAI_MAX_TOKENS=4096

# OLLAMA
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=llava:latest
export OLLAMA_TIMEOUT=120

# Image Processing
export IMAGE_MAX_SIZE_MB=20
export IMAGE_QUALITY_COMPRESSION=85

# File Paths
export INPUT_FOLDER=my_documents
export OUTPUT_FOLDER=my_markdown

# Logging
export LOG_LEVEL=INFO
```

### 🔍 Testing & Validation

```bash
# Test AI service connectivity
documents-to-markdown --config test

# Example output:
# 🔍 Testing AI service connectivity...
#
# 🤖 AI Service Status:
# ✅ OLLAMA: Available
#    Model: llava:latest
# ❌ OpenAI: Not available
#    Error: No API key configured
#
# 💡 Recommendations:
#   • OLLAMA is available - great for privacy!
#   • Consider setting up OpenAI as backup

# Validate configuration
documents-to-markdown --config validate

# View current settings
documents-to-markdown --config show
```

## 📖 Examples

### Converting Different File Types

```python
from documents_to_markdown import DocumentConverter

converter = DocumentConverter()

# Word document
converter.convert_file("report.docx", "report.md")

# PDF document
converter.convert_file("manual.pdf", "manual.md")

# Excel spreadsheet
converter.convert_file("data.xlsx", "data.md")

# Image with text (requires AI setup)
converter.convert_file("screenshot.png", "screenshot.md")

# Plain text/CSV
converter.convert_file("data.csv", "data.md")
```

### Batch Processing

```python
from documents_to_markdown import convert_folder

# Convert entire folder
results = convert_folder("documents", "markdown_output")

print(f"✅ Converted: {results['successful_conversions']}")
print(f"❌ Failed: {results['failed_conversions']}")

# Process results
for result in results['results']:
    if result['status'] == 'success':
        print(f"✓ {result['file']} -> Converted with {result['converter']}")
    else:
        print(f"✗ {result['file']} -> Failed")
```

### Custom Configuration

```python
from documents_to_markdown import DocumentConverter

# Initialize with custom settings (overrides config file)
converter = DocumentConverter(
    add_section_numbers=False,  # Disable numbering
    verbose=True               # Enable debug logging
)

# Check what formats are supported
formats = converter.get_supported_formats()
print(f"Supported formats: {', '.join(formats)}")

# Get detailed converter information
stats = converter.get_conversion_statistics()
for conv_info in stats['converters']:
    name = conv_info['name']
    exts = ', '.join(conv_info['supported_extensions'])
    print(f"{name}: {exts}")
```

### Programmatic Configuration Access

```python
from documents_to_markdown import get_config, save_config, get_config_directory

# Get current configuration
config = get_config()
print(f"AI Service: {config.get('ai_service', 'auto-detect')}")
print(f"Section Numbers: {config.get('add_section_numbers', True)}")

# Modify configuration programmatically
config['ai_service'] = 'openai'
config['openai']['api_key'] = 'your-new-key'
config['add_section_numbers'] = False

# Save changes
success = save_config(config)
if success:
    print("Configuration updated successfully!")

# Get config directory path
config_dir = get_config_directory()
print(f"Config directory: {config_dir}")

# Use updated configuration
converter = DocumentConverter()  # Will use new settings
```

### Configuration-Aware Usage

```python
from documents_to_markdown import DocumentConverter, get_config

# Check configuration before processing
config = get_config()
ai_service = config.get('ai_service', '')

if ai_service == 'none':
    print("AI features disabled - image processing will be skipped")
elif not ai_service:
    print("Auto-detection enabled - will try OLLAMA first, then OpenAI")
else:
    print(f"Using {ai_service} for AI processing")

# Initialize converter (uses configuration automatically)
converter = DocumentConverter()

# Convert with current settings
success = converter.convert_file("document.docx", "output.md")
```

## 🏗️ Architecture

### Library Structure

```
documents_to_markdown/
├── __init__.py              # Main package exports
├── api.py                   # Public API interface
├── cli.py                   # Command-line interface
└── services/                # Core conversion services
    ├── document_converter_manager.py  # Main orchestrator
    ├── base_converter.py             # Abstract base converter
    ├── word_converter.py             # Word document converter
    ├── pdf_converter.py              # PDF document converter
    ├── excel_converter.py            # Excel spreadsheet converter
    ├── image_converter.py            # Image converter (AI-powered)
    ├── plain_text_converter.py       # Text/CSV converter (AI-enhanced)
    ├── text_chunking_utils.py        # Text processing utilities
    └── ai_services/                  # AI service abstraction
        ├── base_ai_service.py        # AI service interface
        ├── openai_service.py         # OpenAI implementation
        ├── ollama_service.py         # OLLAMA implementation
        └── ai_service_factory.py     # Service factory
```

### Converter Architecture

- **DocumentConverter**: Main public API class
- **DocumentConverterManager**: Orchestrates multiple converters
- **BaseDocumentConverter**: Abstract base for all converters
- **Specialized Converters**: Word, PDF, Excel, Image, PlainText
- **AI Services**: Pluggable AI backends (OpenAI, OLLAMA)

### Extensibility

The modular design makes it easy to:
- Add new document formats
- Integrate additional AI services
- Customize conversion behavior
- Extend processing capabilities

```python
# Example: Custom converter
from documents_to_markdown.services.base_converter import BaseDocumentConverter

class MyCustomConverter(BaseDocumentConverter):
    def get_supported_extensions(self):
        return ['.custom']

    def can_convert(self, file_path):
        return file_path.suffix.lower() == '.custom'

    def _convert_document_to_markdown(self, doc_path):
        # Your conversion logic here
        return "# Converted Content\n\nCustom format converted!"

# Add to converter manager
from documents_to_markdown import DocumentConverter
converter = DocumentConverter()
converter._get_manager().add_converter(MyCustomConverter())
```

## 🧪 Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/ChaosAIs/DocumentsToMarkdown.git
cd DocumentsToMarkdown

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run specific tests
python test_converter.py
python test_ai_services.py
```

### Running Tests

```bash
# Test basic conversion
python test_converter.py

# Test AI services
python test_ai_services.py

# Test image conversion
python test_image_converter.py

# Test flowchart conversion
python test_flowchart_conversion.py
```

### Building and Publishing

```bash
# Build the package
python -m build

# Install locally for testing
pip install dist/documents_to_markdown-1.0.0-py3-none-any.whl

# Publish to PyPI (maintainers only)
python -m twine upload dist/*
```

## 📋 Output Examples

### Word Document Conversion
Input Word document with formatting:
```markdown
# 1. Project Report

Some **bold text** and *italic text*

## 1.1 Data Summary

| Header 1 | Header 2 | Header 3 |
| --- | --- | --- |
| Data 1 | Data 2 | Data 3 |
| Data 4 | Data 5 | Data 6 |
```

### CSV to Markdown Table
Input CSV:
```csv
Employee ID,Name,Department,Salary
001,Alice Johnson,Engineering,75000
002,Bob Smith,Marketing,65000
```

Output:
```markdown
| Employee ID | Name         | Department  | Salary |
|:-----------:|:-------------|:------------|-------:|
| 001         | Alice Johnson| Engineering |  75000 |
| 002         | Bob Smith    | Marketing   |  65000 |
```

### AI-Enhanced Image Processing
Images containing flowcharts are automatically converted to ASCII diagrams:
```markdown
┌─────────────┐
│    Start    │
└──────┬──────┘
       ↓
┌─────────────┐
│  Process A  │
└──────┬──────┘
       ↓
┌─────────────┐
│     End     │
└─────────────┘
```

## 🎯 Demo Files & Live Examples

We've included a comprehensive set of demo files to showcase the converter's capabilities across different document types. You can find these in the [`demo_files`](demo_files/) folder along with their converted outputs in [`demo_files/output`](demo_files/output/).

### 📁 Available Demo Files

| Input File | Type | Description | Output |
|------------|------|-------------|---------|
| [`employees.csv`](demo_files/employees.csv) | CSV | Employee data with headers | [`employees.md`](demo_files/output/employees.md) |
| [`inventory.tsv`](demo_files/inventory.tsv) | TSV | Tab-separated inventory data | [`inventory.md`](demo_files/output/inventory.md) |
| [`project_report.txt`](demo_files/project_report.txt) | Plain Text | Project status report | [`project_report.md`](demo_files/output/project_report.md) |
| [`system.log`](demo_files/system.log) | Log File | System log entries | [`system.md`](demo_files/output/system.md) |
| [`file_example_XLS_50.xls`](demo_files/file_example_XLS_50.xls) | Excel | Sample spreadsheet data | [`file_example_XLS_50.md`](demo_files/output/file_example_XLS_50.md) |
| [`file-sample_500kB.doc`](demo_files/file-sample_500kB.doc) | Word Doc | Legacy Word document | [`file-sample_500kB.md`](demo_files/output/file-sample_500kB.md) |
| [`file-example_PDF_500_kB.pdf`](demo_files/file-example_PDF_500_kB.pdf) | PDF | Sample PDF with images | [`file-example_PDF_500_kB.md`](demo_files/output/file-example_PDF_500_kB.md) |
| [`NET-Microservices-Architecture-for-Containerized-NET-Applications.pdf`](demo_files/NET-Microservices-Architecture-for-Containerized-NET-Applications.pdf) | PDF | Technical documentation (338 pages) | [`NET-Microservices-Architecture-for-Containerized-NET-Applications.md`](demo_files/output/NET-Microservices-Architecture-for-Containerized-NET-Applications.md) |
| [`FlowChartSample.png`](demo_files/FlowChartSample.png) | Image | Flowchart diagram | [`FlowChartSample.md`](demo_files/output/FlowChartSample.md) |
| [`employees_direct.md`](demo_files/employees_direct.md) | Markdown | Existing markdown file | [`employees_direct.md`](demo_files/output/employees_direct.md) |

### 🚀 Try the Demo

You can run the demo conversion yourself:

```bash
# Clone the repository
git clone https://github.com/ChaosAIs/DocumentsToMarkdown.git
cd DocumentsToMarkdown

# Install the package
pip install -e .

# Convert all demo files
python document_converter.py --input demo_files --output demo_files/output --verbose

# Or use the CLI
documents-to-markdown --input demo_files --output demo_files/output
```

### 📊 Demo Results Summary

The demo showcases successful conversion of **10 different file types**:
- ✅ **CSV/TSV files** → Properly formatted markdown tables
- ✅ **Plain text files** → AI-enhanced markdown with structure
- ✅ **Excel spreadsheets** → Data tables with preserved formatting
- ✅ **Word documents** → Structured markdown with headings
- ✅ **PDF documents** → Text extraction with embedded image processing
- ✅ **Large technical PDFs** → Complete conversion with 137+ images processed
- ✅ **Images with flowcharts** → ASCII diagram conversion
- ✅ **Log files** → Formatted markdown with syntax highlighting

### 🎨 Conversion Features Demonstrated

**AI-Powered Image Processing:**
- Extracted text from 142+ images across PDF documents
- Converted flowchart images to ASCII diagrams
- Processed embedded images within documents

**Smart Text Processing:**
- Enhanced CSV/TSV formatting with proper table alignment
- Intelligent text structure recognition
- Preserved data relationships and formatting

**Document Structure Preservation:**
- Maintained hierarchical heading structure
- Preserved table formatting and data alignment
- Kept original document flow and organization

**Batch Processing Efficiency:**
- Processed 10 diverse files in a single operation
- Handled large documents (338-page PDF) successfully
- Maintained consistent output quality across all formats

## 🔧 Troubleshooting

### Configuration Issues

**Check Configuration Status:**
```bash
# View current configuration
documents-to-markdown --config show

# Test AI services
documents-to-markdown --config test

# Validate configuration
documents-to-markdown --config validate

# Show config file locations
documents-to-markdown --config location
```

**Reset Configuration:**
```bash
# Reset to defaults if configuration is corrupted
documents-to-markdown --config reset

# Re-run setup wizard
documents-to-markdown --config init
```

### AI Service Issues

**OLLAMA Problems:**
```bash
# Check if OLLAMA is running
curl http://localhost:11434/api/version

# Start OLLAMA if not running
ollama serve

# Install vision model if missing
ollama pull llava:latest

# Test OLLAMA connectivity
documents-to-markdown --config test
```

**OpenAI Problems:**
```bash
# Check API key
echo $OPENAI_API_KEY

# Set API key via configuration
documents-to-markdown --config set openai.api_key your_key_here

# Or set via environment variable
export OPENAI_API_KEY=your_key_here

# Test OpenAI connectivity
documents-to-markdown --config test
```

**Auto-Detection Issues:**
```bash
# Check which services are available
documents-to-markdown --config test

# Force specific service if auto-detection fails
documents-to-markdown --config set ai_service ollama
# or
documents-to-markdown --config set ai_service openai
```

### Installation Problems

**Missing Dependencies:**
```bash
# Reinstall specific version
pip install --upgrade documents-to-markdown==1.0.0

# Or reinstall latest version
pip install --upgrade documents-to-markdown

# Development installation
git clone https://github.com/ChaosAIs/DocumentsToMarkdown.git
cd DocumentsToMarkdown
pip install -e .
```

**Permission Issues:**
```bash
# Check config directory permissions
documents-to-markdown --config location

# On Linux/macOS, ensure user has write access to config directory
chmod 755 ~/.config/documents-to-markdown/
```

### File Processing Issues

**Conversion Failures:**
```bash
# Enable verbose logging for debugging
documents-to-markdown --config set verbose_logging true

# Or use verbose flag
documents-to-markdown --verbose --file document.docx output.md

# Check supported formats
documents-to-markdown --stats
```

**Common File Issues:**
- Ensure files are in supported formats (.docx, .pdf, .xlsx, .png, .txt, .csv)
- Check file permissions and paths
- Verify files are not corrupted or password-protected
- For large files, ensure sufficient disk space

### Configuration Priority

Settings are applied in this order (highest to lowest priority):
1. **Command line arguments** (e.g., `--verbose`)
2. **Environment variables** (e.g., `OPENAI_API_KEY`)
3. **Configuration file** (`config.json`)
4. **Default values**

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Run tests**: `pytest` or `python test_converter.py`
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure backward compatibility

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **python-docx** for Word document processing
- **PyMuPDF** for PDF handling
- **OpenAI** for AI vision capabilities
- **OLLAMA** for local AI processing
- **openpyxl** for Excel support

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ChaosAIs/DocumentsToMarkdown/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ChaosAIs/DocumentsToMarkdown/discussions)
- **Documentation**: [Project Wiki](https://github.com/ChaosAIs/DocumentsToMarkdown/wiki)

---

**Made with ❤️ by [Felix](https://github.com/ChaosAIs)**
