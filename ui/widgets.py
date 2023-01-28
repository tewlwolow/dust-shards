from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QSizePolicy


class TextBlockLabel(QLabel):
	def __init__(self, text: str, font_size = None, font_type = None) -> None:
		super().__init__(text)
		self.setWordWrap(True)
		self.setFont(QFont(font_type or 'Pelagiad', font_size or 12))
		self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)