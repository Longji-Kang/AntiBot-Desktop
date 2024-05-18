from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QLabel, QWidget
from PyQt6.QtCore import Qt
from custom_palette import CustomPalette

class MainContent:
    def __init__(self) -> None:
        self.container = QVBoxLayout()

        self.on_off_container = self.createOnOffContainer()
        self.labels_container = self.createLabels()

        self.container.addLayout(self.on_off_container)
        self.container.addLayout(self.labels_container)

    def createOnOffContainer(self):
        container = QVBoxLayout()

        self.button = QPushButton('Toggle State: ON')
        self.button.setPalette(CustomPalette.active_palette)
        self.button.setFixedWidth(200)
        self.button.setFixedHeight(75)

        self.mode_button = QPushButton('Current Mode: Simple Mode')
        self.mode_button.setPalette(CustomPalette.passive_palette)
        self.mode_button.setFixedWidth(200)
        self.mode_button.setFixedHeight(75)

        self.button.clicked.connect(self.on_off_clicked)
        self.mode_button.clicked.connect(self.mode_clicked)

        container.addWidget(self.button, 0, Qt.AlignmentFlag.AlignCenter)
        container.addWidget(self.mode_button, 0, Qt.AlignmentFlag.AlignCenter)

        return container
    
    def createLabels(self):
        self.label_content_box = QHBoxLayout()
        self.label_box = QVBoxLayout()
        self.content_box = QVBoxLayout()

        self.last_scanned_label = QLabel("Last Scan:")
        self.last_scanned = QLabel("13:10 01/01/2024")

        self.last_update_label = QLabel("Last Update:")
        self.last_update = QLabel("13:10 01/01/2024")

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
        else:
            self.button.setPalette(CustomPalette.active_palette)
            self.button.setText("Toggle State: ON")

    def mode_clicked(self):
        pass

    def hide(self):
        self.on_off_container.removeWidget(self.button)
        self.on_off_container.removeWidget(self.mode_button)

        self.label_box.removeWidget(self.last_scanned_label)
        self.label_box.removeWidget(self.last_update_label)

        self.content_box.removeWidget(self.last_scanned)
        self.content_box.removeWidget(self.last_update)