# about_dialog.py

# v0.7

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextBrowser, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About File Tree Generator")
        self.setFixedSize(420, 370)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        title_label = QLabel("<b>File Tree Generator</b>")
        title_label.setAlignment(Qt.AlignCenter)

        version_label = QLabel("Version 1.0.0")
        version_label.setAlignment(Qt.AlignCenter)

        author_label = QLabel(
            'Created by <a href="https://github.com/Avaxerrr">Avaxerrr</a>'
        )
        author_label.setAlignment(Qt.AlignCenter)
        author_label.setOpenExternalLinks(True)

        desc_label = QLabel(
            "File Tree Generator is a modern tool for visualizing, searching, and exporting directory trees.<br>"
            "Easily exclude files or folders, switch between ASCII and box-drawing styles, and export your results."
        )
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)

        # Extra spacing
        layout.addSpacing(5)

        github_repo = QLabel(
            'Learn more or get the source code on '
            '<a href="https://github.com/Avaxerrr/File-Tree-Generator">GitHub</a>.'
        )
        github_repo.setAlignment(Qt.AlignCenter)
        github_repo.setOpenExternalLinks(True)

        # More spacing before attribution
        layout.addSpacing(8)

        icon_attribution = QTextBrowser()
        icon_attribution.setOpenExternalLinks(True)
        icon_attribution.setHtml(
            '<div align="center" style="font-size:9pt;">'
            '<b>Credits</b><br>'
            'App icon by '
            '<a href="https://www.flaticon.com/authors/iyahicon" style="color:#5a9bd4;">iyahicon</a> '
            'from <a href="https://www.flaticon.com/" style="color:#5a9bd4;">Flaticon</a><br>'
            'Icon: <a href="https://www.flaticon.com/free-icon/file_6431569" style="color:#5a9bd4;">File (6431569)</a> '
            'in <a href="https://www.flaticon.com/authors/iyahicon/flat-gradient?author_id=973&type=standard" style="color:#5a9bd4;">Flat Gradient Collection</a>'
            '</div>'
        )

        icon_attribution.setMaximumHeight(70)
        icon_attribution.setFrameStyle(0)
        icon_attribution.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        icon_attribution.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Add stretch before close button for better spacing
        layout.addWidget(title_label)
        layout.addWidget(version_label)
        layout.addWidget(author_label)
        layout.addSpacing(5)
        layout.addWidget(desc_label)
        layout.addWidget(github_repo)
        layout.addSpacing(10)
        layout.addWidget(icon_attribution)
        layout.addStretch()

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        close_button.setFixedWidth(90)
        close_button.setDefault(True)
        close_button.setAutoDefault(True)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)
