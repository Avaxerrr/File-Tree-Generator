# address_bar.py

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QFileDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal

class AddressBar(QWidget):
    path_changed = Signal(str)
    refresh_requested = Signal()  # New signal for refresh button

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Path input field
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Enter directory path...")
        self.path_input.returnPressed.connect(self._on_path_changed)

        # Browse button
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self._open_file_dialog)

        # Refresh button
        self.refresh_button = QPushButton()
        self.refresh_button.setIcon(QIcon("resources/refresh.png"))
        self.refresh_button.setToolTip("Refresh")
        self.refresh_button.clicked.connect(self._on_refresh_clicked)

        # Add widgets to layout: Browse, Refresh, then Path Input
        layout.addWidget(self.path_input)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.browse_button)

    def get_path(self) -> str:
        """Get the current path from the input field"""
        return self.path_input.text()

    def set_path(self, path: str):
        """Set the path in the input field and trigger path changed signal"""
        self.path_input.setText(path)
        self._on_path_changed()

    def _open_file_dialog(self):
        """Open a file dialog to select a directory"""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory",
            self.path_input.text() or "."
        )

        if directory:
            self.path_input.setText(directory)
            self._on_path_changed()

    def _on_path_changed(self):
        """Emit a signal when the path changes"""
        path = self.path_input.text()
        if path:
            self.path_changed.emit(path)

    def _on_refresh_clicked(self):
        """Emit a signal when the refresh button is clicked"""
        self.refresh_requested.emit()
