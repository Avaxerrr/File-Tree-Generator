# about_dialog.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextBrowser
from PySide6.QtCore import Qt

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About File Tree Generator")
        self.setFixedSize(400, 320)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel("<b>File Tree Generator</b>")
        title_label.setAlignment(Qt.AlignCenter)

        version_label = QLabel("Version 1.0.0")
        version_label.setAlignment(Qt.AlignCenter)

        author_label = QLabel('Author: <a href="https://github.com/Avaxerrr">Avaxerrr</a>')
        author_label.setAlignment(Qt.AlignCenter)
        author_label.setOpenExternalLinks(True)

        desc_label = QLabel(
            "A modern tool for generating and exporting directory trees with exclusion support."
        )
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)

        # GitHub repo placeholder
        github_repo = QLabel(
            'GitHub Repo: <a href="https://github.com/Avaxerrr/your-repo-name">https://github.com/Avaxerrr/your-repo-name</a>'
        )
        github_repo.setAlignment(Qt.AlignCenter)
        github_repo.setOpenExternalLinks(True)

        # Icon attribution (with clickable links)
        icon_attribution = QTextBrowser()
        icon_attribution.setOpenExternalLinks(True)
        icon_attribution.setHtml(
            '<div align="center" style="font-size:9pt;">'
            'App icon by '
            '<a href="https://www.flaticon.com/authors/iyahicon" style="color:#5a9bd4;">iyahicon</a> '
            'from <a href="https://www.flaticon.com/" style="color:#5a9bd4;">Flaticon</a><br>'
            'Icon: <a href="https://www.flaticon.com/free-icon/file_6431569" style="color:#5a9bd4;">File (6431569)</a> '
            'in <a href="https://www.flaticon.com/authors/iyahicon/flat-gradient?author_id=973&type=standard" style="color:#5a9bd4;">Flat Gradient Collection</a>'
            '</div>'
        )
        icon_attribution.setMaximumHeight(60)
        icon_attribution.setFrameStyle(0)  # Remove border

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)

        layout.addWidget(title_label)
        layout.addWidget(version_label)
        layout.addWidget(author_label)
        layout.addWidget(desc_label)
        layout.addWidget(github_repo)
        layout.addWidget(icon_attribution)
        layout.addStretch()
        layout.addWidget(close_button)
