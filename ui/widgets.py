from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QSizePolicy


class TextBlockLabel(QLabel):
	def __init__(self, text: str) -> None:
		super().__init__(text)
		self.setWordWrap(True)
		self.setFont(QFont('Bahnschrift'))
		self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)