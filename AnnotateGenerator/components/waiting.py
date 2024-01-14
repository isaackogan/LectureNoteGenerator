import os
import subprocess
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QProgressBar, QVBoxLayout, QPushButton, QWidget

from AnnotateGenerator.components.path import PathWidgetContainer


class ProcessingDialog(QDialog):
    def __init__(self, parent=None, title: str = "Modal"):
        super(ProcessingDialog, self).__init__(parent)
        self.setModal(False)  # Modal = Can you interact with main screen while loaded
        self.setWindowTitle(title)
        self.label = QLabel("Processing... Please wait", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 0)  # Set the progressBar to indeterminate mode
        self.progressBar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.progressBar)

    def closeEvent(self, event):
        # Prevent the dialog from closing if the task is still running
        event.ignore()


class FinishedDialog(QDialog):
    def __init__(self, parent, title, fp):
        super().__init__(parent)

        r_s_i = fp.rfind("/")
        self.fd, self.fp = fp[:r_s_i], fp[r_s_i + 1:]
        self.og_fp = fp
        self.setWindowTitle(title)
        self.setMinimumWidth(200)

        self.layout = QVBoxLayout()

        self.output_path: PathWidgetContainer = PathWidgetContainer("Output:")
        self.output_path.update(self.fp)

        self.buttons_box_widget = QWidget()
        self.buttons_box = QVBoxLayout()
        self.close: QPushButton = QPushButton("Close")
        self.close.pressed.connect(self.accept)
        self.open_dir: QPushButton = QPushButton("Open Directory")
        self.open_dir.pressed.connect(self.open_le_dir)
        self.open_file: QPushButton = QPushButton("Open File")
        self.open_file.pressed.connect(self.open_le_file)

        self.open_file.setMinimumHeight(40)
        self.open_dir.setMinimumHeight(40)
        self.close.setMinimumHeight(40)

        self.buttons_box.addWidget(self.open_dir)
        self.buttons_box.addWidget(self.open_file)
        self.buttons_box.addWidget(self.close)
        self.buttons_box_widget.setLayout(self.buttons_box)

        self.layout.addWidget(self.output_path.widget)
        self.layout.addWidget(self.buttons_box_widget)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

    def open_le_dir(self):
        self.startfile(self.fd)

    def open_le_file(self):
        self.startfile(self.og_fp)

    @classmethod
    def startfile(cls, file_path):

        if sys.platform == "win32":
            os.startfile(file_path)
        elif sys.platform == "darwin":
            subprocess.call(["open", file_path])
        elif sys.platform == "linux":
            subprocess.call(["xdg-open", file_path])
        else:
            raise OSError("No tool found")
