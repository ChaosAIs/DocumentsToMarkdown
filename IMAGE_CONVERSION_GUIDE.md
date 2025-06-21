# Image to Markdown Conversion Guide

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure OpenAI API**:
   - Copy `.env.template` to `.env`
   - Get your OpenAI API key from: https://platform.openai.com/api-keys
   - Add your API key to `.env`:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```

3. **Add Image Files**:
   - Place your image files in the `input` folder
   - Supported formats: JPG, PNG, GIF, BMP, TIFF, WebP

4. **Run Conversion**:
   ```bash
   python document_converter_v2.py
   ```

## Example Usage

```python
from services.document_converter_manager import DocumentConverterManager

# Initialize converter manager
manager = DocumentConverterManager()

# Convert all documents (including images)
results = manager.convert_all()

print(f"Converted {results['successful_conversions']} files")
```

## Features

- **AI-Powered**: Uses OpenAI GPT-4 Vision for text extraction
- **Smart Formatting**: Preserves document structure and formatting
- **Multiple Formats**: Supports all common image formats
- **Automatic Optimization**: Resizes large images for API efficiency
- **Batch Processing**: Convert multiple images at once

## Tips for Best Results

1. **High Quality Images**: Use clear, high-resolution images
2. **Good Lighting**: Ensure text is clearly visible
3. **Proper Orientation**: Make sure images are right-side up
4. **Clean Background**: Avoid cluttered backgrounds around text
5. **Standard Fonts**: Common fonts work better than decorative ones

## Troubleshooting

- **API Key Issues**: Make sure your OpenAI API key is valid and has credits
- **Large Images**: Images are automatically resized if too large
- **Poor Quality**: Try enhancing image quality before conversion
- **Complex Layouts**: Simple layouts work better than complex designs
