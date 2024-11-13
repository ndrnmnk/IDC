from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import math


class CategorySidebar(QTableWidget):
	def __init__(self, categories):
		super().__init__()
		self.setFixedWidth(200)
		self.setRowCount(math.ceil(len(categories)/2))  # Set the number of rows based on categories
		self.setColumnCount(2)  # One column to act like a list

		# Hide the headers
		self.horizontalHeader().hide()  # Hide the top header
		self.verticalHeader().hide()    # Hide the left header

		# Add category items to the table
		for idx, category in enumerate(categories):
			item = QTableWidgetItem(category[0])
			item.setTextAlignment(Qt.AlignCenter)
			item.setForeground(QColor(category[1]))
			item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make item non-editable
			self.setItem(math.floor(idx/2), idx%2, item)  # Place item in the first column

		# Handle item click
		self.cellClicked.connect(self.on_category_clicked)

	def on_category_clicked(self, row, column):
		item = self.item(row, column)
		if item:
			category = item.text()
			print(category)


app = QApplication([])
window = CategorySidebar([("category 1", "#FF0000"), ("category 2", "#FFFF00"), ("category 3", "#FF00FF"), ("category 4", "#00FFFF"), ("category 5", "#00FF00"), ("category 6", "#0000FF")])
window.show()
app.exec_()
