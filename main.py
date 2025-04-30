# main.py

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from ui.main_window import MainWindow
from core.directory_scanner import DirectoryScanner
from core.tree_formatter import TreeFormatter
from core.exclusion_manager import ExclusionManager
from utils.file_exporter import FileExporter
from utils.theme_manager import ThemeManager

class FileTreeGeneratorApp:
    def __init__(self):
        # Always resolve resource paths relative to the executable location
        self.base_qss_path = self._resource_path("resources/themes/base.qss")
        self.theme_dir = os.path.dirname(self.base_qss_path)

        # Make sure themes directory exists at the correct location
        os.makedirs(self.theme_dir, exist_ok=True)

        # Create base QSS file if it doesn't exist
        if not os.path.exists(self.base_qss_path):
            self._create_base_qss()

        self.app = QApplication(sys.argv)
        self._set_app_icon()

        # Pass the absolute QSS path to the ThemeManager
        self.theme_manager = ThemeManager(self.app, base_qss_path=self.base_qss_path)
        self.theme_manager.load_theme()

        self.window = MainWindow()

        # Initialize exclusion manager
        self.exclusion_manager = ExclusionManager()

        # Connect signals
        self.window.address_bar.path_changed.connect(self.generate_tree)
        self.window.address_bar.refresh_requested.connect(self.refresh_tree)
        self.window.tree_view.ascii_radio.toggled.connect(self.update_tree_format)
        self.window.tree_view.box_drawing_radio.toggled.connect(self.update_tree_format)
        self.window.export_panel.export_requested.connect(self.export_tree)
        self.window.exclusion_panel.exclusions_changed.connect(self.update_exclusions)

        # Initialize current path and tree data
        self.current_path = ""
        self.tree_data = None

    def _create_base_qss(self):
        """Create the base QSS file if it doesn't exist"""
        with open(self.base_qss_path, "w", encoding="utf-8") as f:
            f.write("/* See full QSS in the base.qss file */")

    def _resource_path(self, relative_path):
        """
        Get absolute path to resource, works for dev and for PyInstaller/Nuitka bundle.
        """
        try:
            # Nuitka or PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        return os.path.join(base_path, relative_path)

    def _set_app_icon(self):
        """Set the application icon from resources/filetree.png"""
        icon_path = self._resource_path("resources/file_tree.png")
        if os.path.exists(icon_path):
            self.app.setWindowIcon(QIcon(icon_path))
        # Optionally, else: print warning if icon not found

    def run(self):
        """Run the application"""
        self.window.show()
        return self.app.exec()

    def process_command_line(self):
        """Process command line arguments if any"""
        if len(sys.argv) > 1:
            folder_path = sys.argv[1]
            if os.path.isdir(folder_path):
                # Set the path in the address bar and generate tree
                self.window.address_bar.set_path(folder_path)

    # The rest of your existing code remains unchanged...
    def update_exclusions(self):
        """Update exclusion patterns from the UI and regenerate tree"""
        # Update exclusion manager from UI
        self.exclusion_manager.clear_patterns()
        patterns = self.window.exclusion_panel.get_exclusion_patterns()
        for pattern in patterns:
            self.exclusion_manager.add_pattern(pattern)

        # Set common exclusions setting
        self.exclusion_manager.set_use_common_exclusions(
            self.window.exclusion_panel.use_common_exclusions()
        )

        # Regenerate tree if we have a path
        if self.current_path:
            self.generate_tree(self.current_path)

    def generate_tree(self, path: str):
        """Generate the tree structure from a directory path"""
        self.current_path = path
        self.window.set_status(f"Scanning directory: {path}")

        try:
            # Scan the directory with exclusions
            scanner = DirectoryScanner(path)
            scanner.set_exclusion_manager(self.exclusion_manager)
            self.tree_data = scanner.scan()

            # Format and display the tree
            self.update_tree_format()

            self.window.set_status(f"Directory scanned successfully: {path}")
        except Exception as e:
            self.window.set_status(f"Error scanning directory: {str(e)}")
            self.window.tree_view.set_tree_content(f"Error: {str(e)}")

    def update_tree_format(self):
        """Update the tree display with the current format settings"""
        if not self.tree_data:
            return

        # Get format preference
        use_box_drawing = self.window.tree_view.use_box_drawing()

        # Format the tree
        formatter = TreeFormatter(use_box_drawing)
        formatted_tree = formatter.format_tree(self.tree_data)

        # Display the tree
        self.window.tree_view.set_tree_content(formatted_tree)

        # Re-apply search if there's an active search
        search_text = self.window.search_panel.get_search_text()
        if search_text:
            self.window.tree_view.highlight_search_results(
                search_text,
                self.window.search_panel.case_sensitive.isChecked()
            )

    def refresh_tree(self):
        """Re-scan the current directory using the current path and settings."""
        if self.current_path:
            self.generate_tree(self.current_path)
        else:
            self.window.set_status("No directory selected to refresh.")

    def export_tree(self, file_path: str):
        """Export the tree to a file"""
        content = self.window.tree_view.get_tree_content()
        if not content:
            self.window.export_panel.show_export_error("No tree content to export")
            return

        if FileExporter.export_to_text(content, file_path):
            self.window.export_panel.show_export_success(file_path)
            self.window.set_status(f"Tree exported to: {file_path}")
        else:
            self.window.export_panel.show_export_error("Failed to write to file")
            self.window.set_status("Export failed")


if __name__ == "__main__":
    app = FileTreeGeneratorApp()
    app.process_command_line()
    sys.exit(app.run())
