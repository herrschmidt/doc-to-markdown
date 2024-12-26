from docling.datamodel.base_models import InputFormat
from docling.document_converter import (
    DocumentConverter,
    ImageFormatOption,
    PdfFormatOption,
)
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from docling.datamodel.pipeline_options import PdfPipelineOptions
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Create a test image
def create_sample_image():
    img = Image.new('RGB', (1200, 800), color='white')
    d = ImageDraw.Draw(img)
    
    # Try to use a system font
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    text = [
        ("Sample Document", font, 50),
        ("", small_font, 120),
        ("This is a test image with multiple lines of text.", small_font, 180),
        ("It includes:", small_font, 240),
        ("• A title", small_font, 300),
        ("• Multiple paragraphs", small_font, 360),
        ("• And bullet points", small_font, 420),
        ("", small_font, 480),
        ("Let's see how well the OCR works!", small_font, 540)
    ]
    
    for line, font_to_use, y_pos in text:
        d.text((50, y_pos), line, fill='black', font=font_to_use)
    
    path = Path(__file__).parent / "sample.png"
    img.save(path)
    return path

def main():
    # Create the image
    image_path = create_sample_image()
    print(f"Created test image at: {image_path}")
    
    # Configure the converter
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True

    doc_converter = DocumentConverter(
        allowed_formats=[InputFormat.IMAGE],
        format_options={
            InputFormat.IMAGE: ImageFormatOption(
                pipeline_cls=StandardPdfPipeline
            ),
        },
    )
    
    # Convert the image
    print("Converting image...")
    result = doc_converter.convert(str(image_path))
    markdown = result.document.export_to_markdown()
    
    print("\nGenerated Markdown:")
    print("=" * 40)
    print(markdown)
    print("=" * 40)

if __name__ == "__main__":
    main()