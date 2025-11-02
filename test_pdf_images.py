from pdf2image import convert_from_path
from pathlib import Path

pdf_path = "uploads/your_pdf.pdf"

try:
    images = convert_from_path(pdf_path)
    print(f"Successfully extracted {len(images)} images from PDF", end="\n")
    
    # Save first image to verify
    if images:
        images[0].save("test_image_extracted.png")
        print("First page saved as test_image_extracted.png", end="\n")
except Exception as e:
    print(f"Error: {str(e)}", end="\n")
