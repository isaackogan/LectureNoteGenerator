from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QHBoxLayout


class PathWidgetContainer:

    NOT_SELECTED: str = "Not Selected"
    DESC_FONT: QFont = QFont("Arial", 11)
    PATH_FONT: QFont = QFont("Arial", 11)

    def __init__(self, desc_str: str):

        # Layout
        layout: QHBoxLayout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Label
        self.desc_label: QLabel = self.get_desc_label(desc_str=desc_str)
        self.path_label: QLabel = self.get_path_label(path_str=self.NOT_SELECTED)

        # Add 'em
        layout.addWidget(self.desc_label)
        layout.addWidget(self.path_label)
        layout.setContentsMargins(0, 0, 0, 0)

        # Widget
        self.widget: QWidget = QWidget()
        self.widget.setLayout(layout)

        # Value
        self._value: Optional[str] = None

    @property
    def value(self) -> Optional[str]:
        return self._value

    def get_desc_label(self, desc_str: str) -> QLabel:
        """Create description label"""

        label: QLabel = QLabel(desc_str)
        label.setFont(self.DESC_FONT)

        return label

    def get_path_label(self, path_str: str) -> QLabel:
        """Create the path label"""

        label: QLabel = QLabel(path_str)
        label.setFont(self.PATH_FONT)

        return label

    def update(self, value: str) -> None:

        self._value = value
        self.path_label.setText(self._value)


PathWidgetContainer.DESC_FONT.setBold(True)
