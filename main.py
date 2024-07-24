if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from src.widget import Widget

    app = QApplication()
    widget = Widget()
    app.exec()
