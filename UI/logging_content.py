from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QLabel, QWidget, QTextEdit
from PyQt6.QtCore import Qt

class LoggingContent:
    def __init__(self) -> None:
        self.container = QVBoxLayout()
        self.text_field = QTextEdit()

        self.text_field.setReadOnly(True)

        self.container.addWidget(self.text_field)

    def getContainer(self):
        return self.container
    
    def hide(self):
        self.container.removeWidget(self.text_field)
        self.text_field.deleteLater()
        self.container.deleteLater()