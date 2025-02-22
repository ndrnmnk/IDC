from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QGraphicsProxyWidget, QHeaderView
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtCore import Qt
from ui.subwidgets.RichTextDelegate import RichTextDelegate
from backend.config_manager import ConfigManager
import math


class Category(QTableWidgetItem):
	def __init__(self, text, color):
		colored_text = f"<span style='color: {color};'>⬛</span> " + text
		super().__init__(colored_text)
		self.raw_text = text
		self.setTextAlignment(Qt.AlignCenter)
		self.setFlags(self.flags() & ~Qt.ItemIsEditable)

	def get_category_name(self):
		return self.raw_text


class BlockSelectionMenu(QGraphicsProxyWidget):
	def __init__(self, parent_view, categories):
		super().__init__()
		self.setZValue(6)
		self.parent_view = parent_view
		self.table_widget = QTableWidget()
		self.table_widget.setStyleSheet(f"background-color: {ConfigManager().get_config()['styles']['category_selector_bg']}; ")
		self.setWidget(self.table_widget)

		self.table_widget.setItemDelegate(RichTextDelegate())
		self.table_widget.setFixedWidth(300)
		self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.table_widget.setSelectionMode(QTableWidget.SingleSelection)
		self.table_widget.setColumnCount(2)
		self.table_widget.setRowCount(math.ceil(len(categories)/2))
		self.table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.table_widget.horizontalHeader().hide()
		self.table_widget.verticalHeader().hide()

		# Add category items to the table
		for idx, category in enumerate(categories):
			item = Category(category[0], category[1])
			self.table_widget.setItem(math.floor(idx/2), idx % 2, item)

		# Handle item click
		self.table_widget.cellClicked.connect(self.on_category_clicked)

	def on_category_clicked(self, row, column):
		item = self.table_widget.item(row, column)
		if item:
			category = item.get_category_name()
			self.parent_view.on_new_category(category)
			
	def wheelEvent(self, event: QWheelEvent):
		super().wheelEvent(event)
		event.accept()  # Prevent event propagation