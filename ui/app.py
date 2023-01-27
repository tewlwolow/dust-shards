import qtvscodestyle as styler
from PyQt6.QtWidgets import QApplication

from ui.windows import MainWindow

class DustShards(QApplication):

    def __init__(self, argv: list[str]) -> None:
        super().__init__(argv)

        stylesheet = styler.Theme.DARK_VS
        self.setStyleSheet(styler.load_stylesheet(stylesheet))
        self.window = MainWindow(self)
        self.window.show()