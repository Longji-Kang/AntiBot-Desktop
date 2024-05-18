from PyQt6.QtWidgets import QMainWindow, QApplication, QGridLayout, QPushButton, QVBoxLayout, QLabel, QWidget, QSpacerItem
from PyQt6.QtCore import Qt
from sidebar import Sidebar
from version_tab import VersionTab
from ui_controller import UiController

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AntiBot - Home")

        self.cWidg = QWidget()

        self.setCentralWidget(self.cWidg)

        self.grid = QGridLayout()
        self.cWidg.setLayout(self.grid)
        
        self.controller = UiController(self.grid)

        self.sidebar = Sidebar(self.controller)
        self.sidebar_container = self.sidebar.getSidebar()

        self.version_tab = VersionTab()
        self.version_container = self.version_tab.getContainer()

        self.grid.addLayout(self.sidebar_container, 0, 0, 3, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.grid.addLayout(self.version_container, 2, 2, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        self.controller.switchToMain()

        self.showMaximized()


app = QApplication(sys.argv)
w = MainWindow()
app.exec()