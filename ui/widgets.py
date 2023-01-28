from PyQt6.QtCore import QSize, Qt, QObject
from PyQt6.QtGui import QFont, QColor, QAction, QIcon, QPainter
from PyQt6.QtWidgets import QLabel, QSizePolicy, QPushButton, QDockWidget, QListWidget, QStackedWidget, QWidget, \
	QListWidgetItem, QMainWindow, QVBoxLayout
from qtvscodestyle import theme_icon, Vsc
from qtvscodestyle.qtpy.QtCore import Signal

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

class ActivityBarItem(QListWidgetItem, QObject):

	hovered = Signal()
	toggled = Signal(bool)
	triggered = Signal()

	_action: QAction
	_widget: QWidget

	def __init__(self, widget: QWidget, icon: QIcon | str, text: str):
		super().__init__()

		icon = self._create_icon(icon)

		font = self.font()
		font.setFamily('Pelagiad')
		font.setPointSize(15)

		self.setIcon(icon)
		self.setFont(font)
		self.setText(text)

		# The associated window that is visible while active.
		self._widget = widget

		# Make an action that forwards its events to the widget.
		self._action = QAction(text)
		self._action.hovered.connect(self.hovered.emit)
		self._action.toggled.connect(self.toggled.emit)
		self._action.triggered.connect(self.triggered.emit)

	@staticmethod
	def _create_icon(icon: QIcon | str) -> QIcon:
		icon = QIcon(icon) if isinstance(icon, str) else icon

		pixmap = icon.pixmap(128, 128)
		mask = pixmap.mask()

		painter = QPainter(pixmap)
		painter.fillRect(pixmap.rect(), QColor.fromRgb(245,245,220))
		painter.end()

		pixmap.setMask(mask)

		icon = QIcon(pixmap)
		icon.addPixmap(pixmap, QIcon.Mode.Selected)

		return icon

class BrowseBar(QDockWidget):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self._list = QListWidget()
		self._list.setIconSize(QSize(30, 30))
		self._list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
		self._list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
		self._list.currentItemChanged.connect(self.set_current_item)
		self._list.setStyleSheet(
			"""
            QListWidget { background: rgba(255,245,238, 0.02); }
            QListWidget::item:selected { color: #D1AD61; rgba(255,245,238, 0.04); }
            """
		)

		self._view = QStackedWidget()

		# Customize Look

		self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
		self.setTitleBarWidget(QWidget())  # hide title bar
		self.setMinimumWidth(self._list.iconSize().width() + 12)
		self.setWidget(self._list)

		self.add_item(
			ActivityBarItem(
				widget=LanguagesDock(),
				icon=theme_icon(Vsc.BOOK),
				text="Languages",
			)
		)

	def add_item(self, item: ActivityBarItem) -> None:
		"""Add a new item to the activity bar."""
		self._list.addItem(item)
		self._view.addWidget(item._widget)

	def remove_item(self, item: ActivityBarItem) -> None:
		"""Remove an item from the activity bar."""
		i = self._list.indexFromItem(item).row()
		if i != -1:
			self._list.takeItem(i)
			self._view.removeWidget(item._widget)

	def set_current_item(self, item: ActivityBarItem) -> None:
		"""Set the currently active item in the activity bar."""
		i = self._list.indexFromItem(item).row()
		if i != -1:
			self._list.setCurrentRow(i)
			self._view.setCurrentIndex(i)

class LanguagesDock(QWidget):
	left_dock: QDockWidget

	def __init__(self) -> None:
		super().__init__()

		# Widgets
		self.left_dock = QDockWidget("Languages")
		#
		# # Setup widgets
		# self.left_dock.setWidget(self.explorer)

		# Layout
		main_win = QMainWindow()
		main_win.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.left_dock)

		layout = QVBoxLayout(self)
		layout.addWidget(main_win)
		layout.setContentsMargins(0, 0, 0, 0)




