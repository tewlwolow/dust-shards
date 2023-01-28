import qtvscodestyle as styler
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QApplication

from ui.windows import MainWindow

class DustShards(QApplication):

    def __init__(self, argv: list[str]) -> None:
        super().__init__(argv)

        QtCore.QDir.addSearchPath('icons', 'ui/icons/')
        icon = QtGui.QIcon('icons:ds_logo.ico')
        self.setWindowIcon(icon)

        QFontDatabase.addApplicationFont("Mistic-Regular.ttf")
        QFontDatabase.addApplicationFont("Pelagiad.ttf")

        stylesheet = styler.Theme.KIMBIE_DARK
        self.setStyleSheet(styler.load_stylesheet(stylesheet))
        self.window = MainWindow(self)
        self.window.show()