from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About File Tree Generator")
        self.setFixedSize(350, 200)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel("<b>File Tree Generator</b>")
        title_label.setAlignment(Qt.AlignCenter)
        version_label = QLabel("Version 1.0.0")
        version_label.setAlignment(Qt.AlignCenter)
        author_label = QLabel("Author: Your Name")
        author_label.setAlignment(Qt.AlignCenter)
        desc_label = QLabel("A modern tool for generating and exporting directory trees with exclusion support.")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)

        layout.addWidget(title_label)
        layout.addWidget(version_label)
        layout.addWidget(author_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        layout.addWidget(close_button)
