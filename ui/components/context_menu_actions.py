from PySide6.QtWidgets import QMessageBox
from utils.context_menu_manager import (
    install_context_menu,
    uninstall_context_menu,
    is_context_menu_installed
)

class ContextMenuActions:
    def __init__(self, main_window, menu_bar, status_bar):
        self.main_window = main_window
        self.menu_bar = menu_bar
        self.status_bar = status_bar

    def update_context_menu_status(self):
        """Check and update the context menu installation status"""
        is_installed = is_context_menu_installed()
        self.menu_bar.set_context_menu_status(is_installed)

    def on_install_context_menu(self):
        success, message = install_context_menu()
        self.status_bar.showMessage(message)
        QMessageBox.information(
            self.main_window,
            "Context Menu Installation",
            message if success else f"Error: {message}"
        )
        self.update_context_menu_status()

    def on_uninstall_context_menu(self):
        success, message = uninstall_context_menu()
        self.status_bar.showMessage(message)
        QMessageBox.information(
            self.main_window,
            "Context Menu Removal",
            message if success else f"Error: {message}"
        )
        self.update_context_menu_status()
