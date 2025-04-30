# main_window.py

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                               QLabel, QStatusBar, QSplitter,
                               QHBoxLayout, QMessageBox)
from PySide6.QtCore import Qt

from .components.address_bar import AddressBar
from .components.tree_view import TreeView
from .components.export_panel import ExportPanel
from .components.search_panel import SearchPanel
from .components.exclusion_panel import ExclusionPanel
from .components.menu_bar import MenuBar
from .components.about_dialog import AboutDialog
from utils.context_menu_manager import install_context_menu, uninstall_context_menu, is_context_menu_installed

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("File Tree Generator")
        self.resize(900, 700)

        # Menu bar
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Connect menu status update signal
        self.menu_bar.context_menu.aboutToShow.connect(self.update_context_menu_status)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout - reduce spacing and margins
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        # Directory path section
        dir_section = QWidget()
        dir_layout = QVBoxLayout(dir_section)
        dir_layout.setContentsMargins(0, 0, 0, 0)
        dir_layout.setSpacing(2)

        dir_label = QLabel("Directory Path:")
        self.address_bar = AddressBar()

        dir_layout.addWidget(dir_label)
        dir_layout.addWidget(self.address_bar)

        # Splitter for main content
        splitter = QSplitter(Qt.Horizontal)

        # Left side: Tree view and search panel
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(5)

        self.search_panel = SearchPanel()
        self.tree_view = TreeView()

        left_layout.addWidget(self.search_panel)
        left_layout.addWidget(self.tree_view)

        # Right side: Exclusion panel
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(5)

        self.exclusion_panel = ExclusionPanel()
        right_layout.addWidget(self.exclusion_panel)
        right_layout.addStretch()

        # Add panels to splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        # Export panel
        export_container = QWidget()
        export_layout = QHBoxLayout(export_container)
        export_layout.setContentsMargins(0, 0, 0, 0)

        self.export_panel = ExportPanel()
        export_layout.addWidget(self.export_panel)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Add widgets to layout
        main_layout.addWidget(dir_section)
        main_layout.addWidget(splitter, 1)
        main_layout.addWidget(export_container)

        # Connect search signals
        self.search_panel.search_requested.connect(self.tree_view.highlight_search_results)
        self.search_panel.clear_requested.connect(self.tree_view.clear_search)

        # Connect menu bar signals
        self.menu_bar.about_requested.connect(self.show_about_dialog)
        # The following are placeholders for future logic
        self.menu_bar.install_context_menu_requested.connect(self._on_install_context_menu)
        self.menu_bar.uninstall_context_menu_requested.connect(self._on_uninstall_context_menu)

        self.update_context_menu_status()

    def set_status(self, message: str):
        """Set a message in the status bar"""
        self.status_bar.showMessage(message)

    def show_about_dialog(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec()

    def update_context_menu_status(self):
        """Check and update the context menu installation status"""
        is_installed = is_context_menu_installed()
        self.menu_bar.set_context_menu_status(is_installed)

    def _on_install_context_menu(self):
        success, message = install_context_menu()
        self.set_status(message)
        QMessageBox.information(self, "Context Menu Installation", message if success else f"Error: {message}")
        self.update_context_menu_status()

    def _on_uninstall_context_menu(self):
        success, message = uninstall_context_menu()
        self.set_status(message)
        QMessageBox.information(self, "Context Menu Removal", message if success else f"Error: {message}")
        self.update_context_menu_status()
