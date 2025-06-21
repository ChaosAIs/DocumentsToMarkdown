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
- **AI-powered image conversion**: Extract text from images using OpenAI GPT-4 Vision
- **Embedded image extraction**: Automatically extracts and processes images within Word and PDF documents
- **Automatic section numbering**: Hierarchical numbering (1, 1.1, 1.2, etc.)
- **Modular architecture**: Pluggable converter system
- **Batch processing**: Convert multiple documents at once
- **Preserves formatting**: Bold, italic, tables, and document structure

### Document Structure Preservation
- Headings (H1-H6) with automatic numbering
- Bold and italic text formatting
- Tables with proper Markdown formatting
- Paragraphs and line breaks
- Font-based heading detection (PDF)

### AI-Powered Image Processing
- **Smart content detection**: Automatically identifies flowcharts, tables, and text content
- **Flowchart to ASCII conversion**: Converts flowcharts and process diagrams to ASCII flow diagrams
- **Inline image processing**: Extracts and processes embedded images within documents at their original locations
- **Multiple image formats**: Supports PNG, JPG, JPEG, GIF, BMP, TIFF, SVG
- **Intelligent formatting**: Preserves document structure and applies appropriate Markdown formatting
- **Content filtering**: Skips unclear or failed extractions to maintain clean output

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

3. **Setup AI Vision (for image conversion and embedded image extraction)**:
   - Copy `.env.template` to `.env`
   - Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Add your API key to the `.env` file:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Optional Configuration** (in `.env` file):
   ```bash
   # AI Model Configuration
   OPENAI_MODEL=gpt-4-vision-preview
   OPENAI_MAX_TOKENS=4096
   OPENAI_TEMPERATURE=0.1

   # Image Processing Settings
   IMAGE_MAX_SIZE_MB=20
   IMAGE_QUALITY_COMPRESSION=85

   # Logging Level
   LOG_LEVEL=INFO
   ```

### Dependencies
- `python-docx==1.2.0`: For Word document processing
- `PyMuPDF==1.24.14`: For PDF document processing and image extraction
- `openpyxl==3.1.2`: For Excel document processing (.xlsx, .xlsm, .xlsb)
- `xlrd==2.0.1`: For legacy Excel document processing (.xls)
- `python-dotenv==1.0.0`: For environment variable management
- `openai==1.51.0`: For AI-powered image text extraction
- `Pillow==10.4.0`: For image processing and optimization
- `requests==2.32.3`: For HTTP requests to AI services

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
│   └── document_converter_manager.py  # Main orchestrator
├── test_flowchart_conversion.py  # Test script for flowchart conversion
├── test_image_converter.py       # Test script for image conversion
├── IMAGE_INTEGRATION_FEATURE.md  # Documentation for image integration
├── IMAGE_CONVERSION_GUIDE.md     # Guide for image conversion features
├── input/                        # Place documents here
└── output/                       # Converted Markdown files appear here
```

## Architecture

The v2.0 converter uses a modular architecture:

- **BaseDocumentConverter**: Abstract base class defining the converter interface
- **WordDocumentConverter**: Handles Word document conversion with advanced formatting detection
- **PDFDocumentConverter**: Handles PDF conversion with font-based heading detection
- **ExcelDocumentConverter**: Handles Excel spreadsheet conversion with table formatting
- **ImageDocumentConverter**: Handles image conversion using AI vision capabilities
- **DocumentConverterManager**: Orchestrates multiple converters and provides unified interface

This design makes it easy to add new document formats by creating new converter classes.

## AI-Powered Features

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
# AI Model Selection
OPENAI_MODEL=gpt-4-vision-preview          # AI model to use
OPENAI_MAX_TOKENS=4096                     # Maximum response length
OPENAI_TEMPERATURE=0.1                     # Response creativity (0.0-1.0)

# Image Processing
IMAGE_MAX_SIZE_MB=20                       # Maximum image size for processing
IMAGE_QUALITY_COMPRESSION=85               # JPEG compression quality (1-100)

# Logging
LOG_LEVEL=INFO                             # Logging detail level
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
- **AI-powered text extraction**: Uses OpenAI GPT-4 Vision to extract text from standalone images and embedded images
- **Flowchart detection and ASCII conversion**: Automatically detects flowcharts and converts them to ASCII flow diagrams
- **Smart content recognition**: Distinguishes between flowcharts, tables, forms, and regular text content
- **Multiple image formats**: Supports JPG, PNG, GIF, BMP, TIFF, WebP, SVG
- **Embedded image extraction**: Automatically extracts images from Word (.docx) and PDF documents
- **Inline processing**: Places extracted image content at original image locations within document flow
- **Image optimization**: Automatic resizing and compression for API efficiency
- **Content filtering**: Skips unclear or failed extractions to maintain clean output
- **ASCII flow diagrams**: Converts flowcharts to text-based diagrams using characters like ┌─┐│└─┘ and arrows →↓←↑

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
<!-- Conversion method: AI Vision (OpenAI gpt-4-vision-preview) -->

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

4. **OpenAI API errors**:
   - Verify your API key is correctly set in the `.env` file
   - Check your OpenAI account has sufficient credits
   - Ensure you have access to GPT-4 Vision model

5. **Image processing issues**:
   - Large images are automatically resized for API efficiency
   - Supported formats: JPG, PNG, GIF, BMP, TIFF, WebP, SVG
   - Check the logs for specific error messages

6. **Embedded image extraction not working**:
   - Ensure OpenAI API key is configured
   - Check that the document actually contains embedded images
   - Review the conversion logs for detailed information

### Performance Tips

- **Large documents**: Processing documents with many embedded images may take longer due to AI processing
- **API limits**: Be aware of OpenAI API rate limits when processing many images
- **Image quality**: Higher quality images generally produce better text extraction results

## Requirements

- Python 3.7+
- OpenAI API key (for image processing features)
- All dependencies listed in requirements.txt

## License

This project is open source and available under the MIT License.
