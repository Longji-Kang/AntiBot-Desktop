from main_content import MainContent
from logging_content import LoggingContent
from PyQt6.QtWidgets import QMainWindow, QApplication, QGridLayout, QPushButton, QVBoxLayout, QLabel, QWidget, QSpacerItem

import sys
sys.path.append('../AntiBot-Desktop')

from BusinessLogic.LoggingComponent import LoggingComponentClass

class UiController:
    def __init__(self, grid: QGridLayout, logger: LoggingComponentClass):
        self.grid = grid
        self.main_content = None
        self.logging_content = None
        self.logger = logger
        

    def switchToMain(self):
        self.main_content = MainContent(self.logger)

        if self.logging_content is not None:
            self.grid.removeItem(self.logging_content.getContainer().layout())
            self.logging_content.hide()
            self.logging_content = None

        self.grid.addLayout(self.main_content.getContainer(), 1, 1, 1, 1)
 

    def switchToLogging(self):
        self.logging_content = LoggingContent(self.logger)

        if self.main_content is not None:
            self.grid.removeItem(self.main_content.getContainer().layout())
            self.main_content.hide()
            self.main_content = None


        self.grid.addLayout(self.logging_content.getContainer(), 1, 1, 1, 1)