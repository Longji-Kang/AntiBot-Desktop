from PyQt6.QtWidgets import QMainWindow, QApplication, QGridLayout, QPushButton, QHBoxLayout, QLabel, QWidget, QSpacerItem
from PyQt6.QtCore import Qt

class VersionTab:
    def __init__(self) -> None:
        self.container = QHBoxLayout()
        self.label = QLabel("Current Definition: ")
        self.version = QLabel("v1.2.3")
        self.container.addWidget(self.label)
        self.container.addWidget(self.version)

    def getContainer(self):
        return self.container