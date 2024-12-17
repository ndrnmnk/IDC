from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from ui.subwidgets.RichTextDelegate import RichTextDelegate
from PyQt5.QtCore import Qt
import math


class CategorySidebar(QTableWidget):
	def __init__(self, categories):
		super().__init__()
		delegate = RichTextDelegate()
		self.setItemDelegate(delegate)
		self.setFixedWidth(300)
		self.setSelectionMode(QTableWidget.SingleSelection)
		self.setColumnCount(2)
		self.setRowCount(math.ceil(len(categories)/2))  # Set the number of rows based on categories

		self.horizontalHeader().hide()
		self.verticalHeader().hide()

		# Add category items to the table
		for idx, category in enumerate(categories):
			text = f"<span style='color: {category[1]};'>⬛</span> " + category[0]  # for styling
			item = QTableWidgetItem(text)
			item.setTextAlignment(Qt.AlignCenter)
			item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make item non-editable
			self.setItem(math.floor(idx/2), idx%2, item)  # Place item

		# Handle item click
		self.cellClicked.connect(self.on_category_clicked)

	def on_category_clicked(self, row, column):
		item = self.item(row, column)
		if item:
			category = item.text()
			print(category)


app = QApplication([])
window = CategorySidebar([
	("category 1", "#FF0000"),
	("category 2", "#FFFF00"),
	("category 3", "#FF00FF"),
	("category 4", "#00FFFF"),
	("category 5", "#00FF00"),
	("category 6", "#0000FF")])
window.show()
app.exec_()
