import tomllib

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from ui import widgets

from languages import Languages
from ui.widgets import LanguageButton

Languages = Languages()

with open('metadata.toml', mode='rb') as metadata:
    metadata = tomllib.load(metadata)

class MainWindow(QMainWindow):

    def __init__(self, app) -> None:
        super().__init__()

        self.app = app
        self.language_window = None

        self.setWindowTitle('Dust Shards v.' + metadata['version'])
        self.resize(self.screen().availableGeometry().size() * 0.8)

        self.welcome_window = WelcomeWindow(self)
        self.show_welcome()

    def show_welcome(self) -> None:
        self.setCentralWidget(self.welcome_window)
        self.welcome_window.show()

    def show_language(self, language) -> None:
        self.language_window = LanguageWindow(self, language)
        self.setCentralWidget(self.language_window)
        self.language_window.show()

class WelcomeWindow(QWidget):
    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)

        self.header = WelcomeHeader(self)
        self.buttons = WelcomeButtonBlock(self)

        layout.addWidget(self.header)
        layout.addWidget(self.buttons)

class WelcomeHeader(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.setMaximumHeight(int(self.height()/1.5))

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.name_label = widgets.TextBlockLabel(metadata['name'], 45, 'Mistic')
        self.name_label.setStyleSheet('color: coral;')
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # self.image_label = QLabel(self)
        # pixmap = QtGui.QPixmap("ui/icons/ds_logo.ico")
        # pixmap_scaled = pixmap.scaledToWidth(100)
        # self.image_label.setPixmap(pixmap_scaled)
        # self.image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.description_label = widgets.TextBlockLabel(metadata['description'], 20)
        self.description_label.setStyleSheet('color: cornsilk;')
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(self.name_label)
        # layout.addWidget(self.image_label)
        layout.addWidget(self.description_label)

class WelcomeButtonBlock(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)

        for language in Languages.archive:
            lang_button = LanguageButton(self, language)

            layout.addWidget(lang_button)

class LanguageWindow(QWidget):
    def __init__(self, parent, language) -> None:
        super().__init__()
        self.parent = parent
        self.language = language

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.header = LanguageHeader(self)

        layout.addWidget(self.header)


class LanguageHeader(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.setMaximumHeight(int(self.height()/1.5))

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.name_label = widgets.TextBlockLabel(parent.language.name, 45, 'Mistic')
        self.name_label.setStyleSheet('color: coral;')
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.description_label = widgets.TextBlockLabel(self.parent.language.description, 15)
        self.description_label.setStyleSheet('color: cornsilk;')
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(self.name_label)
        layout.addWidget(self.description_label)
