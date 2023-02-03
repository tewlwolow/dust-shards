from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt, QByteArray
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QSizePolicy, QPushButton, QDockWidget, QWidget, QFrame

from languages import Languages

import util

class QHLine(QFrame):
	def __init__(self):
		super(QHLine, self).__init__()
		self.setFrameShape(QFrame.Shape.HLine)
		self.setFrameShadow(QFrame.Shadow.Sunken)

class TextBlockLabel(QLabel):
	def __init__(self, text: str, font_size = None, font_type = None) -> None:
		super().__init__(text)
		self.setWordWrap(True)
		self.setFont(QFont(font_type or 'Pelagiad', font_size or 13))
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
		self.setStyleSheet("QLabel { background-color: none; }")

class TableModel(QtCore.QAbstractTableModel):
	def __init__(self, data):
		super(TableModel, self).__init__()

		self.setHeaderData(0, Qt.Orientation.Horizontal, Qt.AlignmentFlag.AlignHCenter, Qt.ItemDataRole.TextAlignmentRole)
		self.setHeaderData(0, Qt.Orientation.Vertical, Qt.AlignmentFlag.AlignVCenter, Qt.ItemDataRole.TextAlignmentRole)

		self._data = {
			'headers': ['Word', 'Stem'],
			'content': []
		}

		for l in data:
			item = [l, self.unpack(util.get_stem(l))]
			self._data['content'].append(item)

	@staticmethod
	def unpack(array: list) -> str:
		cell_data = ""
		for stem in array:
			cell_data += f"{stem}\n"
		return cell_data.rstrip()

	def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
		if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.ItemDataRole.DisplayRole:
			return self._data['headers'][section]

	def data(self, index, role):
		if role == Qt.ItemDataRole.DisplayRole:
			return self._data['content'][index.row()][index.column()]
		elif role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
			return Qt.AlignmentFlag.AlignCenter

	def rowCount(self, index):
		return len(self._data['content'])

	def columnCount(self, index):
		return len(self._data['headers'])

class LanguagePropertiesButton(QPushButton):
	def __init__(self, text: str, font_size: int = None, font_type: str = None) -> None:
		super().__init__(text)
		self.setFont(QFont(font_type or 'Pelagiad', font_size or 14))
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
		self.setStyleSheet("QPushButton { background-color: none; color: cornsilk;}")

class LanguageDescriptionButton(LanguagePropertiesButton):
	def __init__(self, text: str, parent, lang) -> None:
		super().__init__(text)
		self.parent = parent
		self.lang = lang

		def description_action():
			self.parent.parent.show_description(self.lang)

		self.clicked.connect(description_action)

class LanguageHistoryButton(LanguagePropertiesButton):
	def __init__(self, text: str, parent, lang) -> None:
		super().__init__(text)
		self.parent = parent
		self.lang = lang

		def history_action():
			self.parent.parent.show_history(self.lang)

		self.clicked.connect(history_action)

class LanguageCorpusButton(LanguagePropertiesButton):
	def __init__(self, text: str, parent, lang, corpus) -> None:
		super().__init__(text)
		self.parent = parent
		self.lang = lang
		self.corpus = corpus

		def corpus_action():
			self.parent.parent.show_corpus(self.lang, self.corpus)

		self.clicked.connect(corpus_action)


class LanguageCollapsibleButton(QWidget):
	def __init__(self, title="", parent=None):
		super().__init__(parent)

		self.setStyleSheet("""
			background-color: rgba(245,245,220, 0);
			border: none;
		""")

		self.toggle_button = QtWidgets.QToolButton()
		self.toggle_button.setText(title)
		self.toggle_button.setFont(QFont('Pelagiad', 14))

		self.toggle_button.setCheckable(True)
		self.toggle_button.setChecked(False)

		self.toggle_button.setStyleSheet("QToolButton { background-color: none; color: burlywood; }")

		self.toggle_button.setToolButtonStyle(
			QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon
		)
		self.toggle_button.setArrowType(QtCore.Qt.ArrowType.RightArrow)
		self.toggle_button.pressed.connect(self.on_pressed)

		self.toggle_animation = QtCore.QParallelAnimationGroup(self)

		self.content_area = QtWidgets.QScrollArea()
		self.content_area.setMaximumHeight(0)
		self.content_area.setMinimumHeight(0)
		self.content_area.setSizePolicy(
			QSizePolicy.Policy.Expanding,
			QSizePolicy.Policy.Fixed
		)
		self.content_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

		lay = QtWidgets.QVBoxLayout(self)
		lay.setSpacing(0)
		lay.setContentsMargins(0, 0, 0, 0)
		lay.addWidget(self.toggle_button)
		lay.addWidget(self.content_area)

		self.toggle_animation.addAnimation(
			QtCore.QPropertyAnimation(self.content_area, QByteArray(b"maximumHeight"))
		)

	@QtCore.pyqtSlot()
	def on_pressed(self):
		checked = self.toggle_button.isChecked()
		self.toggle_button.setArrowType(
			QtCore.Qt.ArrowType.DownArrow if not checked else QtCore.Qt.ArrowType.RightArrow
		)
		self.toggle_animation.setDirection(
			QtCore.QAbstractAnimation.Direction.Forward
			if not checked
			else QtCore.QAbstractAnimation.Direction.Backward
		)
		self.toggle_animation.start()

	def set_content_layout(self, layout):
		lay = self.content_area.layout()
		del lay
		self.content_area.setLayout(layout)
		collapsed_height = (
				self.sizeHint().height() - self.content_area.maximumHeight()
		)
		content_height = layout.sizeHint().height()

		for i in range(self.toggle_animation.animationCount()):
			animation = self.toggle_animation.animationAt(i)
			animation.setDuration(75)
			animation.setStartValue(collapsed_height)
			animation.setEndValue(collapsed_height + content_height)

		content_animation = self.toggle_animation.animationAt(
			self.toggle_animation.animationCount() - 1
		)
		content_animation.setDuration(75)
		content_animation.setStartValue(0)
		content_animation.setEndValue(content_height)

class LanguageBrowseBar(QDockWidget):
	def __init__(self, parent):
		super().__init__()

		self.parent = parent

		self.languages = Languages()

		# Customize Look
		self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
		self.setTitleBarWidget(QWidget())  # hide title bar

		scroll = QtWidgets.QScrollArea()
		self.setWidget(scroll)
		content = QtWidgets.QWidget()
		scroll.setWidget(content)
		scroll.setWidgetResizable(True)
		scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

		vlay = QtWidgets.QVBoxLayout(content)
		for lang in self.languages.archive:
			lay = QtWidgets.QVBoxLayout()

			label = TextBlockLabel(lang.name, 18)
			label.setStyleSheet("QLabel { background-color: none; color: sandybrown;}")
			vlay.addWidget(label)
			vlay.addWidget(QHLine())

			description = LanguageDescriptionButton("\t\tDescription", self, lang)
			vlay.addWidget(description, alignment=Qt.AlignmentFlag.AlignLeft)

			history = LanguageHistoryButton("\t\tHistory", self, lang)
			vlay.addWidget(history, alignment=Qt.AlignmentFlag.AlignLeft)

			corpus = LanguageCollapsibleButton("Corpus")
			vlay.addWidget(corpus, alignment=Qt.AlignmentFlag.AlignLeft)

			vanilla_locations = LanguageCorpusButton("\t\tVanilla toponymy", self, lang, lang.corpus['vanilla']['toponymy'])
			lay.addWidget(vanilla_locations, alignment=Qt.AlignmentFlag.AlignLeft)

			corpus.set_content_layout(lay)

		vlay.addStretch()







