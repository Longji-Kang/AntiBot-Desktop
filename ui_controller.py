from main_content import MainContent
from logging_content import LoggingContent
from PyQt6.QtWidgets import QMainWindow, QApplication, QGridLayout, QPushButton, QVBoxLayout, QLabel, QWidget, QSpacerItem

class UiController:
    def __init__(self, grid: QGridLayout):
        self.grid = grid

    def switchToMain(self):
        self.main_content = MainContent()
        self.grid.addLayout(self.main_content.getContainer(), 1, 1, 1, 1)

    def switchToLogging(self):
        self.logging_content = LoggingContent()
        self.grid.addLayout(self.logging_content.getContainer(), 1, 1, 1, 1)