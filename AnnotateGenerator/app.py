import logging
import random
import traceback
from typing import Tuple

from PyQt6.QtCore import Qt, QSize, pyqtSlot, QDir
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QComboBox, QFileDialog
from PyQt6.uic.properties import QtGui

from AnnotateGenerator.annotate import AnnotatedPDFGenerator
from AnnotateGenerator.components.combo import ComboWidgetContainer
from AnnotateGenerator.components.path import PathWidgetContainer
from AnnotateGenerator.components.waiting import ProcessingDialog, FinishedDialog


class AnnotateApp(QMainWindow):

    APP_TITLE: str = "Lecture Note Generator"
    APP_WIDTH, APP_HEIGHT = 800, 500
    BUTTON_SIZE: QSize = QSize(200, 60)

    def center(self):

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __init__(self):
        super().__init__()

        # Set up pane
        self.setWindowTitle(self.APP_TITLE)
        self.setGeometry(0, 0, self.APP_WIDTH, self.APP_HEIGHT)
        self.center()

        # Select Button
        self.select_button: QPushButton = QPushButton("Select Input File (.pdf)")
        self.select_button.pressed.connect(self.select_button_click)
        self.select_button.setFixedSize(self.BUTTON_SIZE)

        # Generate Button
        self.generate_button: QPushButton = QPushButton("Generate PDF File (.pdf)")
        self.generate_button.pressed.connect(self.generate_button_click)
        self.generate_button.setFixedSize(self.BUTTON_SIZE)
        self.generate_button.setEnabled(False)

        # Containers
        self.format_combo: ComboWidgetContainer = ComboWidgetContainer(desc_str="Format:")
        self.input_path: PathWidgetContainer = PathWidgetContainer(desc_str="Selected File:")
        self.output_path: PathWidgetContainer = PathWidgetContainer(desc_str="Output Path:")

        # Layout
        layout: QVBoxLayout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.title_label())

        layout.addWidget(self.input_path.widget)
        layout.addWidget(self.output_path.widget)

        self.format_combo.widget.setContentsMargins(0, 30, 0, 30)

        layout.addWidget(self.format_combo.widget, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.select_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.generate_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Main widget
        widget: QWidget = QWidget()
        widget.setLayout(layout)

        self.processing_dialog = ProcessingDialog(self, self.APP_TITLE)

        self.setCentralWidget(widget)
        self.show()

    def title_label(self) -> QLabel:
        """App Title"""

        label = QLabel(self.APP_TITLE)
        font = QFont("Arial", 25)
        font.setBold(True)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(font)
        label.setContentsMargins(0, 0, 0, 30)

        return label

    def select_button_click(self):

        i_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        o_path: str = i_path.replace(".pdf", f" (Gen-{random.randint(1000, 9000)}).pdf")

        self.input_path.update(i_path)
        self.output_path.update(o_path)

        if not self.generate_button.isEnabled():
            self.generate_button.setEnabled(True)

    def generate_button_click(self):
        self.processing_dialog.show()

        generator: AnnotatedPDFGenerator = AnnotatedPDFGenerator(
                parent=self,
                input_fp=self.input_path.value,
                output_fp=self.output_path.value,
                layout=self.format_combo.value
            )

        generator.finished.connect(self.generate_finished)
        generator.start()

    def generate_finished(self):
        self.processing_dialog.accept()

        FinishedDialog(self, self.APP_TITLE, self.output_path.value).show()


# Create the app, the main window, and run the app
if __name__ == '__main__':
    app = QApplication([])
    window = AnnotateApp()
    app.exec()