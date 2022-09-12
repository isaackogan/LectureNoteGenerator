import enum
import io
import PIL
from PIL.Image import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
import fitz

class LayoutRule(enum.Enum):
    LINED = "Lined"
    GRID = "Grid"
    NEITHER = "Neither"

def border_right(image: Image, thickness: int = 2, color: str = "#a5b4d4") -> Image:
    new_image: Image = PIL.Image.new("RGBA", (image.width + thickness, image.height), color=color)
    new_image.paste(image, (0, 0))
    return new_image


def resize_image(image: Image, height: float) -> Image:
    height_percent = (height / float(image.size[1]))
    width_size = int((float(image.size[0]) * float(height_percent)))
    return image.resize((width_size, int(height)))

def export_image(image: Image) -> ImageReader:
    side_im_data = io.BytesIO()
    image.save(side_im_data, format='png')
    side_im_data.seek(0)
    return ImageReader(side_im_data)

def convert_file(pdf_path: str, output_path: str, layout: str = LayoutRule.LINED) -> None:
    # noinspection PyUnresolvedReferences
    pdf = fitz.open(pdf_path)

    PAGE_WIDTH, PAGE_HEIGHT = 1800, 1080
    new_pdf = Canvas(output_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    for i in range(0, pdf.page_count, 2):

        # Draw lines on image (lined paper)
        new_pdf.setStrokeColor("#a5b4d4")
        new_pdf.setLineWidth(2)

        if layout == LayoutRule.LINED.value or layout == LayoutRule.GRID.value:
            distance = int(PAGE_HEIGHT / 30)

            for y in range(distance, int(PAGE_HEIGHT), distance):
                new_pdf.line(0, y, PAGE_WIDTH, y)

            if layout == LayoutRule.GRID.value:
                for x in range(distance, int(PAGE_WIDTH), distance):
                    new_pdf.line(x, 0, x, PAGE_HEIGHT)

        # Get Image Pixmaps
        p1, p2 = pdf.load_page(i), pdf.load_page(i + 1) if i + 1 < pdf.page_count else None
        pm1, pm2 = p1.get_pixmap(), p2.get_pixmap() if p2 else None

        # Create PIL Image Objects
        im1: Image = PIL.Image.frombytes("RGB", (pm1.width, pm1.height), pm1.samples)
        im2: Image = PIL.Image.frombytes("RGB", (pm2.width, pm2.height), pm2.samples).resize((im1.width, im1.height)) \
            if pm2 else PIL.Image.new("RGB", (pm1.width, pm1.height), "white")

        # Resize objects to half of page height
        im1 = border_right(resize_image(im1, PAGE_HEIGHT / 2))
        im2 = border_right(resize_image(im2, PAGE_HEIGHT / 2))

        # Paste Images
        new_pdf.setLineWidth(3)
        new_pdf.drawImage(export_image(im1), 0, PAGE_HEIGHT - im1.height)
        new_pdf.drawImage(export_image(im2), 0, 0)

        # Add Divider Line
        new_pdf.line(0, PAGE_HEIGHT - im1.height, PAGE_WIDTH, PAGE_HEIGHT - im1.height)
        new_pdf.line(0, 2, PAGE_WIDTH, 2)
        new_pdf.showPage()

    new_pdf.save()
