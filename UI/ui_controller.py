from main_content import MainContent
from logging_content import LoggingContent
from PyQt6.QtWidgets import QMainWindow, QApplication, QGridLayout, QPushButton, QVBoxLayout, QLabel, QWidget, QSpacerItem

class UiController:
    def __init__(self, grid: QGridLayout):
        self.grid = grid
        self.main_content = None
        self.logging_content = None

    def switchToMain(self):
        self.main_content = MainContent()

        if self.logging_content is not None:
            self.grid.removeItem(self.logging_content.getContainer().layout())
            self.logging_content.hide()
            self.logging_content = None

        self.grid.addLayout(self.main_content.getContainer(), 1, 1, 1, 1)

    def switchToLogging(self):
        self.logging_content = LoggingContent()

        if self.main_content is not None:
            self.grid.removeItem(self.main_content.getContainer().layout())
            self.main_content.hide()
            self.main_content = None


        self.grid.addLayout(self.logging_content.getContainer(), 1, 1, 1, 1)