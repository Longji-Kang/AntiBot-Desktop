from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QLabel, QWidget
from PyQt6.QtCore import Qt
from custom_palette import CustomPalette
import sys

sys.path.append('../AntiBot-Desktop')

from BusinessLogic.ConfigState import ConfigurationState, Modes, OnOff, DeleteNoDelete
from BusinessLogic.LoggingComponent import LoggingComponentClass
from BusinessLogic.ScanUpdateInfo import ScanUpdateInfo
from FileSystems.DefinitionFilesInterface import DefinitionsFileInterface

class MainContent:
    def __init__(self, logger: LoggingComponentClass, file_inter: DefinitionsFileInterface) -> None:
        self.file_inter = file_inter
        self.logger = logger
        
        self.container = QVBoxLayout()

        self.delete_button = None

        self.on_off_container = self.createOnOffContainer()
        self.labels_container = self.createLabels()
        self.createDeleteBut()
        self.container.addLayout(self.on_off_container)
        self.container.addLayout(self.labels_container)
        
        if ConfigurationState.getMode() == Modes.ADVANCED:
            self.container.addWidget(self.delete_button, 0, Qt.AlignmentFlag.AlignCenter)

    def createOnOffContainer(self):
        container = QVBoxLayout()

        if ConfigurationState.getOnOff() == OnOff.ON:
            self.button = QPushButton('Toggle State: ON')
            self.button.setPalette(CustomPalette.active_palette)
            self.button.setFixedWidth(200)
            self.button.setFixedHeight(75)
        else:
            self.button = QPushButton('Toggle State: OFF')
            self.button.setPalette(CustomPalette.passive_palette)
            self.button.setFixedWidth(200)
            self.button.setFixedHeight(75)

        if ConfigurationState.getMode() == Modes.BASIC:
            self.mode_button = QPushButton('Current Mode: Simple Mode')
            self.mode_button.setPalette(CustomPalette.passive_palette)
            self.mode_button.setFixedWidth(200)
            self.mode_button.setFixedHeight(75)
        else:
            self.mode_button = QPushButton('Current Mode: Advanced Mode')
            self.mode_button.setPalette(CustomPalette.active_palette)
            self.mode_button.setFixedWidth(200)
            self.mode_button.setFixedHeight(75)

        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.setPalette(CustomPalette.passive_palette)
        self.refresh_button.setFixedWidth(100)
        self.refresh_button.setFixedHeight(36)

        self.button.clicked.connect(self.on_off_clicked)
        self.mode_button.clicked.connect(self.mode_clicked)
        self.refresh_button.clicked.connect(self.refresh)

        container.addWidget(self.button, 0, Qt.AlignmentFlag.AlignCenter)
        container.addWidget(self.mode_button, 0, Qt.AlignmentFlag.AlignCenter)        
        container.addWidget(self.refresh_button, 0, Qt.AlignmentFlag.AlignCenter)
        return container
    
    def createLabels(self):
        self.label_content_box = QHBoxLayout()
        self.label_box = QVBoxLayout()
        self.content_box = QVBoxLayout()

        self.last_scanned_label = QLabel("Last Scan:")
        self.last_scanned = QLabel(ScanUpdateInfo.getLastScan(self.file_inter))

        self.last_update_label = QLabel("Last Update:")
        self.last_update = QLabel(ScanUpdateInfo.getLastUpdate(self.file_inter))

        self.label_box.addWidget(self.last_scanned_label, 0, Qt.AlignmentFlag.AlignLeft)
        self.label_box.addWidget(self.last_update_label, 0, Qt.AlignmentFlag.AlignLeft)

        self.content_box.addWidget(self.last_scanned, 0, Qt.AlignmentFlag.AlignRight)
        self.content_box.addWidget(self.last_update, 0, Qt.AlignmentFlag.AlignRight)

        self.label_content_box.addLayout(self.label_box)
        self.label_content_box.addLayout(self.content_box)

        return self.label_content_box
    
    def getContainer(self):
        return self.container
    
    def on_off_clicked(self):
        if self.button.palette() == CustomPalette.active_palette:
            self.button.setPalette(CustomPalette.passive_palette)
            self.button.setText("Toggle State: OFF")
            ConfigurationState.setOnOff(OnOff.OFF, self.logger)
        else:
            self.button.setPalette(CustomPalette.active_palette)
            self.button.setText("Toggle State: ON")
            ConfigurationState.setOnOff(OnOff.ON, self.logger)

    def mode_clicked(self):
        # Basic -> Advanced
        if self.mode_button.palette() == CustomPalette.passive_palette:
            self.mode_button.setPalette(CustomPalette.active_palette)
            self.mode_button.setText('Current Mode: Advanced Mode')
            ConfigurationState.setMode(Modes.ADVANCED, self.logger)
            
            if self.delete_button == None:
                self.createDeleteBut()
                self.container.addWidget(self.delete_button, 0, Qt.AlignmentFlag.AlignCenter)

        else:
            self.mode_button.setPalette(CustomPalette.passive_palette)
            self.mode_button.setText('Current Mode: Basic Mode')
            ConfigurationState.setMode(Modes.BASIC, self.logger)

            if not self.delete_button == None:
                self.container.removeWidget(self.delete_button)
                self.delete_button.deleteLater()
                self.delete_button = None


    def refresh(self):
        self.label_box.removeWidget(self.last_scanned_label)
        self.label_box.removeWidget(self.last_update_label)

        self.content_box.removeWidget(self.last_scanned)
        self.content_box.removeWidget(self.last_update)

        self.last_scanned_label.deleteLater()
        self.last_update_label.deleteLater()
        self.last_scanned.deleteLater()
        self.last_update.deleteLater()

        self.last_scanned_label = QLabel("Last Scan:")
        self.last_scanned = QLabel(ScanUpdateInfo.getLastScan(self.file_inter))

        self.last_update_label = QLabel("Last Update:")
        self.last_update = QLabel(ScanUpdateInfo.getLastUpdate(self.file_inter))

        self.label_box.addWidget(self.last_scanned_label, 0, Qt.AlignmentFlag.AlignLeft)
        self.label_box.addWidget(self.last_update_label, 0, Qt.AlignmentFlag.AlignLeft)

        self.content_box.addWidget(self.last_scanned, 0, Qt.AlignmentFlag.AlignRight)
        self.content_box.addWidget(self.last_update, 0, Qt.AlignmentFlag.AlignRight)

    def hide(self):
        self.on_off_container.removeWidget(self.button)
        self.on_off_container.removeWidget(self.mode_button)
        self.on_off_container.removeWidget(self.refresh_button)

        self.label_box.removeWidget(self.last_scanned_label)
        self.label_box.removeWidget(self.last_update_label)

        self.content_box.removeWidget(self.last_scanned)
        self.content_box.removeWidget(self.last_update)

        self.button.deleteLater()
        self.mode_button.deleteLater()
        self.refresh_button.deleteLater()

        if not self.delete_button == None:
            self.container.removeWidget(self.delete_button)
            self.delete_button.deleteLater()
            self.delete_button = None

        self.last_scanned_label.deleteLater()
        self.last_update_label.deleteLater()
        self.last_scanned.deleteLater()
        self.last_update.deleteLater()
        self.on_off_container.deleteLater()
        self.label_box.deleteLater()
        self.content_box.deleteLater()

    def createDeleteBut(self):
        if ConfigurationState.getMode() == Modes.ADVANCED:
            if ConfigurationState.getDelete() == DeleteNoDelete.DELETE:
                self.delete_button = QPushButton('Current Action: Delete')
                self.delete_button.setPalette(CustomPalette.active_palette)
                self.delete_button.setFixedWidth(200)
                self.delete_button.setFixedHeight(75)
            else:
                self.delete_button = QPushButton('Current Action: Keep')
                self.delete_button.setPalette(CustomPalette.passive_palette)
                self.delete_button.setFixedWidth(200)
                self.delete_button.setFixedHeight(75)

            self.delete_button.clicked.connect(self.setDeleteConfig)

    def setDeleteConfig(self):
        if ConfigurationState.getDelete() == DeleteNoDelete.DELETE:
            ConfigurationState.setDelete(DeleteNoDelete.NO_DELETE, self.logger)
            self.delete_button.setText('Current Action: Keep')
            self.delete_button.setPalette(CustomPalette.passive_palette)
            self.delete_button.setFixedWidth(200)
            self.delete_button.setFixedHeight(75)
        else:
            ConfigurationState.setDelete(DeleteNoDelete.DELETE, self.logger)
            self.delete_button.setText('Current Action: Delete')
            self.delete_button.setPalette(CustomPalette.active_palette)
            self.delete_button.setFixedWidth(200)
            self.delete_button.setFixedHeight(75)