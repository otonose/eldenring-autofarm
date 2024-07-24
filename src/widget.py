from PySide6.QtWidgets import QWidget, QLabel
from toml import 

class Widget(QWidget):
    def __init__(self, config: "dict"):
        super().__init__()
        self.config = config