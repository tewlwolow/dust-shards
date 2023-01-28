import tomllib

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QSizePolicy

from ui import widgets

with open('metadata.toml', mode='rb') as metadata:
    metadata = tomllib.load(metadata)

class MainWindow(QMainWindow):

    def __init__(self, app) -> None:
        super().__init__()

        self.app = app

        self.setWindowTitle('Dust Shards v.' + metadata['version'])
        self.resize(self.screen().availableGeometry().size() * 0.8)

        self.welcome_window = WelcomeWindow(self)
        self.show_welcome()

    def show_welcome(self) -> None:
        self.setCentralWidget(self.welcome_window)
        self.welcome_window.show()


class WelcomeWindow(QWidget):
    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.header = WelcomeHeader(self)

        layout.addWidget(self.header)

class WelcomeHeader(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.setMaximumHeight(int(self.height()/1.5))

        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(header_layout)

        self.name_label = widgets.TextBlockLabel(metadata['name'], 55, 'Mistic')
        self.name_label.setStyleSheet('color: coral;')
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.image_label = QLabel(self)
        pixmap = QtGui.QPixmap("ui/icons/ds_logo.ico")
        pixmap_scaled = pixmap.scaledToWidth(130)
        self.image_label.setPixmap(pixmap_scaled)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.description_label = widgets.TextBlockLabel(metadata['description'], 30)
        self.description_label.setStyleSheet('color: cornsilk;')
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        header_layout.addWidget(self.name_label)
        header_layout.addWidget(self.image_label)
        header_layout.addWidget(self.description_label)

