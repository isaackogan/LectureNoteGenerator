import enum
import io
from typing import Generator, Tuple

import PIL
from PIL.Image import Image
from PyQt6.QtCore import QThread, pyqtSignal
from fitz import Matrix
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
import fitz


class LayoutRule(enum.Enum):
    LINED = "Lined"
    GRID = "Grid"
    BLANK = "Blank"


def export_image(image: Image) -> ImageReader:
    side_im_data = io.BytesIO()
    image.save(side_im_data, format='jpeg', optimize=True)
    side_im_data.seek(0)
    return ImageReader(side_im_data)


class AnnotatedPDFGenerator(QThread):

    MATRIX_ZOOM: int = 2
    PAGE_WIDTH: int = 1800
    PAGE_HEIGHT: int = 1080
    LINE_DIV: int = 30

    def __init__(self, parent, input_fp: str, output_fp: str, layout: LayoutRule):
        super().__init__(parent)
        self.ip: str = input_fp
        self.op: str = output_fp
        self.layout: LayoutRule = layout

    def draw_lines(self, pdf: Canvas, start_x: int) -> None:

        # Line separating slides & grid
        pdf.line(
            x1=start_x,
            x2=start_x,
            y1=0,
            y2=self.PAGE_HEIGHT
        )

        # Grid-specific lines
        if self.layout == self.layout.BLANK:
            return

        # Line spacing
        distance: int = self.PAGE_HEIGHT // self.LINE_DIV

        # Horizontal Lines
        for y in range(distance, int(self.PAGE_HEIGHT), distance):
            pdf.line(start_x, y, self.PAGE_WIDTH, y)

        # Only grid has vertical
        if not self.layout == self.layout.GRID:
            return

        # Vertical Lines
        for x in range(start_x + distance, int(self.PAGE_WIDTH), distance):
            pdf.line(x, 0, x, self.PAGE_HEIGHT)

    def page_fit_rescale(self, height: int, width: int) -> Tuple[int, int]:

        new_height: int = self.PAGE_HEIGHT // 2
        new_width_percent: float = float(new_height) / float(height)
        new_width: float = new_width_percent * float(width)

        return int(new_width), int(new_height)

    def run(self) -> None:

        new_pdf: Canvas = Canvas(
            filename=self.op,
            pagesize=(self.PAGE_WIDTH, self.PAGE_HEIGHT)
        )

        new_pdf.setPageCompression(1)

        for im1, im2 in self.pdf_pages():

            # im1 & im2 will have same height & width
            new_width, new_height = self.page_fit_rescale(width=im1.width, height=im1.height)

            # Draw im1
            new_pdf.drawImage(
                export_image(im1), x=0, y=self.PAGE_HEIGHT - new_height, height=new_height, width=new_width
            )

            # Draw im2
            new_pdf.drawImage(
                export_image(im2), x=0, y=0, height=new_height, width=new_width
            )

            new_pdf.setStrokeColor("#a5b4d4")
            new_pdf.setLineWidth(2)

            # Draw grid lines
            self.draw_lines(
                pdf=new_pdf,
                start_x=new_width
            )

            # Draw midline & page-start divider
            new_pdf.setLineWidth(3)
            new_pdf.line(0, self.PAGE_HEIGHT - new_height, self.PAGE_WIDTH, self.PAGE_HEIGHT - new_height)
            new_pdf.line(0, 2, self.PAGE_WIDTH, 2)

            # Next page
            new_pdf.showPage()

        # Save 'er
        new_pdf.save()

    def pdf_pages(self) -> Generator[Tuple[Image, Image], None, None]:

        pdf: fitz.Document = fitz.Document(filename=self.ip)

        for i in range(0, pdf.page_count, 2):

            # Load Fitz page
            page_1, page_2 = (
                pdf.load_page(i),
                pdf.load_page(i + 1) if i + 1 < pdf.page_count else None
            )

            matrix: Matrix = Matrix(self.MATRIX_ZOOM, self.MATRIX_ZOOM)

            # Convert to Pixmap
            page_1_map, page_2_map = (
                page_1.get_pixmap(matrix=matrix),
                page_2.get_pixmap(matrix=matrix) if page_2 else None
            )

            # Generate Page 1 PIL Image
            page_1_im: Image = PIL.Image.frombytes("RGB", (page_1_map.width, page_1_map.height), page_1_map.samples)

            # Generate Page 2 PIL Image
            page_2_im: Image = (
                PIL.Image.frombytes("RGB", (page_2_map.width, page_2_map.height), page_2_map.samples)
                .resize((page_1_im.width, page_1_im.height))
                if page_2_map else
                PIL.Image.new("RGB", (page_1_map.width, page_1_map.height), "white")  # Fallback white
            )

            yield page_1_im, page_2_im

