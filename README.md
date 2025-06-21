# Document to Markdown Converter

A powerful, modular Python application that converts various document types to Markdown format with AI-driven image extraction and processing.

## Supported Formats

- **Word Documents**: `.docx`, `.doc`
- **PDF Documents**: `.pdf`
- **Excel Spreadsheets**: `.xlsx`, `.xlsm`, `.xlsb`, `.xls`
- **Image Files**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.tif`, `.webp` (using AI vision)

## Features

### Core Features
- **Multi-format support**: Word, PDF, Excel, and Image documents
- **Multiple AI services**: Choose between OpenAI (cloud) and OLLAMA (local) for image processing
- **AI-powered image conversion**: Extract text from images using advanced AI vision capabilities
- **Embedded image extraction**: Automatically extracts and processes images within Word and PDF documents
- **Privacy-focused options**: Use local AI (OLLAMA) to keep your data completely private
- **Automatic section numbering**: Hierarchical numbering (1, 1.1, 1.2, etc.)
- **Modular architecture**: Pluggable converter system with AI service abstraction
- **Batch processing**: Convert multiple documents at once
- **Preserves formatting**: Bold, italic, tables, and document structure

### Document Structure Preservation
- Headings (H1-H6) with automatic numbering
- Bold and italic text formatting
- Tables with proper Markdown formatting
- Paragraphs and line breaks
- Font-based heading detection (PDF)

### AI-Powered Image Processing
- **Multiple AI service options**: Choose between cloud (OpenAI) and local (OLLAMA) AI services
- **Privacy protection**: Use OLLAMA for completely local processing - your images never leave your computer
- **Smart content detection**: Automatically identifies flowcharts, tables, and text content
- **Flowchart to ASCII conversion**: Converts flowcharts and process diagrams to ASCII flow diagrams
- **Inline image processing**: Extracts and processes embedded images within documents at their original locations
- **Multiple image formats**: Supports PNG, JPG, JPEG, GIF, BMP, TIFF, SVG
- **Intelligent formatting**: Preserves document structure and applies appropriate Markdown formatting
- **Content filtering**: Skips unclear or failed extractions to maintain clean output
- **Auto-detection**: Automatically selects the best available AI service

### Advanced Features
- **Smart heading detection**: Uses document styles and content analysis
- **Table detection**: Automatically converts tabular data
- **Error handling**: Graceful handling of corrupted files
- **Detailed logging**: Comprehensive conversion reports
- **Configurable AI settings**: Customize image processing and AI model parameters

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. **Setup AI Services (for image conversion and embedded image extraction)**:

   You have two options for AI-powered image processing:

   ### Option A: OLLAMA (Local AI) - **Recommended for Privacy**
   - ✅ **Free**: No API costs after setup
   - ✅ **Private**: Images never leave your computer
   - ✅ **Offline**: Works without internet connection
   - ⚠️ **Setup Required**: Needs local installation

   **Quick Setup:**
   ```bash
   # Install OLLAMA (see https://ollama.ai)
   ollama serve
   ollama pull llava:latest
   ```

   **Configuration** (copy `.env.template` to `.env`):
   ```bash
   AI_SERVICE=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llava:latest
   ```

   ### Option B: OpenAI (Cloud AI) - **Recommended for Ease of Use**
   - ✅ **Easy Setup**: Just need API key
   - ✅ **High Quality**: Consistently good results
   - ❌ **Costs Money**: Pay per API call
   - ❌ **Privacy**: Images sent to OpenAI

   **Quick Setup:**
   - Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Copy `.env.template` to `.env` and add:
   ```bash
   AI_SERVICE=openai
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   ### Auto-Detection (Recommended)
   Configure both services and let the system choose the best available one:
   ```bash
   # Leave AI_SERVICE empty for auto-detection
   # System will try OLLAMA first, then fall back to OpenAI
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llava:latest
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Optional Advanced Configuration** (in `.env` file):
   ```bash
   # AI Service Selection (optional - auto-detection if not set)
   AI_SERVICE=ollama|openai

   # OpenAI Configuration
   OPENAI_MODEL=gpt-4o
   OPENAI_MAX_TOKENS=4096
   OPENAI_TEMPERATURE=0.1
   OPENAI_BASE_URL=https://api.openai.com/v1  # Optional: for OpenAI-compatible APIs

   # OLLAMA Configuration
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llava:latest
   OLLAMA_TIMEOUT=120
   OLLAMA_TEMPERATURE=0.1

   # Image Processing Settings
   IMAGE_MAX_SIZE_MB=20
   IMAGE_QUALITY_COMPRESSION=85
   IMAGE_MAX_SIZE_PIXELS=2048

   # Logging Level
   LOG_LEVEL=INFO
   ```

### Dependencies
- `python-docx==1.2.0`: For Word document processing
- `PyMuPDF==1.24.14`: For PDF document processing and image extraction
- `openpyxl==3.1.2`: For Excel document processing (.xlsx, .xlsm, .xlsb)
- `xlrd==2.0.1`: For legacy Excel document processing (.xls)
- `python-dotenv==1.0.0`: For environment variable management
- `openai==1.51.0`: For OpenAI AI-powered image text extraction
- `Pillow==10.4.0`: For image processing and optimization
- `requests==2.32.3`: For HTTP requests to AI services (OpenAI and OLLAMA)

## Usage

### Quick Start

1. **Setup folders**: The application will automatically create `input` and `output` folders if they don't exist.

2. **Add documents**: Place your documents (Word, PDF, Excel, or Image files) in the `input` folder.

3. **Run the converter**:

```bash
# Convert all documents
python document_converter.py

# Use custom input/output folders
python document_converter.py --input docs --output markdown

# Show converter statistics
python document_converter.py --stats
```

4. **Check results**: Converted Markdown files will be saved in the `output` folder.

### Legacy Version
The original Word-only converter is still available:
```bash
python document_converter.py
```

## Project Structure

```
DocumentsToMarkdown/
├── document_converter_v2.py      # New modular application (recommended)
├── document_converter.py         # Legacy Word-only converter
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── .env.template                 # Environment configuration template
├── .env                          # Your environment configuration (create from template)
├── services/                     # Converter services (modular architecture)
│   ├── __init__.py
│   ├── base_converter.py         # Abstract base converter
│   ├── word_converter.py         # Word document converter with image extraction
│   ├── pdf_converter.py          # PDF document converter with image extraction
│   ├── excel_converter.py        # Excel document converter
│   ├── image_converter.py        # Image document converter (AI vision)
│   ├── document_converter_manager.py  # Main orchestrator
│   └── ai_services/              # AI service abstraction layer
│       ├── __init__.py
│       ├── base_ai_service.py    # Abstract AI service interface
│       ├── openai_service.py     # OpenAI implementation
│       ├── ollama_service.py     # OLLAMA implementation
│       └── ai_service_factory.py # AI service factory and management
├── test_flowchart_conversion.py  # Test script for flowchart conversion
├── test_image_converter.py       # Test script for image conversion
├── test_ai_services.py           # Test script for AI service implementations
├── IMAGE_INTEGRATION_FEATURE.md  # Documentation for image integration
├── IMAGE_CONVERSION_GUIDE.md     # Guide for image conversion features
├── OLLAMA_SETUP_GUIDE.md         # Complete OLLAMA setup guide
├── AI_SERVICES.md                # AI services documentation
├── input/                        # Place documents here
└── output/                       # Converted Markdown files appear here
```

## Architecture

The v2.0 converter uses a modular architecture:

- **BaseDocumentConverter**: Abstract base class defining the converter interface
- **WordDocumentConverter**: Handles Word document conversion with advanced formatting detection
- **PDFDocumentConverter**: Handles PDF conversion with font-based heading detection
- **ExcelDocumentConverter**: Handles Excel spreadsheet conversion with table formatting
- **ImageDocumentConverter**: Handles image conversion using pluggable AI vision services
- **DocumentConverterManager**: Orchestrates multiple converters and provides unified interface

### AI Service Architecture
- **BaseAIService**: Abstract interface for AI services
- **OpenAIService**: Cloud-based AI using OpenAI's GPT-4 Vision
- **OllamaService**: Local AI using OLLAMA with LLaVA models
- **AIServiceFactory**: Manages service creation and auto-detection

This modular design makes it easy to add new document formats and AI services.

## AI-Powered Features

### Multiple AI Service Options

Choose the AI service that best fits your needs:

#### 🏠 OLLAMA (Local AI)
- **Complete Privacy**: All processing happens on your machine
- **No API Costs**: Free after initial setup
- **Offline Capable**: Works without internet connection
- **Models**: LLaVA variants (7B, 13B, 34B parameters)
- **Setup**: Requires local installation and model download

#### ☁️ OpenAI (Cloud AI)
- **Easy Setup**: Just need an API key
- **High Performance**: Consistently fast and accurate
- **Latest Models**: Access to cutting-edge AI capabilities
- **Costs**: Pay-per-use pricing
- **Privacy**: Images are sent to OpenAI servers

#### 🔄 Auto-Detection
- **Smart Selection**: Automatically chooses the best available service
- **Fallback Support**: Uses OLLAMA if available, falls back to OpenAI
- **Zero Configuration**: Works out of the box with either service

### Intelligent Image Content Detection

The converter uses advanced AI vision capabilities to automatically detect and process different types of image content:

#### 🔄 Flowchart & Process Diagram Detection
- **Automatic recognition**: Identifies flowcharts, process diagrams, and workflows
- **ASCII conversion**: Converts visual flowcharts to text-based ASCII diagrams
- **Character set**: Uses Unicode box-drawing characters (┌─┐│└─┘) and directional arrows (→↓←↑)
- **Decision points**: Represents decision diamonds with ASCII art
- **Flow preservation**: Maintains logical flow direction and connections

#### 📊 Table & Form Recognition
- **Smart detection**: Identifies tabular data, forms, and structured content
- **Markdown formatting**: Converts to properly formatted Markdown tables
- **Data preservation**: Maintains all data relationships and structure

#### 📝 Text Content Extraction
- **OCR capabilities**: Extracts text from images, screenshots, and scanned documents
- **Structure preservation**: Maintains headings, paragraphs, and formatting
- **Multi-column support**: Handles complex layouts with proper reading order

### Embedded Image Processing

#### Word Documents (.docx)
- **ZIP extraction**: Accesses the `word/media/` directory within the document structure
- **Automatic detection**: Finds all embedded images regardless of format
- **Position mapping**: Places extracted content at original image locations

#### PDF Documents (.pdf)
- **Page-by-page extraction**: Uses PyMuPDF to extract images from each page
- **Format support**: Handles various embedded image formats
- **Inline integration**: Inserts extracted content at appropriate document positions

### Configuration Options

The AI features can be customized through environment variables:

```bash
# AI Service Selection
AI_SERVICE=ollama|openai                   # Choose specific service or leave empty for auto-detection

# OpenAI Configuration
OPENAI_API_KEY=your_key_here              # Required for OpenAI
OPENAI_MODEL=gpt-4o                       # AI model to use
OPENAI_MAX_TOKENS=4096                    # Maximum response length
OPENAI_TEMPERATURE=0.1                    # Response creativity (0.0-1.0)

# OLLAMA Configuration
OLLAMA_BASE_URL=http://localhost:11434    # OLLAMA server URL
OLLAMA_MODEL=llava:latest                 # Vision model to use
OLLAMA_TIMEOUT=120                        # Request timeout in seconds
OLLAMA_TEMPERATURE=0.1                    # Response creativity (0.0-1.0)

# Image Processing
IMAGE_MAX_SIZE_MB=20                      # Maximum image size for processing
IMAGE_QUALITY_COMPRESSION=85              # JPEG compression quality (1-100)
IMAGE_MAX_SIZE_PIXELS=2048                # Maximum image dimensions

# Logging
LOG_LEVEL=INFO                            # Logging detail level
```

## Supported Features

### Text Formatting
- **Bold text** → `**bold text**`
- *Italic text* → `*italic text*`

### Headings
- Heading 1 → `# Heading 1`
- Heading 2 → `## Heading 2`
- Heading 3 → `### Heading 3`
- And so on...

### Tables
Word tables are converted to Markdown table format with proper headers and alignment.

### Excel Spreadsheets
- **Multi-worksheet support**: Each worksheet becomes a separate section
- **Table formatting**: Spreadsheet data converted to Markdown tables
- **Data type preservation**: Numbers, text, dates, and formulas handled appropriately
- **Format compatibility**: Supports modern (.xlsx, .xlsm, .xlsb) and legacy (.xls) formats

### Image Documents & Embedded Image Processing (AI Vision)
- **Multiple AI service support**: Choose between OpenAI (cloud) and OLLAMA (local) for image processing
- **Privacy-focused processing**: Use OLLAMA to keep all image data on your local machine
- **AI-powered text extraction**: Extract text from standalone images and embedded images using advanced AI vision
- **Flowchart detection and ASCII conversion**: Automatically detects flowcharts and converts them to ASCII flow diagrams
- **Smart content recognition**: Distinguishes between flowcharts, tables, forms, and regular text content
- **Multiple image formats**: Supports JPG, PNG, GIF, BMP, TIFF, WebP, SVG
- **Embedded image extraction**: Automatically extracts images from Word (.docx) and PDF documents
- **Inline processing**: Places extracted image content at original image locations within document flow
- **Image optimization**: Automatic resizing and compression for optimal AI processing
- **Content filtering**: Skips unclear or failed extractions to maintain clean output
- **ASCII flow diagrams**: Converts flowcharts to text-based diagrams using characters like ┌─┐│└─┘ and arrows →↓←↑
- **Auto-detection**: Automatically selects the best available AI service

### Error Handling
- Graceful handling of corrupted or unsupported files
- Detailed error logging
- Continues processing other files if one fails

## Examples

### Basic Document Conversion
Input Word document with:
- Title: "My Document"
- Some **bold text** and *italic text*
- A table with data

Output Markdown:
```markdown
# My Document

Some **bold text** and *italic text*

| Header 1 | Header 2 | Header 3 |
| --- | --- | --- |
| Data 1 | Data 2 | Data 3 |
| Data 4 | Data 5 | Data 6 |
```

### AI-Powered Flowchart Conversion
Input: Image containing a flowchart

Output Markdown with ASCII flow diagram:
```markdown
<!-- Converted from image: flowchart.png -->
<!-- Conversion method: AI Vision (OLLAMA llava:latest) -->

┌─────────────┐
│    Start    │
└──────┬──────┘
       ↓
┌─────────────┐
│  Process A  │
└──────┬──────┘
       ↓
    /\     /\
   /  \   /  \
  /    \ /    \
 / Decision?  \
 \            /
  \          /
   \        /
    \      /
     \    /
      \  /
       \/
   Yes ↓  No →
┌─────────────┐    ┌─────────────┐
│  Process B  │    │  Process C  │
└──────┬──────┘    └──────┬──────┘
       ↓                  ↓
┌─────────────┐    ┌─────────────┐
│     End     │    │     End     │
└─────────────┘    └─────────────┘
```

### Document with Embedded Images
Input: Word document containing embedded flowchart images

Output: Markdown with extracted image content placed inline at original locations, preserving document flow and structure.

## Testing AI Features

### Test AI Services
Run the comprehensive AI services test to verify your setup:

```bash
python test_ai_services.py
```

This script will:
- Check which AI services are available (OLLAMA and/or OpenAI)
- Test service creation and configuration
- Verify image conversion capabilities
- Run actual conversion tests with sample images
- Provide setup guidance for any missing services

### Test Flowchart Conversion
Run the included test script to verify flowchart detection and ASCII conversion:

```bash
python test_flowchart_conversion.py
```

This script will:
- Test the flowchart detection capabilities
- Show example ASCII flow diagram output
- Verify the enhanced image processing features

### Test Image Conversion
Test standalone image conversion capabilities:

```bash
python test_image_converter.py
```

### Manual Testing
1. **Flowchart images**: Add flowchart images to the `input` folder and run the converter
2. **Documents with embedded images**: Use Word or PDF documents containing images
3. **Mixed content**: Test documents with various image types (flowcharts, tables, text screenshots)

## Troubleshooting

### Common Issues

1. **"python-docx is not installed" error**:
   ```bash
   pip install -r requirements.txt
   ```

2. **No documents found**:
   - Make sure your documents are in the `input` folder
   - Supported formats: Word (.docx, .doc), PDF (.pdf), Excel (.xlsx, .xlsm, .xlsb, .xls), Images (.jpg, .png, etc.)

3. **Permission errors**:
   - Make sure you have write permissions in the output folder
   - Close any documents that might be open

4. **AI Service errors**:

   **OLLAMA Issues:**
   - **"Cannot connect to OLLAMA server"**: Make sure OLLAMA is running (`ollama serve`)
   - **"Model not found"**: Install the vision model (`ollama pull llava:latest`)
   - **Slow performance**: Use a smaller model (`ollama pull llava:7b`)
   - **Out of memory**: Close other applications or use a smaller model

   **OpenAI Issues:**
   - Verify your API key is correctly set in the `.env` file
   - Check your OpenAI account has sufficient credits
   - Ensure you have access to GPT-4 Vision model

5. **Image processing issues**:
   - Large images are automatically resized for optimal AI processing
   - Supported formats: JPG, PNG, GIF, BMP, TIFF, WebP, SVG
   - Check the logs for specific error messages
   - Run `python test_ai_services.py` to diagnose AI service issues

6. **Embedded image extraction not working**:
   - Ensure at least one AI service is configured (OLLAMA or OpenAI)
   - Check that the document actually contains embedded images
   - Review the conversion logs for detailed information
   - Verify AI service availability with the test script

### Performance Tips

- **Choose the right AI service**:
  - **OLLAMA**: Slower but private and free. Good for sensitive documents
  - **OpenAI**: Faster and more accurate. Good for production use
- **Large documents**: Processing documents with many embedded images may take longer due to AI processing
- **OLLAMA optimization**: Use smaller models (llava:7b) for faster processing if quality is acceptable
- **OpenAI limits**: Be aware of API rate limits when processing many images
- **Image quality**: Higher quality images generally produce better text extraction results
- **Hardware**: OLLAMA performance depends on your CPU/GPU and available RAM

## Requirements

- Python 3.7+
- **For AI-powered image processing**, choose one or both:
  - **OLLAMA**: Local AI server with vision models (free, private)
  - **OpenAI API key**: Cloud AI service (paid, high quality)
- All dependencies listed in requirements.txt

## Quick Start Guides

- **[OLLAMA Setup Guide](OLLAMA_SETUP_GUIDE.md)**: Complete guide for setting up local AI
- **[Image Conversion Guide](IMAGE_CONVERSION_GUIDE.md)**: Comprehensive image processing documentation
- **[AI Services Documentation](AI_SERVICES.md)**: Technical details about the AI service architecture

## License

This project is open source and available under the MIT License.
