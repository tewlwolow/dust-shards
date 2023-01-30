import tomllib

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableView

from languages import Languages
from ui import widgets
from ui.widgets import LanguageBrowseBar, TableModel

Languages = Languages()

with open('metadata.toml', mode='rb') as metadata:
    metadata = tomllib.load(metadata)

class MainWindow(QMainWindow):

    def __init__(self, app) -> None:
        super().__init__()

        self.app = app

        self.dock = LanguageBrowseBar(self)
        self.dock.show()
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

        self.setWindowTitle('Dust Shards v.' + metadata['version'])
        self.resize(self.screen().availableGeometry().size() * 0.8)

        self.welcome_window = WelcomeWindow(self)
        self.show_welcome()

    def show_welcome(self) -> None:
        self.setCentralWidget(self.welcome_window)
        self.welcome_window.show()

    def show_description(self, language) -> None:
        description_window = DescriptionWindow(self, language)
        self.setCentralWidget(description_window)
        description_window.show()

    def show_history(self, language) -> None:
        history_window = HistoryWindow(self, language)
        self.setCentralWidget(history_window)
        history_window.show()

    def show_corpus(self, language) -> None:
        corpus_window = CorpusWindow(self, language)
        self.setCentralWidget(corpus_window)
        corpus_window.show()

class WelcomeWindow(QWidget):
    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)

        self.header = WelcomeHeader(self)
        self.logo = WelcomeLogo(self)

        layout.addWidget(self.header)
        layout.addWidget(self.logo)

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

        self.description_label = widgets.TextBlockLabel(metadata['description'], 20)
        self.description_label.setStyleSheet('color: cornsilk;')
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(self.name_label)
        layout.addWidget(self.description_label)

class WelcomeLogo(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)

        self.image_label = QLabel(self)
        pixmap = QtGui.QPixmap("ui/icons/ds_logo.ico")
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(self.image_label)


class LanguageHeader(QWidget):
    def __init__(self, parent, lang_name):
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.name_label = widgets.TextBlockLabel(lang_name, 45, 'Mistic')
        self.name_label.setStyleSheet('color: coral;')
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(self.name_label)

class LanguageContent(QWidget):
    def __init__(self, parent, content):
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.label = widgets.TextBlockLabel(content, 15)
        self.label.setStyleSheet('color: cornsilk;')
        self.label.setAlignment(Qt.AlignmentFlag.AlignJustify)

        layout.addWidget(self.label)

class CorpusContent(QWidget):
    def __init__(self, parent, content):
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        self.table = QTableView()
        self.table.setGridStyle(Qt.PenStyle.DashLine)
        self.table.setStyleSheet('color: cornsilk;')

        self.model = TableModel(content)
        self.table.setModel(self.model)

        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()
        layout.addWidget(self.table)

class DescriptionWindow(QWidget):
    def __init__(self, parent, language) -> None:
        super().__init__()
        self.parent = parent
        self.language = language

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.header = LanguageHeader(self, self.language.name)
        self.content = LanguageContent(self, self.language.description)

        layout.addWidget(self.header)
        layout.addWidget(self.content)

class HistoryWindow(QWidget):
    def __init__(self, parent, language) -> None:
        super().__init__()
        self.parent = parent
        self.language = language

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.header = LanguageHeader(self, self.language.name)
        self.content = LanguageContent(self, self.language.history)

        layout.addWidget(self.header)
        layout.addWidget(self.content)

class CorpusWindow(QWidget):
    def __init__(self, parent, language) -> None:
        super().__init__()
        self.parent = parent
        self.language = language

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.header = LanguageHeader(self, self.language.name)
        self.content = CorpusContent(self, self.language.corpus['vanilla']['locations'])

        layout.addWidget(self.header)
        layout.addWidget(self.content)
