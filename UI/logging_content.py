from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QLabel, QWidget, QTextEdit
from PyQt6.QtCore import Qt
import sys

sys.path.append('../AntiBot-Desktop')

from BusinessLogic.LoggingComponent import LoggingComponentClass

class LoggingContent:
    def __init__(self, logger: LoggingComponentClass) -> None:
        self.logger = logger
        self.container = QVBoxLayout()
        self.text_field = QTextEdit()
        # self.text_field.setStyleSheet('<style>p {color: red;} div {display: flex; background-color: white;}</style>')
        self.text_field.setReadOnly(True)

        data = self.logger.get_logs()
        self.text_field.setText(data)

        self.container.addWidget(self.text_field)

    def getContainer(self):
        return self.container
    
    def hide(self):
        self.container.removeWidget(self.text_field)