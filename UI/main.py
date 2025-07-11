from PyQt6.QtWidgets import QMainWindow, QApplication, QGridLayout, QWidget
from PyQt6.QtCore import Qt, QThread
from sidebar import Sidebar
from version_tab import VersionTab
from ui_controller import UiController

import sys
sys.path.append('../AntiBot-Desktop')
from BusinessLogic.UpdatesSceduler import UpdatesSchedulerClass
from BusinessLogic.LoggingComponent import LoggingComponentClass
from FileSystems.DefinitionFilesInterface import DefinitionsFileInterface
from BusinessLogic.ScanScheduler import ScanScheduler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("AntiBot - Home")

        self.cWidg = QWidget()

        self.setCentralWidget(self.cWidg)

        self.grid = QGridLayout()
        self.cWidg.setLayout(self.grid)

        self.logger = LoggingComponentClass()
        self.definitions_interface = DefinitionsFileInterface()

        # Updates Thread
        self.updates = UpdatesSchedulerClass(self.logger, self.definitions_interface)
        self.updates_thread = QThread()

        self.updates.moveToThread(self.updates_thread)

        self.updates_thread.started.connect(self.updates.run)

        # Scan Thread
        self.scan = ScanScheduler(self.logger, self.definitions_interface)
        self.scan_thread = QThread()

        self.scan.moveToThread(self.scan_thread)
        self.scan_thread.started.connect(self.scan.run)

        # UI
        self.controller = UiController(self.grid, self.logger, self.definitions_interface)

        self.sidebar = Sidebar(self.controller)
        self.sidebar_container = self.sidebar.getSidebar()

        self.version_tab = VersionTab()
        self.version_container = self.version_tab.getContainer()

        self.grid.addLayout(self.sidebar_container, 0, 0, 3, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.grid.addLayout(self.version_container, 2, 2, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        self.updates_thread.start()
        self.scan_thread.start()

        self.controller.switchToMain()

        self.showMaximized()

app = QApplication(sys.argv)
w = MainWindow()
app.exec()