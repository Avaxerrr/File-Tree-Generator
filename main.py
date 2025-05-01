# main.py

# v0.7


import os
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QFont, QFontDatabase

from ui.main_window import MainWindow
from core.directory_scanner import DirectoryScanner
from core.tree_formatter import TreeFormatter
from core.exclusion_manager import ExclusionManager
from utils.file_exporter import FileExporter
from utils.theme_manager import ThemeManager
import resources_rc

class FileTreeGeneratorApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self._set_app_icon()

        # ---- Global font setup (from qrc) ----
        # Make sure the font is listed in your resources.qrc, e.g.:
        # <file>resources/Sora-VariableFont_wght.ttf</file>
        font_id = QFontDatabase.addApplicationFont(":/resources/Sora-VariableFont_wght.ttf")
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                font_family = families[0]
                font = QFont(font_family)
                font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
                font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
                self.app.setFont(font)
            else:
                print("No families found in font file.")
        else:
            print("Failed to load font from resource: :/resources/Sora-VariableFont_wght.ttf")
        # ---- End global font setup ----

        # Use the embedded QSS resource path
        self.theme_manager = ThemeManager(self.app, base_qss_path=":/resources/themes/base.qss")
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

    def _set_app_icon(self):
        """Set the application icon from embedded resources"""
        self.app.setWindowIcon(QIcon(":/resources/file_tree.png"))

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
