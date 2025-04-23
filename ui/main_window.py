from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                               QLabel, QStatusBar, QSplitter,
                               QHBoxLayout)
from PySide6.QtCore import Qt

from .components.address_bar import AddressBar
from .components.tree_view import TreeView
from .components.export_panel import ExportPanel
from .components.search_panel import SearchPanel
from .components.exclusion_panel import ExclusionPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("File Tree Generator")
        self.resize(900, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # Title label
        title_label = QLabel("File Tree Generator")
        title_label.setAlignment(Qt.AlignCenter)
        font = title_label.font()
        font.setPointSize(14)
        font.setBold(True)
        title_label.setFont(font)

        # Directory selection
        dir_label = QLabel("Directory Path:")
        self.address_bar = AddressBar()

        # Splitter for main content
        splitter = QSplitter(Qt.Horizontal)

        # Left side: Tree view and search panel
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        # Search panel
        self.search_panel = SearchPanel()

        # Tree view
        self.tree_view = TreeView()

        # Add components to left layout
        left_layout.addWidget(self.search_panel)
        left_layout.addWidget(self.tree_view)

        # Right side: Exclusion panel
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        self.exclusion_panel = ExclusionPanel()
        right_layout.addWidget(self.exclusion_panel)
        right_layout.addStretch()

        # Add panels to splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 3)  # Left side gets more space
        splitter.setStretchFactor(1, 1)

        # Export panel
        self.export_panel = ExportPanel()

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Add widgets to layout
        main_layout.addWidget(title_label)
        main_layout.addWidget(dir_label)
        main_layout.addWidget(self.address_bar)
        main_layout.addWidget(splitter)
        main_layout.addWidget(self.export_panel)

        # Connect search signals
        self.search_panel.search_requested.connect(self.tree_view.highlight_search_results)
        self.search_panel.clear_requested.connect(self.tree_view.clear_search)

    def set_status(self, message: str):
        """Set a message in the status bar"""
        self.status_bar.showMessage(message)
