# theme_manager.py

# v0.7

from PySide6.QtCore import QFile, QTextStream

class ThemeManager:
    def __init__(self, app, base_qss_path=":/resources/themes/base.qss"):
        self.app = app
        self.current_theme = None
        self.base_qss_path = base_qss_path

    def load_theme(self):
        try:
            file = QFile(self.base_qss_path)
            if file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(file)
                qss = stream.readAll()
                self.app.setStyleSheet(qss)
                self.current_theme = "base"
                return True
            else:
                print(f"Failed to open QSS file: {self.base_qss_path}")
                return False
        except Exception as e:
            print(f"Failed to load theme: {e}")
            return False

    def apply_theme(self):
        if self.current_theme == "base":
            self.load_theme()
        else:
            self.app.setStyleSheet("")

    def switch_theme(self, theme_name: str):
        if theme_name == "base":
            self.load_theme()
        else:
            self.app.setStyleSheet("")
            self.current_theme = theme_name
