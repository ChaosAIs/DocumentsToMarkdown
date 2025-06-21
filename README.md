# Document to Markdown Converter v2.0

A modular Python application that converts various document types to Markdown format with automatic section numbering.

## Supported Formats

- **Word Documents**: `.docx`, `.doc`
- **PDF Documents**: `.pdf`
- **Excel Spreadsheets**: `.xlsx`, `.xlsm`, `.xlsb`, `.xls`
- **Image Files**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.tif`, `.webp` (using AI vision)

## Features

### Core Features
- **Multi-format support**: Word, PDF, Excel, and Image documents
- **AI-powered image conversion**: Extract text from images using OpenAI GPT-4 Vision
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

### Advanced Features
- **Smart heading detection**: Uses document styles and content analysis
- **Table detection**: Automatically converts tabular data
- **Error handling**: Graceful handling of corrupted files
- **Detailed logging**: Comprehensive conversion reports
- **Configurable options**: Enable/disable section numbering

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. **Setup AI Vision (for image conversion)**:
   - Copy `.env.template` to `.env`
   - Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Add your API key to the `.env` file:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Dependencies
- `python-docx`: For Word document processing
- `PyMuPDF`: For PDF document processing and text extraction
- `openpyxl`: For Excel document processing (.xlsx, .xlsm, .xlsb)
- `xlrd`: For legacy Excel document processing (.xls)
- `python-dotenv`: For environment variable management
- `openai`: For AI-powered image text extraction
- `Pillow`: For image processing and optimization
- `requests`: For HTTP requests to AI services

## Usage

### Quick Start

1. **Setup folders**: The application will automatically create `input` and `output` folders if they don't exist.

2. **Add documents**: Place your documents (Word, PDF, Excel, or Image files) in the `input` folder.

3. **Run the converter**:

```bash
# Convert all documents with section numbering (recommended)
python document_converter_v2.py

# Convert without section numbering
python document_converter_v2.py --no-numbering

# Use custom input/output folders
python document_converter_v2.py --input docs --output markdown

# Show converter statistics
python document_converter_v2.py --stats
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
├── services/                     # Converter services (modular architecture)
│   ├── __init__.py
│   ├── base_converter.py         # Abstract base converter
│   ├── word_converter.py         # Word document converter
│   ├── pdf_converter.py          # PDF document converter
│   ├── excel_converter.py        # Excel document converter
│   ├── image_converter.py        # Image document converter (AI vision)
│   └── document_converter_manager.py  # Main orchestrator
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

### Image Documents (AI Vision)
- **AI-powered text extraction**: Uses OpenAI GPT-4 Vision to extract text from images
- **Multiple image formats**: Supports JPG, PNG, GIF, BMP, TIFF, WebP
- **Smart formatting**: Preserves document structure, headings, and tables
- **Image optimization**: Automatic resizing and compression for API efficiency
- **Intelligent content analysis**: Describes charts, diagrams, and visual elements

### Error Handling
- Graceful handling of corrupted or unsupported files
- Detailed error logging
- Continues processing other files if one fails

## Example

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

## Troubleshooting

### Common Issues

1. **"python-docx is not installed" error**:
   ```bash
   pip install python-docx
   ```

2. **No documents found**:
   - Make sure your Word documents are in the `input` folder
   - Only `.docx` files are supported (not `.doc`)

3. **Permission errors**:
   - Make sure you have write permissions in the output folder
   - Close any Word documents that might be open

## Requirements

- Python 3.6+
- python-docx library

## License

This project is open source and available under the MIT License.
