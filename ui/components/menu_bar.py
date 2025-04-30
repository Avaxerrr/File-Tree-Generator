# menu_bar.py

from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QAction

class MenuBar(QMenuBar):
    install_context_menu_requested = Signal()
    uninstall_context_menu_requested = Signal()
    about_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_menus()

    def _setup_menus(self):
        # Context Install menu
        context_menu = QMenu("Context Install", self)
        self.install_context_action = QAction("Install Context Menu", self)
        self.uninstall_context_action = QAction("Uninstall Context Menu", self)
        context_menu.addAction(self.install_context_action)
        context_menu.addAction(self.uninstall_context_action)

        # Add Context Install menu to the menu bar
        self.addMenu(context_menu)

        # About menu
        #about_menu = QMenu("About", self)
        self.about_action = QAction("About", self)
        self.addAction(self.about_action)

        # Connect actions to signals
        self.install_context_action.triggered.connect(self.install_context_menu_requested)
        self.uninstall_context_action.triggered.connect(self.uninstall_context_menu_requested)
        self.about_action.triggered.connect(self.about_requested)
