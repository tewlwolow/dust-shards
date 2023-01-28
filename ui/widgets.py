from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QLinearGradient, QColor, QBrush, QAction, QIcon
from PyQt6.QtWidgets import QLabel, QSizePolicy, QPushButton, QListWidgetItem, QWidget, QDockWidget, QListWidget, \
	QStackedWidget, QMainWindow
from qtvscodestyle import Vsc, theme_icon
from qtvscodestyle.qtpy.QtCore import Signal

GRADIENT = QLinearGradient(0, 0, 128, 128)
GRADIENT.setColorAt(0, QColor(242, 220, 134))
GRADIENT.setColorAt(1, QColor(177, 128, 62))
GRADIENT_BRUSH = QBrush(GRADIENT)


class TextBlockLabel(QLabel):
	def __init__(self, text: str, font_size = None, font_type = None) -> None:
		super().__init__(text)
		self.setWordWrap(True)
		self.setFont(QFont(font_type or 'Pelagiad', font_size or 12))
		self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

class LanguageButton(QPushButton):
	def __init__(self, parent, language):
		super().__init__()

		self.parent = parent
		self.setText(language.name)
		self.setFixedSize(150, 60)
		self.setFont(QFont('Pelagiad', 18))
		self.setStyleSheet("""
			color: azure;
			background-color: rgba(245,245,220, 0.1);
			border-radius: 8px;
		"""
		)

		def on_button_clicked():
			self.parent.parent.parent.show_language(language)


		self.clicked.connect(on_button_clicked)
