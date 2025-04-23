from PySide6.QtWidgets import (QWidget, QHBoxLayout, QPushButton,
                               QFileDialog, QMessageBox)
from PySide6.QtCore import Signal


class ExportPanel(QWidget):
    export_requested = Signal(str)  # Signal emitted with the file path

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Export button
        self.export_button = QPushButton("Export to Text File...")
        self.export_button.clicked.connect(self._open_export_dialog)

        # Add widgets to layout
        layout.addWidget(self.export_button)
        layout.addStretch()

    def _open_export_dialog(self):
        """Open a save file dialog for exporting"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Tree",
            "", "Text Files (*.txt);;All Files (*)"
        )

        if file_path:
            # Add .txt extension if not specified
            if not file_path.lower().endswith('.txt'):
                file_path += '.txt'

            self.export_requested.emit(file_path)

    def show_export_success(self, file_path: str):
        """Show a success message after exporting"""
        QMessageBox.information(
            self, "Export Successful",
            f"Tree structure exported to:\n{file_path}"
        )

    def show_export_error(self, error_msg: str):
        """Show an error message if export fails"""
        QMessageBox.critical(
            self, "Export Failed",
            f"Failed to export tree structure:\n{error_msg}"
        )
