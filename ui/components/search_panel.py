#search_panel.py

# v1.0.0

from PySide6.QtWidgets import (QWidget, QHBoxLayout, QLineEdit,
                               QPushButton, QCheckBox, QLabel)
from PySide6.QtCore import Signal


class SearchPanel(QWidget):
    search_requested = Signal(str, bool)  # search_text, case_sensitive
    clear_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 9, 0)

        # Search label
        self.search_label = QLabel("Search:")

        # Search input field
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search text...")
        self.search_input.returnPressed.connect(self._on_search)

        # Case sensitive checkbox
        self.case_sensitive = QCheckBox("Case Sensitive")

        # Search button
        self.search_button = QPushButton("Find")
        self.search_button.clicked.connect(self._on_search)

        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self._on_clear)

        # Add widgets to layout
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input, 1)  # Give search field more space
        layout.addWidget(self.case_sensitive)
        layout.addWidget(self.search_button)
        layout.addWidget(self.clear_button)

    def _on_search(self):
        """Emit a signal with search parameters"""
        search_text = self.search_input.text()
        if search_text:
            self.search_requested.emit(search_text, self.case_sensitive.isChecked())

    def _on_clear(self):
        """Clear the search field and emit clear signal"""
        self.search_input.clear()
        self.clear_requested.emit()

    def get_search_text(self):
        """Get the current search text"""
        return self.search_input.text()
