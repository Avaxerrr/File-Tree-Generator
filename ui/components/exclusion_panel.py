from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QListWidget, QLineEdit,
                               QLabel, QCheckBox, QGroupBox)
from PySide6.QtCore import Signal


class ExclusionPanel(QWidget):
    exclusions_changed = Signal()  # Signal when exclusions are updated

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Group box for exclusions
        group_box = QGroupBox("File & Directory Exclusions")
        group_layout = QVBoxLayout(group_box)

        # Use common exclusions checkbox
        self.common_exclusions_cb = QCheckBox("Use common exclusions")
        self.common_exclusions_cb.setChecked(False)
        self.common_exclusions_cb.toggled.connect(self._on_exclusions_changed)
        group_layout.addWidget(self.common_exclusions_cb)

        # List of exclusion patterns
        self.exclusion_list = QListWidget()
        group_layout.addWidget(self.exclusion_list)

        # Input for new patterns
        input_layout = QHBoxLayout()
        self.pattern_input = QLineEdit()
        self.pattern_input.setPlaceholderText("Enter exclusion pattern (e.g., *.pyc, .git)")
        self.pattern_input.returnPressed.connect(self._add_pattern)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self._add_pattern)

        input_layout.addWidget(self.pattern_input)
        input_layout.addWidget(self.add_button)
        group_layout.addLayout(input_layout)

        # Buttons for managing exclusions
        button_layout = QHBoxLayout()

        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(self._remove_pattern)

        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self._clear_patterns)

        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.clear_button)
        group_layout.addLayout(button_layout)

        # Help text
        help_text = QLabel(
            "Patterns can include wildcards: * (any text) and ? (single character)\n"
            "Examples: .git, __pycache__, *.pyc, temp_*"
        )
        help_text.setWordWrap(True)
        group_layout.addWidget(help_text)

        # Add to main layout
        layout.addWidget(group_box)

    def _add_pattern(self):
        """Add a new exclusion pattern"""
        pattern = self.pattern_input.text().strip()
        if pattern and not self._pattern_exists(pattern):
            self.exclusion_list.addItem(pattern)
            self.pattern_input.clear()
            self._on_exclusions_changed()

    def _remove_pattern(self):
        """Remove the selected exclusion pattern"""
        selected_items = self.exclusion_list.selectedItems()
        if selected_items:
            for item in selected_items:
                self.exclusion_list.takeItem(self.exclusion_list.row(item))
            self._on_exclusions_changed()

    def _clear_patterns(self):
        """Clear all exclusion patterns"""
        self.exclusion_list.clear()
        self._on_exclusions_changed()

    def _pattern_exists(self, pattern: str) -> bool:
        """Check if a pattern already exists in the list"""
        for i in range(self.exclusion_list.count()):
            if self.exclusion_list.item(i).text() == pattern:
                return True
        return False

    def _on_exclusions_changed(self):
        """Emit signal when exclusions are changed"""
        self.exclusions_changed.emit()

    def get_exclusion_patterns(self) -> list:
        """Get the list of exclusion patterns"""
        return [self.exclusion_list.item(i).text()
                for i in range(self.exclusion_list.count())]

    def use_common_exclusions(self) -> bool:
        """Check if common exclusions should be used"""
        return self.common_exclusions_cb.isChecked()
