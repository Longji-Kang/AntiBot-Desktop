from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QWidget
from PyQt6.QtCore import Qt, QObject
import PyQt6.QtGui as QtGui
from custom_palette import CustomPalette
from ui_controller import UiController

class Sidebar(QVBoxLayout):
    def __init__(self, controller: UiController) -> None:
        super().__init__()

        container = QVBoxLayout()

        self.homeButton = QPushButton("Home")
        self.logsButton = QPushButton("Logs")

        self.homeButton.setFixedWidth(200)
        self.homeButton.setFixedHeight(75)
        self.logsButton.setFixedWidth(200)
        self.logsButton.setFixedHeight(75)

        self.homeButton.pressed.connect(self.homeclicked)
        self.logsButton.pressed.connect(self.loggingclicked)

        active_palette = self.homeButton.palette()
        active_palette.setColor(self.homeButton.backgroundRole(), QtGui.QColorConstants.Color0)
        active_palette.setColor(self.homeButton.foregroundRole(), QtGui.QColorConstants.Green)

        CustomPalette.setActivePalette(active_palette)
        CustomPalette.setPassivePalette(self.logsButton.palette())


        self.homeButton.setPalette(CustomPalette.active_palette)

        container.addWidget(self.homeButton, 0)
        container.addWidget(self.logsButton, 0)

        self.container = container

        self.controller = controller

    def homeclicked(self):
        print('home')
        self.setCurrent('home')
        self.controller.switchToMain()

    def loggingclicked(self):
        print('logging')
        self.controller.switchToLogging()
        self.setCurrent('logging')

    def getSidebar(self):
        return self.container
    
    def resetButtons(self):
        self.homeButton.setPalette(CustomPalette.passive_palette)
        self.logsButton.setPalette(CustomPalette.passive_palette)

    def setCurrent(self, curr: str) -> None:
        self.resetButtons()

        if curr == 'home':
            self.homeButton.setPalette(CustomPalette.active_palette)
        elif curr == 'logging':
            self.logsButton.setPalette(CustomPalette.active_palette)
            
