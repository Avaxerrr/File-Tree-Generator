# theme_manager.py

class ThemeManager:
    def __init__(self, app, base_qss_path=None):
        self.app = app
        self.current_theme = None
        if base_qss_path is not None:
            self.base_qss_path = base_qss_path
        else:
            self.base_qss_path = "resources/themes/base.qss"

    def load_theme(self):
        try:
            with open(self.base_qss_path, "r", encoding="utf-8") as f:
                qss = f.read()
            self.app.setStyleSheet(qss)
            self.current_theme = "base"
            return True
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
