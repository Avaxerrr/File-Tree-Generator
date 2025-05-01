# tree_view.py

# v0.7

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit,
                            QHBoxLayout, QRadioButton, QGroupBox,
                            QLabel, QFontComboBox, QSpinBox)
from PySide6.QtGui import QFont, QTextCharFormat, QColor, QBrush, QTextCursor, QTextDocument


class TreeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Format options
        format_group = QGroupBox("Format Options")
        format_layout = QHBoxLayout(format_group)

        self.ascii_radio = QRadioButton("ASCII (+---, |)")
        self.box_drawing_radio = QRadioButton("Box Drawing (├──, │)")
        self.ascii_radio.setChecked(True)

        format_layout.addWidget(self.ascii_radio)
        format_layout.addWidget(self.box_drawing_radio)
        format_layout.addStretch()

        # Font options
        font_group = QWidget()
        font_layout = QHBoxLayout(font_group)
        font_layout.setContentsMargins(0, 0, 0, 0)

        font_layout.addWidget(QLabel("Font:"))
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont("Consolas"))
        font_layout.addWidget(self.font_combo)

        font_layout.addWidget(QLabel("Size:"))
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        self.font_size.setValue(10)
        font_layout.addWidget(self.font_size)

        font_layout.addStretch()

        # Tree display area
        self.tree_display = QTextEdit()
        self.tree_display.setReadOnly(True)
        self.tree_display.setFont(QFont("Consolas", 10))

        # Connect signals
        self.font_combo.currentFontChanged.connect(self._update_font)
        self.font_size.valueChanged.connect(self._update_font)

        # Add widgets to layout
        layout.addWidget(format_group)
        layout.addWidget(font_group)
        layout.addWidget(self.tree_display)

    def _update_font(self):
        """Update the font of the tree display"""
        font = self.font_combo.currentFont()
        font.setPointSize(self.font_size.value())
        self.tree_display.setFont(font)

    def set_tree_content(self, content: str):
        """Set the content of the tree display"""
        self.tree_display.setText(content)

    def get_tree_content(self) -> str:
        """Get the content of the tree display"""
        return self.tree_display.toPlainText()

    def use_box_drawing(self) -> bool:
        """Check if box drawing format is selected"""
        return self.box_drawing_radio.isChecked()

    def highlight_search_results(self, search_text: str, case_sensitive: bool = False):
        """Highlight search results in the tree display"""
        if not search_text:
            return self.clear_search()

        # Clear any previous highlighting
        cursor = self.tree_display.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.setCharFormat(QTextCharFormat())
        cursor.clearSelection()

        # Create format for highlighting
        highlight_format = QTextCharFormat()
        highlight_format.setBackground(QBrush(QColor(255, 255, 0, 100)))  # Light yellow

        # Find and highlight all occurrences
        doc = self.tree_display.document()
        cursor = QTextCursor(doc)

        # Set case sensitivity
        flags = QTextDocument.FindFlags()  # No flags initially
        if case_sensitive:
            flags |= QTextDocument.FindFlag.FindCaseSensitively

        match_count = 0

        # Find first occurrence
        cursor = doc.find(search_text, cursor, flags)

        # Continue finding and highlighting
        while not cursor.isNull():
            cursor.mergeCharFormat(highlight_format)
            match_count += 1
            cursor = doc.find(search_text, cursor, flags)

        # Scroll to the first match if any
        if match_count > 0:
            cursor = self.tree_display.textCursor()
            cursor.setPosition(0)  # Start from the beginning
            self.tree_display.setTextCursor(cursor)

            # Find first occurrence again to position cursor there
            cursor = doc.find(search_text, 0, flags)
            if not cursor.isNull():
                self.tree_display.setTextCursor(cursor)
                self.tree_display.ensureCursorVisible()

        # Show match count in status bar
        self.window().statusBar().showMessage(f"Found {match_count} matches")
        return match_count

    def clear_search(self):
        """Clear search highlighting"""
        cursor = self.tree_display.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.setCharFormat(QTextCharFormat())  # Reset to default format
        cursor.clearSelection()
        self.tree_display.setTextCursor(cursor)
        self.window().statusBar().showMessage("Search cleared")
