from PyQt6.QtWidgets import QMainWindow, QApplication, QGridLayout, QPushButton, QHBoxLayout, QLabel, QWidget, QSpacerItem
from PyQt6.QtCore import Qt

class VersionTab:
    def __init__(self) -> None:
        self.container = QHBoxLayout()
        self.label = QLabel("AntiBot")
        self.container.addWidget(self.label)

    def getContainer(self):
        return self.container