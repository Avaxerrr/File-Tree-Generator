# menu_bar.py

# v0.7

from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont, QAction


class MenuBar(QMenuBar):
    install_context_menu_requested = Signal()
    uninstall_context_menu_requested = Signal()
    about_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_menus()

    def _setup_menus(self):
        # Context Install menu
        self.context_menu = QMenu("Context Install", self)

        # Status indicator (non-clickable)
        self.status_action = QAction("Status: Checking...", self)
        self.status_action.setEnabled(False)  # Make it non-clickable
        font = self.status_action.font()
        font.setItalic(True)
        self.status_action.setFont(font)

        # Install/Uninstall actions
        self.install_context_action = QAction("Install Context Menu", self)
        self.uninstall_context_action = QAction("Uninstall Context Menu", self)

        # Add actions to menu
        self.context_menu.addAction(self.status_action)
        self.context_menu.addSeparator()
        self.context_menu.addAction(self.install_context_action)
        self.context_menu.addAction(self.uninstall_context_action)

        # About action
        self.about_action = QAction("About", self)

        # Add menus to the menu bar
        self.addMenu(self.context_menu)
        self.addAction(self.about_action)

        # Connect actions to signals
        self.install_context_action.triggered.connect(self.install_context_menu_requested)
        self.uninstall_context_action.triggered.connect(self.uninstall_context_menu_requested)
        self.about_action.triggered.connect(self.about_requested)

        # Connect aboutToShow signal to update status
        self.context_menu.aboutToShow.connect(self.update_context_menu_status)

    def update_context_menu_status(self):
        """Signal that the menu is about to be shown - status should be updated"""
        # This will be connected to a method in MainWindow
        pass

    def set_context_menu_status(self, is_installed):
        """Update the status text based on installation status"""
        if is_installed:
            self.status_action.setText("Status: Installed")
        else:
            self.status_action.setText("Status: Not Installed")
