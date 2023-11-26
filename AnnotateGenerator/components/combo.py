from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QComboBox, QSizePolicy, QHBoxLayout, QLabel, QWidget

from AnnotateGenerator.annotate import LayoutRule


class ComboWidgetContainer:
    DESC_FONT: QFont = QFont("Arial", 12)
    MIN_COMBO_WIDTH: int = 130

    def __init__(self, desc_str: str):
        # Layout
        layout: QHBoxLayout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Label
        self.desc_label: QLabel = self.get_desc_label(desc_str=desc_str)
        self.combo_box: QComboBox = self.create_combo()

        # Add 'em
        layout.addWidget(self.desc_label)
        layout.addWidget(self.combo_box)
        layout.setContentsMargins(0, 0, 0, 0)

        # Widget
        self.widget: QWidget = QWidget()
        self.widget.setLayout(layout)

    def create_combo(self) -> QComboBox:
        box: QComboBox = QComboBox()
        items = [e.value for e in LayoutRule]
        box.addItems(items)

        box.setMinimumWidth(self.MIN_COMBO_WIDTH)

        return box

    def get_desc_label(self, desc_str: str) -> QLabel:
        """Create description label"""

        label: QLabel = QLabel(desc_str)
        label.setFont(self.DESC_FONT)

        return label

    @property
    def value(self) -> Optional[LayoutRule]:
        return LayoutRule(self.combo_box.currentText())


ComboWidgetContainer.DESC_FONT.setBold(True)
