import tomllib

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFrame

from ui import widgets


# from ui.resources import styles


class MainWindow(QMainWindow):

    def __init__(self, app) -> None:
        with open('metadata.toml', mode='rb') as metadata:
            self.metadata = tomllib.load(metadata)

        super().__init__()
        self.app = app
        self.welcome_window = WelcomeWindow(self)
        self.setWindowTitle('Dust Shards v. ' + self.metadata['version'])
        self.resize(self.screen().availableGeometry().size() * 0.8)

        # self._create_actions()
        # self._create_menu_bar()
        self.show_welcome()

    def show_welcome(self) -> None:
        self.setCentralWidget(self.welcome_window)
        self.welcome_window.show()

class WelcomeWindow(QWidget):
    def __init__(self, parent) -> None:
        super().__init__()
        self.setParent(parent)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.description_label = widgets.TextBlockLabel("Hello Resdayn!")
        self.description_label.adjustSize()
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.description_label)

        self.setLayout(layout)

